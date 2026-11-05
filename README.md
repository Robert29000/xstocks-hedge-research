# xStocks dividend-gap hedge research

xStocks are tokenized US stocks from Backed Assets (JE) Limited. A cash dividend does not go to holders as cash. The issuer reinvests it and increases the token multiplier.

Since about May 2026 the issuer increases the multiplier on the evening **before the ex-date**. The custodian receives the dividend cash only on the **payment date**. Between the two dates, the issuer is short the new shares. If the price goes up, the dividend cash buys fewer shares than the multiplier promised.

This project measures that gap and compares three hedge strategies:

| Strategy | Cost formula ($X = N \cdot D \cdot (1-w)$) |
|---|---|
| A. Short-term financing | $X \cdot r_A \cdot T/360$ |
| B. Long futures | $X \cdot (r_B \cdot T/360 + f_B)$ |
| C. Call options | $\approx X \cdot (0.4 \cdot \sigma \cdot \sqrt{T/365} + f_C)$ |

The formula for C is an estimate of the option premium and the fees. The premium and the fees are the maximum cost of C. If the price goes down, the cost is lower.

| Symbol | Meaning | Unit |
|---|---|---|
| $N$ | Number of underlying shares that back the tokens of one xStock | shares |
| $D$ | Gross dividend per share | USD |
| $w$ | Withholding tax rate (0.30 for most US stocks) | fraction |
| $X$ | Net dividend cash that the issuer must reinvest | USD |
| $T$ | Calendar days from the ex-date to the payment date. For A, the loan starts on the ex-date, when the purchase settles. For B and C, the backtest adds the days from the close before the ex-date ($T_{\text{eff}}$). | days |
| $r_A$ | Annual loan rate of the venue (for example EFFR + spread or SOFR + spread), ACT/360 | fraction per year |
| $r_B$ | Annual financing rate in the futures price (SOFR + spread, or the perps funding rate), ACT/360 | fraction per year |
| $f_B$ | Round-trip futures fees (commission and exchange fee, buy and sell) as a fraction of $X$ | fraction |
| $\sigma$ | Annual implied volatility of an at-the-money call (from Massive option prices). If an event has no option price, the 20-day realized volatility. | fraction per year |
| $f_C$ | Round-trip option fees (commission and exchange fees, buy and sell) as a fraction of $X$ | fraction |
| $0.4$ | Approximation of $1/\sqrt{2\pi}$. $0.4 \cdot \sigma \cdot \sqrt{T/365}$ is the price of an at-the-money call as a fraction of the share price. | — |

The venue values of $r_A$, $r_B$, $f_B$, and $f_C$ are in sections 4.1 to 4.3 of the notebook.

**Capital requirements.** The cost formulas do not include the capital that the issuer must lock up during the gap. The value of this capital depends on the issuer's own balance sheet. The notebook shows the capital in separate columns:

| Strategy | Capital | Meaning |
|---|---|---|
| A | $h \cdot X$ | Collateral that the lender asks for in addition to the bought shares (own cash or other assets). Under US Regulation T, $h = 0.5$. |
| B | $m \cdot X$ + buffer | $m$ is the initial margin for futures as a fraction of the notional. The buffer is cash for the daily variation margin. Only cash can serve as futures margin at IBKR. |
| C | None | The issuer pays the premium in full. |

**Ways to make strategy A cheaper.** The cost formula for A is the general case: the issuer borrows all of $X$. Section 4.1 of the notebook lists ways to lower the cost:

1. Pay $h \cdot X$ with own cash. Then the lender lends only $(1-h) \cdot X$, and the interest falls to $(1-h) \cdot X \cdot r_A \cdot T/360$.
2. Pay all of $X$ with own cash, without a loan.
3. Use portfolio margin at IBKR ($h \approx 0.33$ for one stock, USD 110,000 equity to open).
4. Use a lender that does not hold the backing shares. This avoids a conflict between the lender's lien and the pledge for the token holders.

## Project layout

```
fetch_data.py            Script: fetch events, dividend dates, prices, option prices, and rates into data/
.env.example             Template for the API keys. Copy it to .env (git ignores .env).
hedge_research.ipynb     Notebook: data analysis, formulas, venue parameters, backtest
requirements.txt         Python packages
data/                    Output of fetch_data.py (raw/ is the HTTP cache)
docs/legal/              Legal context: issuer, ecosystem, and one file for each venue
```

