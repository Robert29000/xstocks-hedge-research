# Interactive Brokers

Checked on 2026-10-19. Collateral section checked on 2026-11-04. Status: **Kept**. Strategies: A, B, C. Back to the [index](../README.md).

Numbers (rates and fees) are in [`hedge_research.ipynb`](../../../hedge_research.ipynb), in the venue tables for each strategy.

## Legal entity and regulator

- IBKR assigns an entity account to an IBKR company by the **country of formation** of the entity. Source: <https://ibkb.interactivebrokers.com/es/node/1000>. CONFIRMED.
- For a Jersey company, the probable entity is **Interactive Brokers (U.K.) Limited** (FCA). Interactive Brokers LLC (SEC, FINRA, CFTC) carries US trades and custody. Jersey is not in the EU/EEA, so IBKR Ireland is unlikely. Source: <https://www.interactivebrokers.co.uk/de/accounts/forms-and-disclosures-services-guide.php>. UNCONFIRMED.
- Both entities are regulated in jurisdictions that the Jersey FSC counterparty rule allows (UK, US).

## Onboarding a Jersey corporate

- IBKR classifies organisations as "Institutional". IBKR Lite is not available to them, so IBKR Pro pricing applies. Source: <https://www.interactivebrokers.com/en/trading/margin-rates.php>. CONFIRMED.
- The issuer will probably need a W-8BEN-E form, an LEI, corporate documents, and beneficial-owner documents. UNCONFIRMED.

## Products for each strategy

