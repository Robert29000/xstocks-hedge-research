#!/usr/bin/env python3
"""Fetch xStocks cash-dividend events with ex-date, payment date, underlying prices and option prices.

Default scope: the 10 xStocks with the largest underlying market cap, events of the last 6 months.

Output (in ./data):
  xstocks_dividend_events.csv  one row per xStocks cash-dividend event
  universe.csv                 the selected xStocks with rank and market cap
  rates.csv                    daily SOFR and EFFR (NY Fed)
  fetch_log.txt                log of the run (requests, unmatched events)

Keys: put them in .env (see .env.example). A variable that is set in the shell has priority.

Sources (all free; Massive and Alpha Vantage need a free key):
  xStocks public API   https://api.xstocks.fi/api/v2/public  (events, multipliers, asset list)
  Nasdaq API           https://api.nasdaq.com/api/quote/{T}/dividends  (Nasdaq-listed names)
  Nasdaq screener      https://api.nasdaq.com/api/screener/stocks  (market caps for the ranking)
  stockanalysis.com    https://stockanalysis.com/api/symbol/{s|e}/{t}/dividend  (all US names)
  Alpha Vantage        DIVIDENDS function, only if ALPHAVANTAGE_API_KEY is set
  Yahoo Finance        yfinance, unadjusted daily Close
  NY Fed               https://markets.newyorkfed.org/api/rates/...  (SOFR, EFFR)
  Massive              https://api.polygon.io  (option contracts and daily option prices), only if MASSIVE_API_KEY is set
"""

import argparse
import hashlib
import json
import logging
import os
import time
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

import numpy as np
import pandas as pd
import requests
from scipy.optimize import brentq
from scipy.stats import norm

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"

XSTOCKS_API = "https://api.xstocks.fi/api/v2/public"
NASDAQ_DIVIDENDS = "https://api.nasdaq.com/api/quote/{symbol}/dividends?assetclass={asset_class}"
STOCKANALYSIS_DIVIDENDS = "https://stockanalysis.com/api/symbol/{kind}/{symbol}/dividend"
ALPHAVANTAGE_DIVIDENDS = "https://www.alphavantage.co/query?function=DIVIDENDS&symbol={symbol}&apikey={key}"
NASDAQ_SCREENER = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&download=true"
NYFED_RATES ="https://markets.newyorkfed.org/api/rates/{group}/{rate}/search.json?startDate={start}&endDate={end}"
MASSIVE_API = "https://api.polygon.io"  # Massive, formerly Polygon.io. The key goes in a header, not in the URL.

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}

# Minimum seconds between two requests to the same host. --delay sets the default.
HOST_DELAYS = {
    "api.nasdaq.com": 3.0,
    "stockanalysis.com": 3.0,
    "www.alphavantage.co": 15.0,  # free tier: 25 requests/day, keep it slow
    "api.polygon.io": 12.5,       # Massive free tier: 5 requests/minute
}

NY_TZ = "America/New_York"
WHT_DEFAULT = 0.30

log = logging.getLogger("fetch_data")


