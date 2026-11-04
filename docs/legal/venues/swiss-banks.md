# Swiss banks: InCore Bank and Maerki Baumann

Checked on 2026-10-19. Collateral section checked on 2026-11-04. Status: **Kept, terms not public**. Strategy: A. Back to the [index](../README.md).

Numbers are in [`hedge_research.ipynb`](../../../hedge_research.ipynb). The notebook uses public Lombard rates (Swissquote) as a benchmark, because neither bank publishes its terms.

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
| A | Lombard loan or overdraft | InCore does no lending business (2025 annual report). Maerki Baumann gives Lombard loans to private clients against diversified portfolios. The xStocks shares are pledged to the security agent and cannot be pledged again without legal review. See [Collateral and lien](#collateral-and-lien). |
| B | Futures through the bank | Not mentioned. InCore lists equities and bonds on more than 100 exchanges, but no exchange-traded derivatives. Source: <https://www.incore.ch/de/bank/loesungen/markets/>. |
| C | Listed options through the bank | Not mentioned. |

## Benchmark for strategy A

The notebook uses two published Swissquote USD Lombard rates. Swissquote is not an xStocks counterparty.

| Entity | Regulator | Rate | Source | Status |
|---|---|---|---|---|
| Swissquote Bank Europe SA | CSSF (Luxembourg) | 1-month average SOFR + 1.95%. Loan-to-value up to 80% of eligible assets. | <https://www.swissquote.com/de-lu/private/trade/products/securities/lombard-loan> | CONFIRMED |
| Swissquote Bank Ltd, Gland | FINMA (Switzerland) | USD 6.923% (2026-11-04). No minimum loan or portfolio. | <https://www.swissquote.com/en-ch/private/trade/products/securities/lombard-loan> | CONFIRMED |

- The earlier version of this file called the Luxembourg page a FINMA bank. That was wrong. Luxembourg is in the EU, so the FSC counterparty rule allows both entities.
- Swissquote Bank Ltd collateralised loan agreement (05-2025): <https://library.swissquote.com/cdn/2958/ql/sqb-collateralised-loan-agreement-en.pdf>. CONFIRMED:
  - The bank alone sets which assets are eligible and their collateral value. It does not have to explain the method (§2.2, §5.1).
  - Interest only on the amount used. Day count 30/360 (§4.2). No commitment fee.
  - The credit has no end date. Either party can end it with immediate effect.
  - A purchase that cash does not cover becomes a loan, and the bought securities are pledged automatically (§3.1, §6.1).
  - The client warrants that the account is free of third-party pledges, at each drawdown (§8.1(a)).
- Lombard loans for legal entities and for a Jersey company: UNCONFIRMED. The CHF 0% promotion excludes "businesses and other legal entities", so legal entities can be Swissquote clients.

## Collateral and lien

Research on 2026-11-04. The collateral values are in section 4.1 of the notebook.

| Point | Finding | Status | Source |
|---|---|---|---|
| InCore lending | "Die Bank betreibt kein Kreditgeschäft." The client receivables (CHF 12.7m) are unsecured relationships with financial service providers. | CONFIRMED | <https://www.incore.ch/fileadmin/incore/news/bank/documents/incore-bank-geschaeftsbericht-2025-de.pdf> (p. 26) |
| Maerki Baumann lending | Lombard loans for private clients against diversified portfolios, with "vorsichtige Belehnungssätze". Unsecured credit only in exceptional cases. Secured client loans CHF 82.8m. | CONFIRMED | <https://www.maerki-baumann.ch/system/files/2026-04/Maerki-Baumann-Privatbank-Zuerich_Geschaeftsbericht-2025_0.pdf> (p. 32–33) |
| Example loan-to-value | Diversified equities up to 60%, high-quality bonds up to 90%, cash up to 95% (Piguet Galland) | CONFIRMED | <https://www.piguetgalland.ch/hubfs/Factsheet%20cr%C3%A9dit%20lombard_EN_new.pdf> |
| Loan-to-value for one stock | No bank publishes it. Banks require diversification (Cornèr, UBS, LUKB, Maerki Baumann). | UNCONFIRMED | <https://www.corner.ch/export/sites/cornerbancaCH/.galleries/pdf/de/FIDLEG/Lombardkredite.pdf> |
| Regulatory haircut | Basel framework: 20% for main-index equities, 0.5% for AAA–AA government paper up to 1 year | CONFIRMED | <https://www.bis.org/committees/bcbs/basel-framework/standard/cre/22/inforce/2023-01-01/published/2020-11-26> |
| Loan form for short periods | A current-account credit line fits best. Fixed advances need at least CHF 100k and run 1 to 12 months or longer. | CONFIRMED | <https://moneyland.ch/en/swiss-lombard-loans-trading-compared> |

**Lien.**

- Swiss bank terms give the bank a lien and a right of set-off over all assets of the client at the bank. Banks may treat all accounts of a client as one (Swissquote §1.2, §6). CONFIRMED. Source: <https://ubs.com/contractualterms-corporates>, Swissquote loan agreement.
- Under the Swiss Federal Intermediated Securities Act (FISA) Art. 30(2), a custodian that signs a control agreement for a secured party without an express reservation of its own earlier rights ranks behind that party. Source: <https://www.droit-bilingue.ch/en-it/9/95/957.1-30-37.html>. CONFIRMED (statute).
- Market practice is a written waiver or subordination by the account bank, and notice to the bank. Source: <https://gpg-pdf.chambers.com/banking-and-finance-2025/610/>. CONFIRMED.
- **Result:** InCore holds the backing shares under a pledge for the security agent. A loan for the hedge at a different bank avoids the conflict. At the same bank, the issuer needs a written carve-out signed by the bank and the security agent.

## Open questions and contacts

1. Ask InCore (services@incorebank.ch, +41 44 403 93 00) for its institutional fee schedule and credit lines for Backed Assets (JE) Limited.
2. Ask if InCore can give access to Eurex, CME, or OCC options.
3. Ask legal counsel if a short credit line against non-pledged assets is possible.
4. Ask Maerki Baumann or Swissquote if they give a Lombard credit line to a Jersey company, and the loan-to-value for one US stock.
