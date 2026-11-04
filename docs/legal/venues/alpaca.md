# Alpaca Securities

Checked on 2026-10-19. Collateral section checked on 2026-11-04. Status: **Kept**. Strategies: A, C. Back to the [index](../README.md).

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
| A | Margin loan (Reg T) | The bought shares are the collateral. Alpaca's lien covers all accounts of the same customer, also the account with the pledged backing shares. See [Collateral and lien](#collateral-and-lien). UNCONFIRMED if Alpaca permits margin in the issuer's account type. |
| B | None | Alpaca offers no futures. |
| C | US listed equity options (levels 1 to 3, long calls at level 2) | Options eligibility for corporate and international accounts is UNCONFIRMED. A corporate issuer can be classified as "non-retail", which changes the commission. |

## Collateral and lien

Research on 2026-11-04. The collateral values are in section 4.1 of the notebook. Sources: the Alpaca margin documentation <https://docs.alpaca.markets/docs/margin-and-short-selling> and the Customer Agreement V26.2026.07 with the margin appendix <https://files.alpaca.markets/disclosures/library/AcctAppMarginAndCustAgmt.pdf>.

| Point | Finding | Status |
|---|---|---|
| Collateral for a share purchase | The bought shares are the collateral (margin purchase). Initial margin is 50% (Regulation T). | CONFIRMED |
| Maintenance margin | 30% for long stocks above USD 6. 50% if one stock is 70% or more of the stock value and the margin balance is USD 100k or more. | CONFIRMED |
| Changes | Alpaca can change maintenance margin and rates without notice. | CONFIRMED |
| Minimum equity | USD 2,000 | CONFIRMED |
| Interest period | On the settlement-date debit, daily, rate/360, overnight only | CONFIRMED |
| Interest on free cash | Alpaca has no obligation to pay interest (Customer Agreement §41). A High-Yield Cash program exists for Trading API users. Eligibility for business accounts is UNCONFIRMED. | CONFIRMED |
| Elite rate | Needs a deposit of USD 100,000. Volume is not a criterion. Source: <https://alpaca.markets/elite> | CONFIRMED |
| Broker API | The partner sets the margin multiplier ("1", "2", or "4") for each account. | CONFIRMED |
| Portfolio margin, unsecured credit, loans against T-bills | No public offer | UNCONFIRMED |

**Lien.**

- The margin appendix gives Alpaca a general lien over all property that it holds, "without regard to the number of Accounts I may have with Alpaca" (Appendix A §2). Alpaca can sell property in any account of the customer without notice (§3, §10). It can use free cash in any account to pay debts (§41). CONFIRMED.
- Alpaca can pledge, re-pledge, and lend securities in any account (Appendix A §5, §7). SEC Rule 15c3-3 limits this to 140% of the debit. CONFIRMED.
- Under New York UCC 9-328(3), the lien of a securities intermediary ranks ahead of other secured parties. Source: <https://www.law.cornell.edu/ucc/9/9-328>. CONFIRMED (statute).
- **Result:** Alpaca also holds the backing shares under an account control agreement for the security agent. A margin loan at Alpaca can conflict with this pledge, unless the account control agreement subordinates Alpaca's lien. The agreement is not public. UNCONFIRMED.
- Appendix A applies only after Alpaca gives separate written notice (§29). The issuer may have negotiated terms.

## Open questions and contacts

1. Can the issuer's existing Alpaca account use margin or options?
2. Does the prime brokerage launch change the financing terms?
3. Is the securities lending income (Prime Borrower) large enough to fund the gap cost?
4. Does the account control agreement for the security agent subordinate Alpaca's general lien?