class HttpClient:
    """GET JSON with a per-host delay, retry with backoff, and a disk cache."""

    def __init__(self, delay: float, refresh: bool, retries: int = 4, timeout: int = 30):
        self.delay = delay
        self.refresh = refresh
        self.retries = retries
        self.timeout = timeout
        self.session = requests.Session()
        self._last_request: dict[str, float] = {}

    def _wait(self, host: str) -> None:
        min_gap = HOST_DELAYS.get(host, self.delay)
        elapsed = time.monotonic() - self._last_request.get(host, 0.0)
        if elapsed < min_gap:
            time.sleep(min_gap - elapsed)
        self._last_request[host] = time.monotonic()

    @staticmethod
    def _cache_path(url: str) -> Path:
        host = urlparse(url).netloc
        return RAW_DIR / host / f"{hashlib.sha256(url.encode()).hexdigest()[:24]}.json"

    def get_json(self, url: str, headers: dict | None = None, use_cache: bool = True):
        cache_file = self._cache_path(url)
        if use_cache and not self.refresh and cache_file.exists():
            return json.loads(cache_file.read_text())

        host = urlparse(url).netloc
        safe_url = url.split("apikey=")[0] + ("apikey=***" if "apikey=" in url else "")
        last_error = None
        for attempt in range(self.retries):
            self._wait(host)
            try:
                resp = self.session.get(url, headers=headers or {}, timeout=self.timeout)
                log.info("GET %s -> %s", safe_url, resp.status_code)
                if resp.status_code == 429 or resp.status_code >= 500:
                    raise requests.HTTPError(f"HTTP {resp.status_code}")
                if resp.status_code >= 400:
                    return None  # not found / bad request: retry does not help
                payload = resp.json()
                cache_file.parent.mkdir(parents=True, exist_ok=True)
                cache_file.write_text(json.dumps(payload))
                return payload
            except (requests.RequestException, ValueError) as exc:
                last_error = exc
                backoff = 2 ** attempt * max(HOST_DELAYS.get(host, self.delay), 1.0)
                log.warning("GET %s failed (%s), retry in %.0f s", safe_url, exc, backoff)
                time.sleep(backoff)
        log.error("GET %s gave up: %s", safe_url, last_error)
        return None


# ---------------------------------------------------------------- xStocks API

def fetch_assets(client: HttpClient) -> pd.DataFrame:
    rows, page = [], 1
    while True:
        payload = client.get_json(f"{XSTOCKS_API}/assets?page={page}&pageSize=100")
        if not payload:
            break
        for node in payload.get("nodes", []):
            exchange = ((node.get("underlying") or {}).get("exchange") or {})
            rows.append({
                "xstock": node["symbol"],
                "underlying": node.get("underlyingSymbol"),
                "name": node.get("name"),
                "exchange_mic": exchange.get("mic"),
            })
        if not payload.get("page", {}).get("hasNextPage"):
            break
        page += 1
    return pd.DataFrame(rows).drop_duplicates("xstock")


def top_by_market_cap(client: HttpClient, assets: pd.DataFrame, n: int) -> pd.DataFrame:
    """Rank xStocks by the market cap of the underlying company (Nasdaq stock screener, US stocks only)."""
    payload = client.get_json(NASDAQ_SCREENER, headers=BROWSER_HEADERS)
    rows = (((payload or {}).get("data") or {}).get("rows")) or []
    screener = pd.DataFrame(rows)
    if screener.empty:
        raise RuntimeError("Nasdaq screener returned no rows")
    screener["underlying"] = screener["symbol"].str.replace("/", ".", regex=False)
    screener["market_cap_usd"] = pd.to_numeric(screener["marketCap"], errors="coerce")
    # One row for each company: drop the second share class (GOOG/GOOGL, BRK.A/BRK.B).
    screener["company"] = screener["name"].str.split(r" Class | Common | Capital ", regex=True).str[0]

    ranked = (assets.merge(screener[["underlying", "company", "market_cap_usd"]], on="underlying", how="inner")
              .dropna(subset=["market_cap_usd"])
              .sort_values("market_cap_usd", ascending=False)
              .drop_duplicates("company"))
    ranked = ranked.head(n).reset_index(drop=True)
    ranked.insert(0, "rank", ranked.index + 1)
    return ranked[["rank", "xstock", "underlying", "company", "market_cap_usd", "exchange_mic"]]


