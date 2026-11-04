# Kraken and the Payward group

Checked on 2026-10-19. Strategy A section checked on 2026-11-04. Status: **Conditional** (xStocks perps), **Kept** (EU index futures), **Excluded** (spot margin). Strategies: A, B. Back to the [index](../README.md).

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
| A | Intercompany loan from Payward | Terms are not public. Needs an arm's-length agreement. See [Strategy A at Payward venues](#strategy-a-at-payward-venues). |
| A | Kraken spot margin | Cannot fund a purchase of real US shares. Excluded. See [Strategy A at Payward venues](#strategy-a-at-payward-venues). |
| A | Kraken Prime credit facilities (OTC lending) | Collateral is BTC or ETH only. Minimum USD 500,000. Excluded. |
| B | xStocks perps (since 2026-02-24) | Underlyings include SPYx, QQQx, NVDAx, AAPLx, GOOGLx, TSLAx, AMZNx, METAx. Not available in the US, Canada, the UK, or Australia. The reference price is the xStocks index. This index uses on-chain xStock trading outside US market hours, so the hedge partly references the issuer's own token. Dividend treatment in the perp is UNCONFIRMED. Source: <https://support.kraken.com/articles/4844359082772-linear-multi-collateral-derivatives-contract-specifications>. |
| B | EU index futures (CySEC) | S&P 500 and Nasdaq-100 only. Useful for SPYx and QQQx. |
| C | None | Kraken offers no xStocks options. |

## Strategy A at Payward venues

Research on 2026-11-04.

| Point | Finding | Status | Source |
|---|---|---|---|
| Kraken spot margin: assets | Margin covers "Digital Assets or Fiat Balances" only. The only stock-like assets are xStocks. Real US shares are not available. | CONFIRMED | <https://www.kraken.com/legal/global-terms> (Annex A) |
| Kraken spot margin: withdrawal | Collateral and margin positions are locked while margin is open. The borrowed USD cannot go to an outside broker. | CONFIRMED | <https://support.kraken.com/articles/204585998> |
| Kraken spot margin: fees | Opening fee and rollover fee 0.025% to 0.05% per 4 hours for USD | CONFIRMED | <https://www.kraken.com/features/fee-schedule> |
| Kraken spot margin: leverage | xStocks pairs 3x. Crypto pairs up to 5x, 10x, or 20x by pair. | CONFIRMED | <https://blog.kraken.com/product/xstocks/introducing-xstocks-margin-trading-on-kraken-pro> |
| Kraken spot margin: entity | Payward Trading Ltd (British Virgin Islands) for clients outside Canada, the EEA, and Brazil. That Jersey falls under this entity is UNCONFIRMED. | CONFIRMED | <https://www.kraken.com/legal/global-terms> |
| Kraken stock trading | "Business accounts are not eligible." Only individuals in some US states and EEA countries. | CONFIRMED | <https://support.kraken.com/articles/unlock-stocks-trading-on-kraken-pro> |
| Kraken Prime OTC lending | Payward Oceanic Ltd lends against BTC or ETH only. Minimum USD 500,000. Loan-to-value set by the OTC desk. Its jurisdiction and regulator are not published. | CONFIRMED | <https://www.kraken.com/institutions/otc-lending> |
| Bitnomial, NinjaTrader Clearing | CFTC futures firms. No stock margin loans found. | UNCONFIRMED (no evidence found) | <https://ninjatrader.com/getmedia/e75aec7b-7efc-488b-954a-b81c9dac7d9b/NinjaTrader-Clearing-LLC-Disclosure-Document-2026-05-06.pdf> |
| Payward Europe Digital Solutions (CY) Ltd | The MiFID passport includes ancillary service B2 "Granting credits" (from 2025-09-01). No public margin or loan product. Its stock service excludes business accounts. | CONFIRMED | <https://www.fsma.be/en/party/payward-europe-digital-solutions-cy-ltd> |
| Earlier parent funding of the issuer | Shareholder loans of USD 6,075,434.74 at 2025-12-31, under the heading "Subordinated Shareholder Loan" | CONFIRMED | Base prospectus §3.1.1.8, §3.9.2. See [xstocks-issuer.md](../xstocks-issuer.md#funding-and-borrowing). |

- **Result:** no Kraken or Payward venue can fund a purchase of real US shares for the issuer. Only an intercompany loan is possible. Its terms are not public.
- **Jersey FSC higher-risk list** (Appendix D2, revised 2026-10-30): the British Virgin Islands are on the list. Bermuda, the US, Cyprus, and Ireland are not. Source: <https://www.jerseyfsc.org/industry/financial-crime/amlcftcpf-handbooks/appendix-d2-countries-and-territories-identified-as-presenting-higher-risks>. CONFIRMED. Thus Payward Trading Ltd (BVI) fails the counterparty rule, and PDSL (Bermuda) passes the list test.
- A holding company such as Payward, Inc. may not count as a "reputable financial services company" under the FSC rule. The earlier shareholder loans suggest that the rule did not block them. Ask counsel.

## Collateral for the perps

- Kraken accepts USD and EUR cash, stablecoins, crypto, and 10 xStocks as collateral, with haircuts. Source: <https://blog.kraken.com/product/xstocks/eligible-as-collateral-for-futures-and-margin>. CONFIRMED.
- The issuer must not post its own xStocks as collateral. That gives a circular exposure and can conflict with the token terms. ASSUMPTION, check with counsel.
- An exchange holds the collateral at PDSL, not a regulated clearing house.

## Open questions

1. ~~Is Bermuda on the Jersey FSC higher-risk jurisdiction list?~~ No. Bermuda is not on Appendix D2 (revised 2026-10-30). See [Strategy A at Payward venues](#strategy-a-at-payward-venues).
2. Can the issuer, as a group company, use PDSL perps, or is an intercompany hedge better?
3. How does the perp handle the multiplier change on the ex-date? The Kraken page contradicts itself.
