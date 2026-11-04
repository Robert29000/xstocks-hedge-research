# Alpaca Securities

Checked on 2026-10-19. Status: **Kept**. Strategies: A, C. Back to the [index](../README.md).

Numbers (rates and fees) are in [`hedge_research.ipynb`](../../../hedge_research.ipynb), in the venue tables for each strategy.

## Legal entity and regulator

- Alpaca Securities LLC is a US broker-dealer. Regulators: SEC and FINRA. SIPC member. CONFIRMED.
- Alpaca is the main custodian and broker for the xStocks underlying shares. It is also the Prime Borrower under the securities lending agreement. See [xstocks-ecosystem.md](../xstocks-ecosystem.md#custodians-and-brokers).
- Alpaca Derivatives LLC registered as an FCM with the CFTC and NFA in August 2026, for prediction markets only. It "has not yet commenced" business. Source: <https://alpaca.markets/blog/alpaca-registers-as-futures-commission-merchant-with-the-cftc-and-nfa-to-advance-launch-of-prediction-markets/>. CONFIRMED.

## Onboarding a Jersey corporate

- The issuer already has an account relationship with Alpaca. The terms of that relationship are not public.
- The Alpaca fee schedule states that accounts opened through a business partner (Broker API) can have different fees. The issuer's real terms are probably negotiated. Source: <https://files.alpaca.markets/disclosures/library/BrokFeeSched.pdf>.
- Alpaca business accounts for non-US companies are in beta for "select entities". The page is from November 2022. Source: <https://alpaca.markets/support/non-us-business>. Jersey eligibility is UNCONFIRMED.
- Alpaca plans a prime brokerage service (financing, margin, securities lending) for about Q1 2027. Source: <https://hedgeweek.com/news/alpaca-targets-prime-brokerage-expansion-amid-tokenised-stock-growth>. UNCONFIRMED.

## Products for each strategy

| Strategy | Product | Legal notes |
|---|---|---|
| A | Margin loan (Reg T) | The shares that back xStocks are pledged. Margin on these shares conflicts with the pledge. A separate margin account with other collateral is necessary. UNCONFIRMED if Alpaca permits margin in the issuer's account type. |
| B | None | Alpaca offers no futures. |
| C | US listed equity options (levels 1 to 3, long calls at level 2) | Options eligibility for corporate and international accounts is UNCONFIRMED. A corporate issuer can be classified as "non-retail", which changes the commission. |

## Open questions and contacts

1. Can the issuer's existing Alpaca account use margin or options?
2. Does the prime brokerage launch change the financing terms?
3. Is the securities lending income (Prime Borrower) large enough to fund the gap cost?