def fetch_corporate_actions(client: HttpClient, symbols: list[str] | None) -> pd.DataFrame:
    base = f"{XSTOCKS_API}/corporate-actions/history?pageSize=100&sortBy=createdTimeUtc&sortOrder=asc"
    queries = [f"{base}&symbol={s}" for s in symbols] if symbols else [base]
    nodes = []
    for query in queries:
        page = 1
        while True:
            payload = client.get_json(f"{query}&page={page}")
            if not payload:
                break
            nodes.extend(payload.get("nodes", []))
            if not payload.get("page", {}).get("hasNextPage"):
                break
            page += 1

    ca = pd.DataFrame(nodes)
    if ca.empty:
        return ca
    # Pages can overlap and events can have corrected versions: keep the latest version.
    ca = ca.sort_values("version").drop_duplicates("eventId", keep="last")
    ca = ca[(ca["caType"] == "CashDividend") & (ca["status"] != "Cancelled")].copy()
    for col in ["multiplierOld", "multiplierNew", "grossCashflowUsd", "netCashflowUsd", "withholdingTaxRate"]:
        ca[col] = pd.to_numeric(ca[col], errors="coerce")
    ca["effective_time_utc"] = pd.to_datetime(ca["effectiveTimeUtc"], utc=True)
    return ca


# ------------------------------------------------------------ dividend dates

def _parse_date(value, fmt=None):
    if value in (None, "", "N/A", "n/a", "--"):
        return pd.NaT
    return pd.to_datetime(value, format=fmt, errors="coerce")


def _parse_amount(value):
    if value is None:
        return np.nan
    try:
        return float(str(value).replace("$", "").replace(",", ""))
    except ValueError:
        return np.nan


def dividends_from_nasdaq(client: HttpClient, symbol: str) -> pd.DataFrame | None:
    for asset_class in ("stocks", "etf"):
        url = NASDAQ_DIVIDENDS.format(symbol=symbol.replace(".", "/"), asset_class=asset_class)
        payload = client.get_json(url, headers=BROWSER_HEADERS)
        rows = (((payload or {}).get("data") or {}).get("dividends") or {}).get("rows")
        if rows:
            return pd.DataFrame({
                "ex_date": [_parse_date(r.get("exOrEffDate"), "%m/%d/%Y") for r in rows],
                "record_date": [_parse_date(r.get("recordDate"), "%m/%d/%Y") for r in rows],
                "pay_date": [_parse_date(r.get("paymentDate"), "%m/%d/%Y") for r in rows],
                "declaration_date": [_parse_date(r.get("declarationDate"), "%m/%d/%Y") for r in rows],
                "amount": [_parse_amount(r.get("amount")) for r in rows],
                "dates_source": "nasdaq",
            })
    return None


def dividends_from_stockanalysis(client: HttpClient, symbol: str) -> pd.DataFrame | None:
    for kind in ("s", "e"):  # s = stock, e = ETF
        url = STOCKANALYSIS_DIVIDENDS.format(kind=kind, symbol=symbol.lower())
        payload = client.get_json(url, headers=BROWSER_HEADERS)
        rows = ((payload or {}).get("data") or {}).get("history")
        if rows:
            return pd.DataFrame({
                "ex_date": [_parse_date(r.get("dt")) for r in rows],
                "record_date": [_parse_date(r.get("record")) for r in rows],
                "pay_date": [_parse_date(r.get("pay")) for r in rows],
                "declaration_date": [_parse_date(r.get("dec")) for r in rows],
                "amount": [_parse_amount(r.get("amt")) for r in rows],
                "dates_source": "stockanalysis",
            })
    return None


def dividends_from_alphavantage(client: HttpClient, symbol: str) -> pd.DataFrame | None:
    key = os.environ.get("ALPHAVANTAGE_API_KEY")
    if not key:
        return None
    payload = client.get_json(ALPHAVANTAGE_DIVIDENDS.format(symbol=symbol, key=key))
    rows = (payload or {}).get("data")
    if not rows:
        return None
    return pd.DataFrame({
        "ex_date": [_parse_date(r.get("ex_dividend_date")) for r in rows],
        "record_date": [_parse_date(r.get("record_date")) for r in rows],
        "pay_date": [_parse_date(r.get("payment_date")) for r in rows],
        "declaration_date": [_parse_date(r.get("declaration_date")) for r in rows],
        "amount": [_parse_amount(r.get("amount")) for r in rows],
        "dates_source": "alphavantage",
    })