| Strategy | Product | Legal notes |
|---|---|---|
| A | USD margin loan against the account | The loan needs collateral in the IBKR account. IBKR gives no loan without collateral. The pledged xStocks shares at Alpaca cannot serve as this collateral. See [Margin loans](#margin-loans-strategy-a). |
| B | CME single stock futures, Eurex single stock futures, CME E-mini index futures | The margin must be cash. See [Collateral and margin](#collateral-and-margin). IBKR access to CME single stock futures is UNCONFIRMED. CME does not list IBKR on its broker page: <https://www.cmegroup.com/trading/where-to-trade-single-stock-futures.html>. Eurex single stock futures are on IBKR. |
| C | US listed equity options (OCC) | Standard US options approval. A non-US corporate needs an options trading level. |

## Collateral and margin

The research for these points was done on 2026-11-04. The margin values are in section 4.2 of the notebook.

| Point | Finding | Status | Source |
|---|---|---|---|
| Form of futures margin | Cash only, in the commodities segment of the account. "Cash remains the only asset eligible to be transferred between the two [segments]." | CONFIRMED | <https://www.interactivebrokers.com/lib/cstools/faq/#/content/1112354345> |
| Shares or T-bills as futures margin | Not possible directly. They have loan value only in the securities segment. Cash that comes from a margin loan is a loan with interest. | UNCONFIRMED | Same FAQ |
| Interest on margin cash | "Interest is not paid on cash held in the commodities segment of an account." | CONFIRMED | <https://www.interactivebrokers.com/lib/cstools/faq/#/content/42714991> |
| Variation margin | Cash only. IBKR checks the margin in real time. It sells positions without a margin call. | CONFIRMED | <https://www.interactivebrokers.com/en/accounts/configuring-your-account.php>, <https://www.interactivebrokers.com/campus/glossary-terms/margin-warning/> |
| Cash sweep | The automatic sweep of excess cash is not available for IB UK accounts. The issuer may have to move cash between the segments by hand. | CONFIRMED | <https://www.interactivebrokers.com/lib/cstools/faq/#/content/29080976> |
| Customer protection | CFTC segregation protects cash in the commodities segment. SIPC does not. | CONFIRMED | Cash sweep FAQ |

### Margin loans (strategy A)

Research on 2026-11-04. The collateral values are in section 4.1 of the notebook.

| Point | Finding | Status | Source |
|---|---|---|---|
| Collateral for a share purchase | The bought shares are the collateral (margin purchase). IBKR checks a Regulation T end-of-day requirement of 50% on long US stocks, also for UK and other non-US residents. Maintenance margin is 25%. | CONFIRMED | <https://www.interactivebrokers.co.uk/en/trading/margin-stocks.php?hm=uk&ex=us&rgt=1&rsk=0&pm=1&rst=101004040808>, <https://www.law.cornell.edu/cfr/text/12/220.12> |
| Loans without collateral | Not available. Every IBKR loan is a margin loan against the assets in the account. | CONFIRMED | Form 3066 §4.2.1: <https://www.interactivebrokers.com/Universal/servlet/Registration_v2.formSampleView?formdb=3066> |
| Portfolio margin | USD 110,000 equity to open, USD 100,000 to keep. Stocks: ±15% stress, 30% for large concentrated positions. Initial margin is 110% of maintenance. Available to UK and other residents for US stocks. Availability for a corporate account is UNCONFIRMED. | CONFIRMED | <https://www.interactivebrokers.co.uk/en/trading/margin-requirements.php> |
| T-bills as collateral | US Treasuries with less than 6 months to maturity need 1% margin. Less than 1 year: 2%. | CONFIRMED | <https://www.interactivebrokers.co.uk/en/trading/margin-bonds.php?hm=uk&ex=us&rgt=1&rsk=1&pm=1&rst=101004040808> |
| Minimum equity | USD 2,000 for a margin account | CONFIRMED | Same margin pages |
| Interest period | "Only settled money is considered for interest rate purposes." USD uses a 360-day year. Each account is tiered on its own, balances of several accounts are not combined. | CONFIRMED | <https://www.interactivebrokers.com/en/accounts/fees/pricing-interest-rates.php> |
| Dividends on shares bought on margin | IBKR may pay a "substitute payment in lieu of … dividends". Its tax treatment can differ from a dividend. | CONFIRMED (clause), UNCONFIRMED (allocation rules) | Form 3207 §A2.1.4: <https://www.interactivebrokers.com/Universal/servlet/Registration_v2.formSampleView?formdb=3207> |
| Margin calls | IBKR generally does not issue margin calls. It may sell positions at once and raise house margin at any time. | CONFIRMED | Form 3207 §D1.1.3, §D1.1.7 |

### Lien and rehypothecation

- The IB LLC customer agreement pledges all customer assets in the account to IB, with "a perfected first priority lien and security interest in IB's favor". The lien secures obligations "under this or any other Agreement". Source: <https://www.sec.gov/Archives/edgar/data/1948817/000194881723000011/IBKRClientAgreement_Official.txt> (Institutional Services Customer Agreement, 2022-12-20). CONFIRMED for IB LLC. The research did not get the IB UK agreement.
- The same agreement permits IB to "pledge, re-pledge, hypothecate or re-hypothecate Customer securities and assets" without notice. CONFIRMED.
- For an IB UK institutional client, all assets in all IB UK accounts are "pledged to the IBKR Group" with a first priority lien (Form 3207 §C4.1.1). IB LLC may return securities "other than the original" (§C3.1.1). IB LLC holds client assets under SEC rules, not FCA CASS rules (§C2.1.3–C2.1.4). CONFIRMED.
- SEC Rule 15c3-3 lets the broker use margin securities up to 140% of the client's debit. The rest must stay in the broker's control. Source: <https://www.law.cornell.edu/cfr/text/17/240.15c3-3>. CONFIRMED.
- Shares bought on margin become fully paid only when the loan is repaid. Only then can the issuer move them to the pledged account.
- **Result:** the backing shares at Alpaca, InCore Bank, and GTN are pledged to Security Agent Services AG. They must never go into an IBKR account. The IBKR lien would attach to them, and IBKR could rehypothecate them. Only free cash of the issuer can serve as margin.
- The IBKR lien also applies to the margin cash. Counsel must check that the programme terms permit the issuer to pledge free cash to a broker. Counsel must also check that this cash is not part of the secured assets of the token holders.
- The lien covers "any other Agreement". IBKR may treat sub-accounts "as separate or as one" for margin, and may merge accounts and set off balances without notice (Form 3207 §D1.1.2, §A13.1.1(iii)). IB UK and IB LLC each have a lien over the client's assets at the other (Form 3066 §6, §7.2.2). Thus a sub-account does not protect assets from the lien. A separate legal entity for the hedge does. CONFIRMED.
- **Possible precedent.** An ETP programme (IncomeShares / Leverage Shares) has a "Margin Account Agreement" with IB UK and IB LLC. Its text seems to remove the security-interest clause of the IBKR customer agreement in favour of a charge to a trustee. Status: UNCONFIRMED (search result only, the document link now redirects). Ask IBKR if it agrees to a similar carve-out.

## Open questions and contacts

1. Which IBKR entity onboards Backed Assets (JE) Limited? Contact IBKR Institutional Sales.
2. Does IBKR offer CME single stock futures (launched 2026-07-27)?
3. Does the issuer's prospectus permit derivatives? See [xstocks-issuer.md](../xstocks-issuer.md#hedging-permission).
4. Does IBKR agree to remove or limit its lien for an issuer account, as in the ETP precedent above?
5. What is the IBKR house margin for the new CME single stock futures?
