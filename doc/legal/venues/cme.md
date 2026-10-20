# CME Group and US listed options

Checked on 2026-10-19. Status: **Kept**. Strategies: B, C. Back to the [index](../README.md).

Numbers (fees, margins, implied financing) are in [`hedge_research.ipynb`](../../../hedge_research.ipynb), in the strategy B and C venue tables.

## Legal entities and regulators

- CME (Chicago Mercantile Exchange Inc.) is a CFTC-designated contract market. CME Clearing is a CFTC-registered derivatives clearing organization. The US is allowed under the Jersey FSC counterparty rule because it is not on the higher-risk list.
- US listed equity options clear through the Options Clearing Corporation (OCC), regulated by the SEC and CFTC. Exchanges: Cboe, MIAX, BOX, Nasdaq, and others.

## Onboarding a Jersey corporate

- **Futures:** the issuer needs a CFTC-registered futures commission merchant (FCM). Another option is a non-US broker that clears through an FCM in an omnibus account (CFTC Regulation 3.10 exemption). Source: <https://www.nfa.futures.org/registration-membership/who-has-to-register/exempt-foreign-firms.html>.
- **Single stock futures** are "security futures". The broker must be registered as both broker-dealer and FCM, or be a notice-registered FCM. No rule bars a Jersey corporate. Full SEC and CFTC KYC applies. UNCONFIRMED in detail.
- **US listed options:** the issuer needs a US broker-dealer with OCC clearing (for example Interactive Brokers or Alpaca). Expect a W-8BEN-E form. UNCONFIRMED.

## Products for each strategy

| Strategy | Product | Legal and design notes |
|---|---|---|
| B | CME single stock futures (launched 2026-07-27) | 55 standard contracts (100 shares) and 22 micro contracts (10 shares) on more than 50 US large caps, including AAPL and NVDA. Cash settlement. Quarterly expiry. Regular cash dividends are not adjusted, so the price includes them. Sources: <https://www.cmegroup.com/media-room/press-releases/2026/6/30/cme_group_to_launchsinglestockfuturesonjuly27.html>, <https://www.cmegroup.com/articles/faqs/faq-single-stock-futures.html>, <https://www.cmegroup.com/rulebook/CME/VI/701/701.pdf>. |
| B | E-mini and Micro E-mini S&P 500 and Nasdaq-100 futures | Use for SPYx and QQQx only. They track the index, not the ETF, so a small tracking error remains. BTIC trades fix the price at the index close. Source: <https://www.cmegroup.com/btic>. |
| C | E-mini S&P 500 options | Expiries every business day for about 5 weeks. Source: <https://www.cmegroup.com/trading/equity-index/files/es-options-product-codes-and-listing-calendar.pdf>. |
| C | US single stock and ETF options (OCC) | 100 shares per contract. Weekly expiries on Monday, Wednesday, and Friday for large names (AAPL, NVDA, MSFT, AMZN, GOOGL, META, TSLA, and others). Source: <https://www.miaxglobal.com/alert/2026/07/01/miax-exchange-group-options-markets-listing-monday-and-wednesday-weekly>. |

## Design limits

- CME single stock futures expire quarterly. The hedge must be closed before expiry, which leaves basis risk on the close date.
- Options with weekly expiries can match the payment date closely for large names.
- CME lists no single stock futures on SPY or QQQ. UNCONFIRMED.

## Open questions

1. Which FCM can onboard the issuer and gives access to CME single stock futures?
2. Exchange fees for CME single stock futures are in Exhibit 2 of SER 9974: <https://www.cmegroup.com/notices/ser/2026/06/ser-9974.pdf>. The research could not read this file. UNCONFIRMED.
3. Does the issuer's prospectus permit derivatives? See [xstocks-issuer.md](../xstocks-issuer.md#hedging-permission).