def fetch_dividends(client: HttpClient, symbol: str, exchange_mic: str | None) -> pd.DataFrame | None:
    """Try the source that fits the listing venue first, then the others."""
    sources = [dividends_from_nasdaq, dividends_from_stockanalysis]
    if exchange_mic and exchange_mic != "XNAS":
        sources.reverse()
    sources.append(dividends_from_alphavantage)
    for source in sources:
        divs = source(client, symbol)
        if divs is not None and divs["pay_date"].notna().any():
            return divs.dropna(subset=["ex_date"])
    return None


# -------------------------------------------------------------- event matching

def _activation_day(effective_ny: pd.Timestamp) -> pd.Timestamp:
    """First NY trading session that sees the new multiplier (after 16:00 -> next business day)."""
    day = effective_ny.normalize().tz_localize(None)
    if effective_ny.hour >= 16 or day.weekday() >= 5:
        day = day + pd.offsets.BDay(1)
    return day


def match_event(event: pd.Series, divs: pd.DataFrame) -> dict:
    eff_ny = event["effective_time_utc"].tz_convert(NY_TZ)
    eff_day = eff_ny.normalize().tz_localize(None)
    act_day = _activation_day(eff_ny)

    window = divs[(divs["ex_date"] >= eff_day - pd.Timedelta(days=60))
                  & (divs["ex_date"] <= eff_day + pd.Timedelta(days=10))].copy()
    if window.empty:
        return {"match": "no-dividend-row"}

    gross = event["grossCashflowUsd"]
    window["amount_ok"] = (window["amount"] - gross).abs() <= np.maximum(0.02 * gross, 0.0051)
    window["dist_ex"] = (window["ex_date"] - act_day).dt.days.abs()
    window["dist_pay"] = (window["pay_date"] - eff_day).dt.days.abs()
    window["dist"] = window[["dist_ex", "dist_pay"]].min(axis=1)
    best = window.sort_values(["amount_ok", "dist"], ascending=[False, True]).iloc[0]
    if best["dist"] > 5:
        return {"match": "too-far"}

    lead = (best["ex_date"] - act_day).days
    if 0 <= lead <= 3:
        basis = "ex-date"
    elif pd.notna(best["pay_date"]) and abs((best["pay_date"] - eff_day).days) <= 2:
        basis = "payment-date"
    else:
        basis = "other"

    return {
        "match": "ok" if best["amount_ok"] else "amount-mismatch",
        "activation_basis": basis,
        "effective_time_ny": eff_ny.strftime("%Y-%m-%d %H:%M"),
        "ex_date": best["ex_date"],
        "record_date": best["record_date"],
        "pay_date": best["pay_date"],
        "declaration_date": best["declaration_date"],
        "div_gross_source": best["amount"],
        "dates_source": best["dates_source"],
    }


# ------------------------------------------------------------------- prices

def fetch_closes(symbol: str, start: date, end: date, delay: float, refresh: bool) -> pd.Series:
    import yfinance as yf

    cache = RAW_DIR / "prices" / f"{symbol}_{start}_{end}.csv"
    if cache.exists() and not refresh:
        return pd.read_csv(cache, index_col=0, parse_dates=True).iloc[:, 0]
    time.sleep(delay)
    yf_symbol = symbol.replace(".", "-")
    df = yf.download(yf_symbol, start=start, end=end, auto_adjust=False, progress=False)
    log.info("yfinance %s %s..%s -> %d rows", yf_symbol, start, end, len(df))
    if df.empty:
        return pd.Series(dtype=float)
    close = df["Close"]
    close = close.iloc[:, 0] if isinstance(close, pd.DataFrame) else close
    close.name = "close"
    cache.parent.mkdir(parents=True, exist_ok=True)
    close.to_csv(cache)
    return close


