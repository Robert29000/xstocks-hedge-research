# Eurex

Checked on 2026-10-19. Status: **Kept**. Strategy: B (C with currency risk). Back to the [index](../README.md).

Numbers (fees, margins, contract sizes) are in [`hedge_research.ipynb`](../../../hedge_research.ipynb), in the strategy B venue table.

## Legal entity and regulator

- Eurex Deutschland is a German public-law exchange. Eurex Clearing AG is the central counterparty. The Hessian exchange supervisory authority and BaFin supervise them. Both are in the EU, so the Jersey FSC counterparty rule allows them.
- The issuer cannot trade on Eurex directly. It needs an Eurex exchange participant and a clearing member, or a broker such as Interactive Brokers. Source: <https://www.interactivebrokers.ie/en/trading/lp-eurex-benchmark-derivatives.php>.

## Onboarding a Jersey corporate

- Eurex restricts some products for US persons. Source: <https://www.eurex.com/ex-en/find/circulars/circular-2831492>. The issuer is a Jersey company, so these restrictions probably do not apply. Check with the broker. UNCONFIRMED.
- The broker (not Eurex) does the client onboarding. See [interactive-brokers.md](interactive-brokers.md).

## Products for each strategy

| Strategy | Product | Legal and design notes |
|---|---|---|
| B | Single stock futures on 114 US underlyings (for example AAPH, MSTF, NVDF, TSLG) | USD, 100 shares, cash settlement. Monthly expiry only (3rd Friday). The final settlement price is the NYSE or Nasdaq opening auction price. Source: <https://www.eurex.com/ex-en/markets/equ/fut/NVIDIA-3609684>. |
| B | USD Equity Total Return Futures on 73 US stocks (since 2026-02-23) | Funding is an overnight rate plus a traded spread. Dividends pass through net of withholding tax by a STOXX dividend index. Source: <https://www.eurex.com/ex-en/markets/equ/equity-trf>. |
| B | Single stock dividend futures (Apple, Microsoft, NVIDIA) | These hedge the dividend amount, not the share price. Not useful here. |
| C | Single stock options on US names | EUR options on the Xetra listing of the shares. Launched 2021. They add EUR/USD risk. Source: <https://www.eurex.com/ex-en/find/circulars/circular-2401928>. |

## Design limits

- Monthly expiry does not align with the payment date. The issuer must close the future before expiry on the payment date, or roll it.
- The futures price already excludes dividends that are expected before expiry.

## Open questions

1. Does the issuer's prospectus permit derivatives? See [xstocks-issuer.md](../xstocks-issuer.md#hedging-permission).
2. How liquid are US single stock futures on Eurex? Most single stock futures volume uses off-book trades (TES). No volume data for single US names. UNCONFIRMED.
