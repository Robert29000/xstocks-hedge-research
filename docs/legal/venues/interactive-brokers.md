# Interactive Brokers

Checked on 2026-10-19. Status: **Kept**. Strategies: A, B, C. Back to the [index](../README.md).

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
| A | USD margin loan against the account | The loan needs collateral in the IBKR account. The pledged xStocks shares at Alpaca cannot serve as this collateral. |
| B | CME single stock futures, Eurex single stock futures, CME E-mini index futures | IBKR access to CME single stock futures is UNCONFIRMED. CME does not list IBKR on its broker page: <https://www.cmegroup.com/trading/where-to-trade-single-stock-futures.html>. Eurex single stock futures are on IBKR. |
| C | US listed equity options (OCC) | Standard US options approval. A non-US corporate needs an options trading level. |

## Open questions and contacts

1. Which IBKR entity onboards Backed Assets (JE) Limited? Contact IBKR Institutional Sales.
2. Does IBKR offer CME single stock futures (launched 2026-07-27)?
3. Does the issuer's prospectus permit derivatives? See [xstocks-issuer.md](../xstocks-issuer.md#hedging-permission).