def _close_before(close: pd.Series, day) -> tuple[pd.Timestamp, float]:
    s = close[close.index < day]
    return (s.index[-1], float(s.iloc[-1])) if len(s) else (pd.NaT, np.nan)


def _close_on_or_before(close: pd.Series, day) -> tuple[pd.Timestamp, float]:
    s = close[close.index <= day]
    return (s.index[-1], float(s.iloc[-1])) if len(s) else (pd.NaT, np.nan)


def add_prices(events: pd.DataFrame, delay: float, refresh: bool) -> pd.DataFrame:
    today = pd.Timestamp(date.today())
    out = []
    for underlying, grp in events.groupby("underlying"):
        start = (grp["ex_date"].min() - pd.Timedelta(days=45)).date()
        end = (min(grp["pay_date"].max(), today) + pd.Timedelta(days=5)).date()
        close = fetch_closes(underlying, start, end, delay, refresh)
        log_ret = np.log(close).diff()
        for _, ev in grp.iterrows():
            row = ev.to_dict()
            prev_day, p_prev = _close_before(close, ev["ex_date"])
            _, p_ex = _close_on_or_before(close, ev["ex_date"])
            pay_known = pd.notna(ev["pay_date"]) and ev["pay_date"] <= close.index.max() if len(close) else False
            pay_day, p_pay = _close_on_or_before(close, ev["pay_date"]) if pay_known else (pd.NaT, np.nan)
            vol_window = log_ret[log_ret.index <= prev_day].tail(20) if pd.notna(prev_day) else log_ret.iloc[:0]
            row.update({
                "p_prev_date": prev_day, "p_prev": p_prev, "p_ex": p_ex,
                "p_pay_date": pay_day, "p_pay": p_pay,
                "gap_trading_days": int(((close.index > ev["ex_date"]) & (close.index <= ev["pay_date"])).sum())
                if pay_known else np.nan,
                "vol_20d": float(vol_window.std() * np.sqrt(252)) if len(vol_window) >= 10 else np.nan,
            })
            out.append(row)
    return pd.DataFrame(out)


# ------------------------------------------------------------ option prices

OPTION_COLS = ["opt_expiry", "opt_k_lo", "opt_k_hi", "opt_c_lo_open", "opt_c_hi_open", "opt_c_lo_pay", "opt_c_hi_pay",
               "opt_volume_open", "iv_open", "iv_pay"]


def _bs_call(S: float, K: float, t: float, r: float, sigma: float) -> float:
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * t) / (sigma * np.sqrt(t))
    return S * norm.cdf(d1) - K * np.exp(-r * t) * norm.cdf(d1 - sigma * np.sqrt(t))


def implied_vol(price: float, S: float, K: float, t: float, r: float) -> float:
    """Black-Scholes implied volatility of a call. NaN if no volatility from 0.01% to 500% gives the price."""
    if not (price > 0 and S > 0 and K > 0 and t > 0):
        return np.nan
    try:
        return brentq(lambda s: _bs_call(S, K, t, r, s) - price, 1e-4, 5.0)
    except ValueError:
        return np.nan  # price below the intrinsic value (stale last trade) or above the stock price


def _massive_headers() -> dict:
    return {"Authorization": f"Bearer {os.environ['MASSIVE_API_KEY']}"}


def fetch_option_bars(client: HttpClient, ticker: str, start: pd.Timestamp, end: pd.Timestamp) -> dict:
    """Daily option bars (close = last trade of the day), keyed by NY trading day."""
    url = f"{MASSIVE_API}/v2/aggs/ticker/{ticker}/range/1/day/{start:%Y-%m-%d}/{end:%Y-%m-%d}?adjusted=true&sort=asc&limit=50"
    payload = client.get_json(url, headers=_massive_headers()) or {}
    return {pd.Timestamp(b["t"], unit="ms", tz="UTC").tz_convert(NY_TZ).tz_localize(None).normalize(): b
            for b in payload.get("results") or []}


