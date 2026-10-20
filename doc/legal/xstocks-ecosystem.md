# xStocks ecosystem

Checked on 2026-10-19. Back to the [index](README.md).

## Ownership

```
Payward, Inc. (US, Kraken)
  └── Payward Europe Limited (Ireland)          100%
        └── Backed Finance AG (Zug, CHE-410.125.970)   100%
              └── Backed Assets (JE) Limited (Jersey, issuer)
```

- Kraken announced the purchase of Backed Finance AG on 2 December 2025. Source: [Payward press release](https://www.payward.com/press-release/kraken-acquires-backed-xstocks-expansion), [Business Wire](https://www.businesswire.com/news/home/20251202666578/en).
- The current prospectus states: "The Parent is itself 100% owned by Payward Europe Limited, Ireland which is in turn 100% owned by Payward, Inc., US." CONFIRMED.
- A law-firm notice from 6 January 2026 reports the closing: [MME](https://www.mme.ch/en/magazine/deals/deal-announcement-kraken). The exact closing date is UNCONFIRMED.
- A services agreement with Payward, Inc. replaced the old agreement with Backed Finance AG on 5 January 2026. CONFIRMED (prospectus).
- "Neither PEL nor Payward have guaranteed the Issuer's obligations." CONFIRMED (prospectus).
- Documentation moved to <https://docs.xstocks.fi>. The API moved to <https://api.xstocks.fi>.

## Custodians and brokers

| Party | Role | Regulator | Status |
|---|---|---|---|
| Alpaca Securities LLC | Main custodian and broker for the underlying shares. Prime Borrower under the securities lending agreement. | SEC, FINRA, SIPC member | CONFIRMED (Kraken FAQ, prospectus) |
| Alpaca Crypto LLC | US custodian named in the prospectus | FinCEN (MSB registration) | CONFIRMED (prospectus) |
| InCore Bank AG, Schlieren | Swiss custodian. Kraken calls it a "secondary custodian". | FINMA bank licence | CONFIRMED |
| Maerki Baumann & Co. AG | Broker named on product pages. It executes all securities orders through InCore Bank. | FINMA bank licence | CONFIRMED (product page, Maerki execution policy) |
| GTN Europe Financial Services Limited | UK custodian | FCA, firm reference 1003343 | CONFIRMED (prospectus) |

Kraken FAQ: "Underlying shares are held by Alpaca Securities LLC (FINRA-regulated, SIPC member)… InCore Bank is a secondary custodian."

Securities lending: "Alpaca Securities LLC acts as Prime Borrower according to the Securities Lending Agreement." The Final Terms of each product must permit lending. Each loan must be "fully collateralized on a daily mark-to-market basis".

## Security agent and collateral

- "Security Agent Services AG, Baarerstrasse 75, 6300 Zug, Switzerland will act as the Security Agent." CONFIRMED.
- The collateral is a Swiss pledge, or a US or UK securities account control agreement, depending on where the custodian is.
- **Result for strategy A:** the custodian holds the underlying shares under a pledge for the token holders. The issuer cannot pledge the same shares again for a Lombard loan without legal review (inference, UNCONFIRMED).

## Multiplier mechanism

Source: <https://docs.xstocks.fi/docs/dividends-and-stock-splits>

> "When a company pays a dividend, the custodian receives the cash on behalf of all shares held in custody." … "Rather than distributing cash, the dividend is reinvested into additional shares of the same stock."
>
> "The multiplier tracks the cumulative effect of all corporate events over the life of the token."

- Each token starts with multiplier 1.0.
- A cash dividend increases the multiplier by `net dividend / reference price`.
- "Dividends are reinvested net of applicable withholding taxes."

### Activation time: three sources disagree

| Source | Statement |
|---|---|
| xStocks docs | "Activation is set for 00:30 UTC on the day immediately following the Ex-Date" |
| Kraken FAQ | "approximately 8:00 PM EST on the day prior to the Ex-Date" |
| xStocks API data | Before about May 2026: activation on the evening of the **payment date**. From about May 2026: activation on the evening **before the ex-date**. |

The `fetch_data.py` output supports the API reading. The multiplier step lets you calculate the reference price: `net dividend / (multiplier_new / multiplier_old − 1)`.

- For events that activate before the ex-date, the reference price is the close on the trading day before the ex-date. Example: AAPLx, 2026-08-10 ex-date, reference price 313.33. This is the AAPL close on 2026-08-07.
- For events that activate on the payment date, the reference price is the close on the payment date. Example: AAPLx, 2025-08-14 payment date, reference price 232.78. This is the AAPL close on 2025-08-14.

**Result:** under the old rule (payment date), the issuer bought the shares at the same price that set the multiplier. It had no price risk. Under the new rule (ex-date), the multiplier uses the close before the ex-date, but the cash arrives on the payment date. The issuer carries the price risk for the full gap. No public document states who carries this risk. The research infers that the issuer carries it.

The xStocks docs tell venues to pause trading around the activation time (for example ±15 minutes).

## Token contracts

Source: <https://docs.xstocks.fi/developers/multipliers>, <https://github.com/backed-fi/backed-token-contract>

| Chain | Standard | Multiplier |
|---|---|---|
| Ethereum and other EVM chains (Arbitrum, Mantle, Ink, BNB Chain, Optimism, HyperEVM, Monad, XLayer) | `BackedTokenProxy` (EIP-1967) to `BackedAutoFeeTokenImplementation` | `multiplier()`, `newMultiplier()`, `newMultiplierActivationTime()`, `getCurrentMultiplier()` |
| Solana | SPL Token-2022 with the Scaled UI Amount extension | `scaledUiAmountConfig.multiplier`, `newMultiplier`, `newMultiplierEffectiveTimestamp` |
| TON | TEP-0526 | `get_display_multiplier` |
| Tron | Listed in the API deployments | Not checked |

- AAPLx has the same EVM address on all EVM chains: `0x9d275685dc284c8eb1c79f6aba7a63dc75ec890a`. Solana mint: `XsbEhLAtcf6HdfpFZ5xEMdqW8nfAvcsP5bdudRLJzJp`.
- Only the `multiplierUpdater` role can call `updateMultiplierValue(...)` and `updateMultiplierWithNonce(...)`. The owner sets that role.
- Events: `MultiplierScheduled(newMultiplier, activationTime)`, `MultiplierUpdated(value)`, `MultiplierScheduleOverridden(...)`, `NewMultiplierUpdater`.
- The contract also has a periodic fee (`feePerPeriod`, `periodLength`) that can change the multiplier. It is UNCONFIRMED whether the fee is above zero for xStocks.

## Public API

Base URL: `https://api.xstocks.fi/api/v2/public`. No key is necessary. Spec: <https://docs.xstocks.fi/apis/openapi>.

| Endpoint | Use in this project |
|---|---|
| `/assets` | xStock symbol to underlying symbol, listing venue (MIC) |
| `/corporate-actions/history` | Cash-dividend events with multipliers, gross and net amounts, withholding rate |
| `/assets/{symbol}/multiplier/history?network=...` | Cross-check of multiplier history |

The API has no ex-date or payment date. `fetch_data.py` gets these dates from Nasdaq and stockanalysis.com. See the project [README](../../README.md).
