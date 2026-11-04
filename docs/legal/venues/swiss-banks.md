# Swiss banks: InCore Bank and Maerki Baumann

Checked on 2026-10-19. Status: **Kept, terms not public**. Strategy: A. Back to the [index](../README.md).

Numbers are in [`hedge_research.ipynb`](../../../hedge_research.ipynb). The notebook uses a public Swiss Lombard rate (Swissquote) as a benchmark, because neither bank publishes its terms.

## Legal entities and regulators

| Bank | Regulator | Role for xStocks | Status |
|---|---|---|---|
| InCore Bank AG, Schlieren/Zurich | FINMA bank licence. FINMA approval (2020) for digital assets. | Swiss custodian ("secondary custodian") | CONFIRMED |
| Maerki Baumann & Co. AG, Zurich | FINMA bank licence. Crypto services under the ARCHIP brand. | Broker named on product pages | CONFIRMED |

- Maerki Baumann executes all securities orders through InCore: "Derzeit ist dies die InCore Bank AG, Zürich." Source: <https://www.maerki-baumann.ch/de/ausfuehrungsgrundsaetze>. CONFIRMED. For the hedge, the two banks are one execution path.
- InCore is a business-to-business bank. It serves banks, intermediaries, asset managers, and companies. Source: <https://www.incore.ch/de/bank/unternehmen/faq/>. CONFIRMED.
- The InCore FAQ says that the website is for Swiss legal entities only. Terms for a Jersey company can be different.
- Ownership: SOBACO holds the InCore majority. Maerki Baumann Holding keeps a minority stake. Source: <https://www.moneycab.com/it/sobaco-und-incore-gemeinsam-in-die-zukunft/amp/>. One source only, possibly old.

## Products for each strategy

| Strategy | Product | Legal notes |
|---|---|---|
| A | Lombard loan or overdraft | Neither bank's website mentions Lombard credit. InCore's 2025 interest result was only CHF 0.43m, so lending is not a main business. The xStocks shares are pledged to the security agent and cannot be pledged again without legal review. |
| B | Futures through the bank | Not mentioned. InCore lists equities and bonds on more than 100 exchanges, but no exchange-traded derivatives. Source: <https://www.incore.ch/de/bank/loesungen/markets/>. |
| C | Listed options through the bank | Not mentioned. |

## Benchmark for strategy A

The notebook uses Swissquote's published USD Lombard rate as a Swiss benchmark: <https://www.swissquote.com/de-lu/private/trade/products/securities/lombard-loan>. Swissquote is a FINMA-regulated Swiss bank. It is not an xStocks counterparty.

## Open questions and contacts

1. Ask InCore (services@incorebank.ch, +41 44 403 93 00) for its institutional fee schedule and credit lines for Backed Assets (JE) Limited.
2. Ask if InCore can give access to Eurex, CME, or OCC options.
3. Ask legal counsel if a short credit line against non-pledged assets is possible.