def option_iv_for_event(client: HttpClient, ev: pd.Series, sofr: pd.Series) -> dict:
    """ATM call implied volatility at the close before the ex-date and at the close on the payment date.

    The hedge strike is S0 = P_prev - D (the ex-dividend start price). The expiry is the first listed expiry on or
    after the payment date. The script uses the two listed strikes around S0 and interpolates the volatility to S0.
    """
    out = dict.fromkeys(OPTION_COLS, np.nan)
    if pd.isna(ev["p_prev"]) or pd.isna(ev["p_pay"]) or pd.isna(ev["pay_date"]):
        return out
    start, pay = ev["p_prev_date"], ev["pay_date"]
    s0 = ev["p_prev"] - ev["div_gross_api"]
    url = (f"{MASSIVE_API}/v3/reference/options/contracts?underlying_ticker={ev['underlying']}&contract_type=call"
           f"&as_of={start:%Y-%m-%d}&expiration_date.gte={pay:%Y-%m-%d}"
           f"&expiration_date.lte={pay + pd.Timedelta(days=45):%Y-%m-%d}"
           f"&strike_price.gte={s0 * 0.9:.2f}&strike_price.lte={s0 * 1.1:.2f}&limit=1000")
    contracts = pd.DataFrame(((client.get_json(url, headers=_massive_headers()) or {}).get("results")) or [])
    if contracts.empty:
        log.warning("no option contracts for %s %s", ev["underlying"], f"{start:%Y-%m-%d}")
        return out
    contracts = contracts[contracts["shares_per_contract"] == 100]
    expiry = contracts["expiration_date"].min()
    chain = contracts[contracts["expiration_date"] == expiry]
    below, above = chain[chain["strike_price"] <= s0], chain[chain["strike_price"] >= s0]
    if below.empty or above.empty:
        log.warning("no strikes around %.2f for %s expiry %s", s0, ev["underlying"], expiry)
        return out
    lo = below.loc[below["strike_price"].idxmax()]
    hi = above.loc[above["strike_price"].idxmin()]
    expiry = pd.Timestamp(expiry)
    bars_lo = fetch_option_bars(client, lo["ticker"], start, pay)
    bars_hi = bars_lo if hi["ticker"] == lo["ticker"] else fetch_option_bars(client, hi["ticker"], start, pay)

    k_lo, k_hi = lo["strike_price"], hi["strike_price"]
    weight = (s0 - k_lo) / (k_hi - k_lo) if k_hi > k_lo else 0.0

    def iv_at(day, spot):
        t = (expiry - day).days / 365
        r = sofr.asof(day) / 100
        c_lo = bars_lo.get(day, {}).get("c", np.nan)
        c_hi = bars_hi.get(day, {}).get("c", np.nan)
        iv_lo, iv_hi = implied_vol(c_lo, spot, k_lo, t, r), implied_vol(c_hi, spot, k_hi, t, r)
        if np.isnan(iv_lo) or np.isnan(iv_hi):
            iv = iv_hi if np.isnan(iv_lo) else iv_lo
        else:
            iv = (1 - weight) * iv_lo + weight * iv_hi
        return c_lo, c_hi, iv

    # Before the ex-date the option price excludes the dividend: use the ex-dividend spot S0.
    c_lo_open, c_hi_open, iv_open = iv_at(start, s0)
    c_lo_pay, c_hi_pay, iv_pay = iv_at(ev["p_pay_date"], ev["p_pay"])
    volume = sum(b.get(start, {}).get("v", 0) for b in ({lo["ticker"]: bars_lo, hi["ticker"]: bars_hi}).values())
    out.update(opt_expiry=expiry.strftime("%Y-%m-%d"), opt_k_lo=k_lo, opt_k_hi=k_hi,
               opt_c_lo_open=c_lo_open, opt_c_hi_open=c_hi_open, opt_c_lo_pay=c_lo_pay, opt_c_hi_pay=c_hi_pay,
               opt_volume_open=volume, iv_open=iv_open, iv_pay=iv_pay)
    return out


