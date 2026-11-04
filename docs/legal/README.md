# Legal and regulatory context

This folder holds the legal context for the hedge research. The numbers (rates, fees, margins) are in [`hedge_research.ipynb`](../../hedge_research.ipynb). These files explain who the parties are, which rules apply, and which venues the issuer can use.

All facts were checked on **2026-10-19**. Each fact has a source link and a status:

- **CONFIRMED**: a primary source (prospectus, regulator, venue's own page) states the fact.
- **UNCONFIRMED**: only a secondary source states it, or the research inferred it. Check it before you rely on it.

## Files

| File | Content |
|---|---|
| [xstocks-issuer.md](xstocks-issuer.md) | The issuer, the product, the prospectus, the dividend clauses, and the counterparty rule |
| [xstocks-ecosystem.md](xstocks-ecosystem.md) | Owners, custodians, security agent, multiplier mechanism, and token contracts |
| [venues/interactive-brokers.md](venues/interactive-brokers.md) | Interactive Brokers |
| [venues/alpaca.md](venues/alpaca.md) | Alpaca Securities (current custodian and broker) |
| [venues/swiss-banks.md](venues/swiss-banks.md) | InCore Bank, Maerki Baumann, and a Swiss Lombard benchmark |
| [venues/eurex.md](venues/eurex.md) | Eurex single stock futures and total return futures |
| [venues/cme.md](venues/cme.md) | CME single stock futures, index futures, and US listed options (OCC) |
| [venues/kraken-payward.md](venues/kraken-payward.md) | Kraken and Payward group venues (xStocks perps, Bitnomial) |
| [venues/saxo.md](venues/saxo.md) | Saxo Bank (excluded) |

## How the venues were filtered

The issuer is Backed Assets (JE) Limited, a Jersey company. It has no licence. Its Jersey consent sets a rule for its brokers and prime borrowers. They must be "reputable financial services companies subject to the appropriate regulation". The regulation must come from the EU, Jersey, the UK, or another jurisdiction that is not on the Jersey FSC high-risk list. See [xstocks-issuer.md](xstocks-issuer.md#counterparty-rule).

The research used three filters:

1. The venue or broker must be regulated in an allowed jurisdiction.
2. The venue must accept a Jersey corporate client.
3. The venue must offer at least one of the three strategies: (A) financing, (B) long futures, (C) call options.

## Summary

| Venue | Entity for the issuer | Regulator | Accepts a Jersey corporate | Strategies | Status |
|---|---|---|---|---|---|
| Interactive Brokers | Interactive Brokers (U.K.) Ltd (UNCONFIRMED) | FCA (UK), SEC/FINRA (US carrying broker) | Probably yes (UNCONFIRMED) | A, B, C | Kept |
| Alpaca Securities | Alpaca Securities LLC | SEC, FINRA, SIPC | Yes, it is the current custodian | A, C | Kept |
| InCore Bank / Maerki Baumann | InCore Bank AG | FINMA (CH) | Yes, it is a current custodian | A (if offered) | Kept, terms not public |
| Eurex | Through a clearing member or a broker | BaFin / Hessian exchange authority (DE) | Through the broker | B (C with FX risk) | Kept |
| CME Group | Through a CFTC-registered FCM | CFTC (US) | Through the FCM | B, C (index options) | Kept |
| US listed options (OCC) | Through a US broker-dealer | SEC, FINRA | Through the broker | C | Kept |
| Kraken xStocks perps | Payward Digital Solutions Ltd | BMA (Bermuda) | Probably yes | B | Conditional |
| Kraken EU futures | Payward Europe Digital Solutions (CY) Ltd | CySEC (MiFID II) | Probably yes | B (index only) | Kept |
| Saxo Bank | None | FSA (DK) | No, Saxo stopped Jersey onboarding in 2024 | A, B, C | Excluded |
| On-chain perps (for example Hyperliquid) | None | None | Not applicable | B | Excluded, no regulation |

## Open legal questions

1. The prospectus has no clause that permits the issuer to use derivatives for hedging. The issuer may need a prospectus supplement or Jersey FSC consent before it uses strategies B or C. A group company (for example a Payward entity) could also do the hedge instead of the issuer.
2. The underlying shares are pledged to the security agent for the token holders. The issuer cannot use them as collateral for a loan without legal review. This limits strategy A to unsecured credit or credit against other assets.
3. Bermuda is not in the EU, UK, or Jersey. Kraken xStocks perps are valid only if Bermuda is not on the Jersey FSC high-risk list. Check the current list.
4. All Payward-group venues are related parties of the issuer. This adds a concentration and conflict-of-interest risk.