The notebook holds the numbers. The legal and regulatory context is in [`docs/legal/`](docs/legal/README.md).

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Put the API keys in `.env`:

```bash
cp .env.example .env    # then add the keys to .env
```

| Variable | Use | Necessary |
|---|---|---|
| `MASSIVE_API_KEY` | Option prices for the implied volatility of strategy C. Key: <https://massive.com>. | Yes, for strategy C. Without it, the notebook uses the 20-day realized volatility. |
| `ALPHAVANTAGE_API_KEY` | Third source for dividend dates. Key: <https://www.alphavantage.co/support/#api-key>. | No |

`fetch_data.py` reads `.env` at start. A variable that is set in the shell has priority over the value in `.env`.

## Fetch the data

```bash
# Default scope: the 10 xStocks with the largest underlying market cap, events of the last 6 months
# (< 1 minute without MASSIVE_API_KEY, about 15 minutes with it: the free tier permits 5 requests a minute)
.venv/bin/python fetch_data.py

# Other scopes
.venv/bin/python fetch_data.py --symbols AAPLx,KOx --since 2025-06-01
.venv/bin/python fetch_data.py --top-market-cap 25 --months 12
```

| Flag | Default | Meaning |
|---|---|---|
| `--symbols` | none | Comma-separated xStock symbols. Replaces `--top-market-cap`. |
| `--top-market-cap` | 10 | Use the N xStocks with the largest underlying market cap. 0 = all xStocks (slow: about 500 underlyings). |
| `--months` | 6 | Use only events that became effective in the last N months |
| `--since` | none | Use only events that became effective on or after this date. Replaces `--months`. |
| `--delay` | 1.0 | Minimum seconds between two requests to the same host |
| `--price-delay` | 1.0 | Seconds between two Yahoo Finance downloads |
| `--refresh` | off | Ignore the cache in `data/raw/` and download again |

The script waits between requests to each host. Some hosts have a fixed longer delay: Nasdaq and stockanalysis.com 3 s, Massive 12.5 s, Alpha Vantage 15 s. The script retries a failed request (HTTP 429, HTTP 5xx, or timeout) up to 4 times with exponential backoff. The script keeps every response in `data/raw/`. A second run reads the cache and sends no requests.

### Steps

1. Fetch the xStocks asset list (xStock symbol to underlying symbol and listing venue). Rank the underlyings by market cap with the Nasdaq stock screener and keep the top N. One company counts once, so GOOG and GOOGL are one company. ETFs are not in the screener.
2. Fetch the corporate-action history. Keep the latest version of each `CashDividend` event. Remove cancelled events.
3. Fetch the dividend history of each underlying. The script uses Nasdaq first for Nasdaq-listed stocks and stockanalysis.com first for other stocks. Alpha Vantage is the last fallback.
4. Match each event to the dividend row with the nearest ex-date or payment date and the same amount. Classify the event as `ex-date` or `payment-date` activation.
5. Fetch daily unadjusted close prices from Yahoo Finance. Calculate the close before the ex-date, the close on the payment date, and the 20-day realized volatility.
6. Fetch daily SOFR and EFFR from the NY Fed.
7. If `MASSIVE_API_KEY` is set, fetch the call options of each event from Massive. The script uses the first listed expiry on or after the payment date and the two strikes around $S_0 = P_{\text{prev}} - D$. It calculates the Black-Scholes implied volatility from the daily close of each option. It interpolates the volatility to $S_0$. It does this at the close before the ex-date and at the close on the payment date.

### Output

`data/xstocks_dividend_events.csv`, one row for each event:

| Column | Meaning |
|---|---|
| `xstock`, `underlying`, `exchange_mic` | Symbols and listing venue |
| `event_id`, `version`, `status` | xStocks event identity |
| `effective_time_utc`, `effective_time_ny` | Time when the new multiplier becomes active |
| `activation_basis` | `ex-date` (multiplier before the ex-date), `payment-date`, or `other` |
| `ex_date`, `record_date`, `pay_date`, `declaration_date` | Dividend dates |
| `dates_source` | `nasdaq`, `stockanalysis`, or `alphavantage` |
| `match` | `ok`, or `amount-mismatch` if the API amount and the source amount differ by more than 2% |
| `div_gross_api`, `div_net_api`, `wht_rate`, `div_gross_source` | Dividend per share (USD) and withholding rate |
| `multiplier_old`, `multiplier_new`, `multiplier_step` | Multiplier before and after, and the relative step |
| `implied_ref_price` | `div_net_api / multiplier_step`, the close price that the issuer used |
| `p_prev_date`, `p_prev` | Close before the ex-date |
| `p_ex` | Close on the ex-date |
| `p_pay_date`, `p_pay` | Close on the payment date (empty if the payment date is in the future) |
| `gap_days`, `gap_trading_days` | Calendar days and trading days from the ex-date to the payment date |
| `px_change` | `p_pay / p_prev - 1` (positive is a loss for the issuer) |
| `shortfall_usd_per_share` | Loss in USD for each underlying share held |
| `vol_20d` | 20-day realized volatility (annual) before the ex-date |
| `sofr_on_ex`, `effr_on_ex` | Rates in % on the ex-date |
| `opt_expiry`, `opt_k_lo`, `opt_k_hi` | Option expiry and the two strikes around $S_0$ |
| `opt_c_lo_open`, `opt_c_hi_open`, `opt_c_lo_pay`, `opt_c_hi_pay` | Option close (last trade, USD per share) of the two strikes, before the ex-date and on the payment date |
| `opt_volume_open` | Contracts traded in the two strikes on the day before the ex-date |
| `iv_open`, `iv_pay` | At-the-money implied volatility (annual) at the close before the ex-date and on the payment date |

Other output files:

- `data/universe.csv`: the selected xStocks with rank and market cap. Some of them pay no dividend.
- `data/rates.csv`: daily SOFR and EFFR.
- `data/unmatched_events.csv`: events without dividend dates.
- `data/fetch_log.txt`: the log of each request.

## Run the notebook

```bash
.venv/bin/jupyter lab hedge_research.ipynb
# or run all cells from the command line:
.venv/bin/jupyter nbconvert --to notebook --execute --inplace hedge_research.ipynb
```

## Data sources

| Data | Source | Key | Limit |
|---|---|---|---|
| Events, multipliers, assets | <https://api.xstocks.fi/api/v2/public> ([docs](https://docs.xstocks.fi/apis/openapi)) | No | Not published |
| Market cap ranking | `https://api.nasdaq.com/api/screener/stocks` (unofficial) | No | Not published. One request. |
| Dividend dates, Nasdaq-listed | `https://api.nasdaq.com/api/quote/{T}/dividends` (unofficial) | No | Not published. A browser User-Agent is necessary. |
| Dividend dates, all US | `https://stockanalysis.com/api/symbol/{s,e}/{t}/dividend` (unofficial) | No | Not published |
| Dividend dates, fallback | Alpha Vantage `DIVIDENDS` | Free key | 25 requests a day |
| Prices | Yahoo Finance via `yfinance` (unofficial) | No | Not published |
| SOFR, EFFR | <https://markets.newyorkfed.org/api/rates> | No | Not published |
| Option contracts and daily option prices | Massive (formerly Polygon.io), `https://api.polygon.io` `/v3/reference/options/contracts` and `/v2/aggs` | Free key | 5 requests a minute. End-of-day data. No bid and ask. |

## Limitations and Assumptions

### Data

- **Sample size.** The default scope gives 14 events for 7 stocks (run of 2026-11-04). AMZN, SPCX (SpaceX), and TSLA are in the top 10 but paid no dividend in the period. Read the backtest results as an indication, not as a statistic.
- **Unofficial sources.** The Nasdaq, stockanalysis.com, and Yahoo Finance endpoints are unofficial. They can change without notice.
- **Dividend dates for NYSE stocks.** The Nasdaq dividend endpoint covers only Nasdaq-listed stocks. No Alpha Vantage key was set, so the script uses stockanalysis.com for other stocks. In the default scope, this applies to TSM.
- **Non-US underlyings.** Non-US underlyings (for example Hong Kong listings) have no dividend dates at these sources. They are in `data/unmatched_events.csv`.
- **TSM.** TSM pays its dividend in TWD. The xStocks API shows 0% withholding tax for TSM. Its USD amount differs a little from the source amount, so its reference-price check can differ by up to 0.3%.