def add_option_iv(client: HttpClient, events: pd.DataFrame, rates: pd.DataFrame) -> pd.DataFrame:
    events = events.reset_index(drop=True)
    if not os.environ.get("MASSIVE_API_KEY"):
        log.warning("MASSIVE_API_KEY is not set: no option prices. iv_open and iv_pay stay empty.")
        return events.assign(**dict.fromkeys(OPTION_COLS, np.nan))
    sofr = rates["sofr"].dropna()
    rows = [option_iv_for_event(client, ev, sofr) for _, ev in events.iterrows()]
    events = pd.concat([events, pd.DataFrame(rows, columns=OPTION_COLS)], axis=1)
    log.info("option implied volatility: %d of %d events", events["iv_open"].notna().sum(), len(events))
    return events


# -------------------------------------------------------------------- rates

def fetch_rates(client: HttpClient, start: date, end: date) -> pd.DataFrame:
    frames = []
    for group, rate in (("secured", "sofr"), ("unsecured", "effr")):
        url = NYFED_RATES.format(group=group, rate=rate, start=start, end=end)
        payload = client.get_json(url) or {}
        rows = payload.get("refRates", [])
        s = pd.Series({pd.Timestamp(r["effectiveDate"]): r["percentRate"] for r in rows}, name=rate, dtype=float)
        frames.append(s)
    rates = pd.concat(frames, axis=1, sort=True)
    rates.index.name = "date"
    return rates


# --------------------------------------------------------------------- main

def load_dotenv(path: Path = ROOT / ".env") -> None:
    """Read KEY=VALUE lines from .env. A variable that is already set in the shell has priority."""
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = (part.strip() for part in line.split("=", 1))
        value = value.strip("'\"")
        if value and not os.environ.get(key):
            os.environ[key] = value


