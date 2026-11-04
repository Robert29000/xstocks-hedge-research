# Kraken and the Payward group

Checked on 2026-10-19. Status: **Conditional** (xStocks perps), **Kept** (EU index futures), **Reference only** (margin). Strategies: A, B. Back to the [index](../README.md).

Numbers (funding, fees, leverage) are in [`hedge_research.ipynb`](../../../hedge_research.ipynb), in the strategy A and B venue tables.

## Related-party note

Payward, Inc. owns the issuer through Payward Europe Limited and Backed Finance AG. Each venue on this page is a related party of the issuer. A hedge with a group company adds concentration risk and a conflict of interest. An intercompany loan or intercompany hedge needs an arm's-length agreement.

## Legal entities and regulators

| Entity | Regulator | Products | Allowed by the FSC counterparty rule | Source |
|---|---|---|---|---|
| Payward Digital Solutions Ltd (PDSL) | Bermuda Monetary Authority (digital asset business licence) | xStocks perpetual futures | Only if Bermuda is not on the Jersey FSC high-risk list. UNCONFIRMED. | <https://blog.kraken.com/product/xstocks/tokenized-equity-perpetual-futures> |
| Payward Europe Digital Solutions (CY) Ltd | CySEC (MiFID II) | About 70 futures on equity indices, commodities, and FX (since 2026-03-16) | Yes (EU) | <https://www.financemagnates.com/cryptocurrency/cysec-regulated-kraken-unit-adds-futures-tied-to-equities-commodities-fx/> |
| Payward Europe Solutions Ltd | Central Bank of Ireland (MiCA CASP, since 2025-06-25) | Crypto services | Yes (EU) | <https://www.businesswire.com/news/home/20250625529871/en> |
| Bitnomial (purchased about May 2026) | CFTC (DCM, DCO, FCM) | 16 crypto perps. Single stock perps filed about 2026-09-18, approval pending. | Yes (US) | <https://www.theblock.co/post/399851/kraken-parent-payward-completes-bitnomial-acquisition>, <https://cointelegraph.com/news/kalshi-joins-coinbase-with-filing-for-us-stock-perpetual-futures> |
| NinjaTrader Clearing LLC (Kraken Derivatives US) | CFTC FCM, NFA member | US futures | Yes (US) | <https://support.kraken.com/articles/us-perpetual-futures> |

## Products for each strategy

| Strategy | Product | Legal and design notes |
|---|---|---|
| A | Intercompany loan from Payward | Terms are not public. Needs an arm's-length agreement. |
| A | Kraken spot margin | Very expensive (rollover fee every 4 hours). Reference only. |
| A | Kraken Prime credit facilities | Institutional asset-backed lending. Terms not public. UNCONFIRMED. Source: <https://www.theblock.co/post/356720/kraken-launches-full-service-prime-brokerage-institutional-crypto-clients>. |
| B | xStocks perps (since 2026-02-24) | Underlyings include SPYx, QQQx, NVDAx, AAPLx, GOOGLx, TSLAx, AMZNx, METAx. Not available in the US, Canada, the UK, or Australia. The reference price is the xStocks index. This index uses on-chain xStock trading outside US market hours, so the hedge partly references the issuer's own token. Dividend treatment in the perp is UNCONFIRMED. Source: <https://support.kraken.com/articles/4844359082772-linear-multi-collateral-derivatives-contract-specifications>. |
| B | EU index futures (CySEC) | S&P 500 and Nasdaq-100 only. Useful for SPYx and QQQx. |
| C | None | Kraken offers no xStocks options. |

## Open questions

1. Is Bermuda on the Jersey FSC higher-risk jurisdiction list?
2. Can the issuer, as a group company, use PDSL perps, or is an intercompany hedge better?
3. How does the perp handle the multiplier change on the ex-date? The Kraken page contradicts itself.