### Model

- **Volatility.** Strategy C uses the implied volatility from the option close (the last trade of the day). The last trade can be some minutes older than the stock close. If an event has no option price, the notebook uses the 20-day realized volatility. See [Realized and implied volatility](#realized-and-implied-volatility).
- **Costs not included.** The formulas do not include bid-ask spreads. The free Massive data has no bid and ask.
- **Structural gain of strategy A.** The multiplier uses the close with the dividend, so the issuer gains about $D/P_{\text{prev}}$ of $X$. Strategy A buys the shares at that close, with the dividend. It gets the net dividend on the new shares instead, so its gain is only $(1-w) \cdot D/P_{\text{prev}}$. The backtest does not include this difference (about 3 bps of $X$ on average).
- **Capital.** The cost formulas do not include the capital that A and B lock up. See **Capital requirements** at the start of this README.
- **Contract size.** The formulas assume that any number of shares can be hedged. For $N = 100{,}000$, more than half of the events need fewer than 100 shares. Options and standard futures then over-hedge. Strategy A has no contract size.
- **Futures expiry.** Futures expire monthly (Eurex) or quarterly (CME). The model closes them on the payment date and ignores the basis change on that date.
- **Margin and collateral values.** The futures margins and the collateral values $h$ are static. No free source gives historical values, and the CME margin pages block scripts. Swiss banks publish no loan-to-value for one stock, so their $h$ is an ESTIMATE.

### Realized and implied volatility

| | Realized volatility | Implied volatility |
|---|---|---|
| Definition | Standard deviation of past daily log returns, times $\sqrt{252}$ | The $\sigma$ at which the Black-Scholes price equals the market price of the option |
| Direction | Backward-looking | Forward-looking |
| Correct use | Price risk in the gap (unhedged case) | Cost of strategy C |
| In the notebook | `vol_20d`: unhedged risk band, and the fallback for strategy C | `iv_open`, `iv_pay`: cost of strategy C |

The 20-day realized volatility is not a good replacement for the implied volatility. Usually it is a little lower. But if the 20-day window contains an earnings day, it can be much higher. Example: AAPL, ex-date 2026-08-10. The implied volatility was 23%, and the 20-day realized volatility was 38%.

### Venue parameters

Venue rates and fees were checked on 2026-10-19. The notebook gives each value a status: CONFIRMED, UNCONFIRMED, ESTIMATE, or ASSUMPTION. The notebook tables, the backtest, and the result use only CONFIRMED venues. Section 9 of the notebook lists the other venues. Check these values with the venue before a decision:

1. Which Interactive Brokers entity onboards a Jersey company (UNCONFIRMED).
2. Whether Interactive Brokers offers CME single stock futures (UNCONFIRMED).
3. The CME exchange fee for single stock futures (ASSUMPTION: USD 0.30 per side).
4. The Kraken xStocks perps funding rate (ASSUMPTION: 10.95% per year).
5. The Eurex total return futures spread (ASSUMPTION: 0.50% per year).
6. The IBKR margin for Eurex single stock futures (ESTIMATE: 1.15 times the Eurex margin, thus 13%) and for the new CME single stock futures (UNCONFIRMED: 20%). The collateral $h$ for Swiss Lombard loans (ESTIMATE: 0.5). Margin and collateral values were checked on 2026-11-04.
7. The terms of Alpaca, InCore Bank, and a Payward intercompany loan. These terms are not public.

### Legal

- **No derivatives clause.** The prospectus has no clause that permits the issuer to use futures or options. Strategies B and C can need a prospectus supplement, Jersey FSC consent, or a hedge by a group company.
- **Pledged collateral.** The underlying shares are pledged to the security agent for the token holders. A loan for strategy A needs other collateral or no collateral. The futures margin for strategy B must be free cash of the issuer. IBKR, Alpaca, and Swiss banks take a lien on all assets of the client, in all its accounts. See [`docs/legal/venues/interactive-brokers.md`](docs/legal/venues/interactive-brokers.md#collateral-and-margin).
- **Not legal advice.** The legal analysis is research, not legal advice. See [`docs/legal/README.md`](docs/legal/README.md#open-legal-questions).