def build_events(args) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    client = HttpClient(delay=args.delay, refresh=args.refresh)
    symbols = [s.strip() for s in args.symbols.split(",")] if args.symbols else None

    assets = fetch_assets(client)
    log.info("assets: %d xStocks", len(assets))

    if not symbols and args.top_market_cap:
        universe = top_by_market_cap(client, assets, args.top_market_cap)
        universe.to_csv(DATA_DIR / "universe.csv", index=False)
        symbols = universe["xstock"].tolist()
        log.info("top %d xStocks by market cap: %s", args.top_market_cap, ", ".join(symbols))

    since = pd.Timestamp(args.since) if args.since else pd.Timestamp(date.today()) - pd.DateOffset(months=args.months)
    log.info("events effective since %s", since.date())

    ca = fetch_corporate_actions(client, symbols)
    if ca.empty:
        log.error("no corporate actions returned")
        return
    ca = ca[ca["effective_time_utc"] >= since.tz_localize("UTC")]
    ca = ca.merge(assets, left_on="xstockSymbol", right_on="xstock", how="left")
    ca["underlying"] = ca["underlying"].fillna(ca["spvSymbol"])
    log.info("cash-dividend events: %d for %d xStocks", len(ca), ca["xstockSymbol"].nunique())
    if symbols:
        no_events = sorted(set(symbols) - set(ca["xstockSymbol"]))
        if no_events:
            log.info("no cash-dividend events in the period: %s", ", ".join(no_events))

    rows, unmatched = [], []
    for underlying, grp in ca.groupby("underlying"):
        divs = fetch_dividends(client, underlying, grp["exchange_mic"].iloc[0])
        for _, ev in grp.iterrows():
            info = match_event(ev, divs) if divs is not None else {"match": "no-dividend-source"}
            base = {
                "xstock": ev["xstockSymbol"], "underlying": underlying, "exchange_mic": ev["exchange_mic"],
                "event_id": ev["eventId"], "version": ev["version"], "status": ev["status"],
                "effective_time_utc": ev["effective_time_utc"].strftime("%Y-%m-%d %H:%M"),
                "div_gross_api": ev["grossCashflowUsd"], "div_net_api": ev["netCashflowUsd"],
                "wht_rate": ev["withholdingTaxRate"] if pd.notna(ev["withholdingTaxRate"]) else WHT_DEFAULT,
                "multiplier_old": ev["multiplierOld"], "multiplier_new": ev["multiplierNew"],
            }
            if info["match"] in ("ok", "amount-mismatch"):
                rows.append({**base, **info})
            else:
                unmatched.append({**base, **info})
                log.warning("unmatched %s %s: %s", base["xstock"], base["effective_time_utc"], info["match"])

    events = pd.DataFrame(rows)
    if events.empty:
        log.error("no events matched to dividend dates")
        return
    events = add_prices(events, args.price_delay, args.refresh)

    events["multiplier_step"] = events["multiplier_new"] / events["multiplier_old"] - 1
    events["implied_ref_price"] = events["div_net_api"] / events["multiplier_step"]
    events["gap_days"] = (events["pay_date"] - events["ex_date"]).dt.days
    events["px_change"] = events["p_pay"] / events["p_prev"] - 1
    # Extra cost per underlying share held (N = 1): shares to buy x price move.
    events["shortfall_usd_per_share"] = events["div_net_api"] / events["p_prev"] * (events["p_pay"] - events["p_prev"])

    today = pd.Timestamp(date.today())
    rates = fetch_rates(client, (events["ex_date"].min() - pd.Timedelta(days=30)).date(), today.date())
    rates.to_csv(DATA_DIR / "rates.csv")
    asof = rates.reindex(rates.index.union(events["ex_date"].dropna().unique())).ffill()
    events["sofr_on_ex"] = events["ex_date"].map(asof["sofr"])
    events["effr_on_ex"] = events["ex_date"].map(asof["effr"])
    events = add_option_iv(client, events, rates)

    events = events.sort_values(["ex_date", "xstock"])
    for col in ["ex_date", "record_date", "pay_date", "declaration_date", "p_prev_date", "p_pay_date"]:
        events[col] = pd.to_datetime(events[col]).dt.strftime("%Y-%m-%d")
    events.to_csv(DATA_DIR / "xstocks_dividend_events.csv", index=False)
    unmatched_file = DATA_DIR / "unmatched_events.csv"
    if unmatched:
        pd.DataFrame(unmatched).to_csv(unmatched_file, index=False)
    else:
        unmatched_file.unlink(missing_ok=True)

    log.info("wrote %d events (%d unmatched) to %s", len(events), len(unmatched), DATA_DIR)
    log.info("activation basis: %s", events["activation_basis"].value_counts().to_dict())
    log.info("dates source: %s", events["dates_source"].value_counts().to_dict())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--symbols", help="comma-separated xStock symbols, e.g. AAPLx,KOx (overrides --top-market-cap)")
    parser.add_argument("--top-market-cap", type=int, default=10,
                        help="use the N xStocks with the largest underlying market cap (0 = all xStocks)")
    parser.add_argument("--months", type=int, default=6, help="only events effective in the last N months")
    parser.add_argument("--since", help="only events effective on or after this date (overrides --months)")
    parser.add_argument("--delay", type=float, default=1.0, help="default seconds between requests to one host")
    parser.add_argument("--price-delay", type=float, default=1.0, help="seconds between yfinance downloads")
    parser.add_argument("--refresh", action="store_true", help="ignore the disk cache in data/raw")
    args = parser.parse_args()

    load_dotenv()
    DATA_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler(DATA_DIR / "fetch_log.txt", mode="w")],
    )
    logging.getLogger("yfinance").setLevel(logging.WARNING)
    build_events(args)


if __name__ == "__main__":
    main()
