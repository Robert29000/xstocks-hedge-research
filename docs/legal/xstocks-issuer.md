# xStocks issuer and product

Checked on 2026-10-19. Back to the [index](README.md).

## Main sources

- Base prospectus 2026-05-08 (file dated 2026-07-27, probably includes the First Supplement): <https://cdn.prod.website-files.com/655f3efc4be468487052e35a/6a748b81c9b1aca19a11c102_Backed_Assets_Base%20Prospectus_20260727.pdf>
- Legal documentation index (supplements, archive): <https://assets.backed.fi/legal-documentation>
- Product page example (Amazon xStock): <https://assets.backed.fi/products/amazon-xstock>
- Kraken xStocks FAQ: <https://support.kraken.com/articles/xstocks-faq>

The research could not read the Second Supplement (2026-09-29). It may change some facts below.

## Issuer

| Item | Value | Status |
|---|---|---|
| Name | Backed Assets (JE) Limited | CONFIRMED (prospectus) |
| Legal form | Private company under the Companies (Jersey) Law 1991 | CONFIRMED |
| Registered office | First Floor, La Chasse Chambers, Ten La Chasse, St Helier, Jersey JE2 4UE | CONFIRMED |
| Registration number | 152608 | CONFIRMED |
| LEI | 984500001AB7C6C7F577 | CONFIRMED |
| Administrator | Cavendish Fiduciary (Jersey) Limited | CONFIRMED |
| Incorporation | 19 January 2024 | CONFIRMED |
| Earlier issuer | Backed Assets GmbH (Zug). It merged into the Jersey company on 23 February 2024. The Zug register deleted it on 24 June 2024. | CONFIRMED |

## Regulatory status

The Jersey FSC registered the issuer for anti-money-laundering purposes only. The issuer also holds a consent under the Control of Borrowing (Jersey) Order 1958 to issue securities.

The prospectus states:

> "the Issuer is not required to be licensed, registered or authorised under any current securities commodities or banking laws of its jurisdiction of incorporation and will operate without supervision by any authority in any jurisdiction."

The prospectus also states that the COBO consent "does not give the issuer a 'regulated' status". It states that the issuer is "not subject to authorisation by … FINMA".

**Result:** the issuer is an unregulated special purpose vehicle (SPV). Venues onboard it as a normal corporate client, not as a regulated financial institution.

## Prospectus approval and passporting

- The Liechtenstein FMA approves the base prospectus under the EU Prospectus Regulation. Approvals: 9 May 2022, 9 May 2023, 8 May 2024, 8 May 2025, 8 May 2026. The current approval is valid "until the expiry on 7 May 2027". CONFIRMED.
- The FMA notified the prospectus to these countries: Austria, Belgium, Czech Republic, Denmark, France, Germany, Ireland, Luxembourg, Malta, Norway, Spain, the Netherlands. CONFIRMED.
- Registry examples: [Finanstilsynet (Norway)](https://www.finanstilsynet.no/en/approved-prospectuses/2024/base-prospectus-backed-assets-je-limited-1717081309), [MFSA supplement certificate (Malta)](https://www.mfsa.mt/wp-content/uploads/2026/08/Backed-Assets-JE-Limited-Certificate-of-Approval-of-a-Supplement-dated-04-August-2026.pdf).

## Legal form of the product

> "The securities offered by the Issuer to Investors ("Products") are designed as Tracker Certificates"

- Swiss Derivatives Map type 1300. Swiss law governs the products.
- The products are "structured products (and debt instruments) according to Swiss Law".
- They are Swiss ledger-based securities (Art. 973d CO), issued as ERC-20 and Solana SPL tokens.
- They are open-ended. The investor has a put right and the issuer has a call right.
- They are not ETPs, funds, or collective investment schemes.

## Dividends and corporate actions

**Reinvestment, not cash.** The Final Terms of each product state if the "Recalculation" includes dividends. If it includes them, the issuer reinvests the dividend into more underlying shares. A smart-contract multiplier then changes the balance of each holder. The prospectus describes the trigger as "dividend, interest or similar payments received by the Issuer from the Underyling are reinvested into Underlyings" (typo in the original).

**Timing.** The prospectus does not give the timing. Kraken's FAQ gives it:

> "Net Dividend (after 30% US withholding tax) divided by the closing price of the underlying share on the prior day."
>
> "The multiplier is updated at approximately 8:00 PM EST on the day prior to the Ex-Date."
>
> "There is no separate cash credit."

**Result:** the multiplier increases before the ex-date. The issuer receives the cash only on the payment date. This gap is the risk that the hedge research measures. See [xstocks-ecosystem.md](xstocks-ecosystem.md#multiplier-mechanism) for the data evidence.

**Withholding tax.** The prospectus states only: "The Issuer may be subject to local withholding taxes … from underlying investments." It gives no rate. The xStocks API shows 30% for most US events (the `withholdingTaxRate` field).

**Issuer discretion.**

- The issuer decides "without the consent of Investors" if an Adjustment Event occurred. Examples in the prospectus: "capital increases, delistings, share splits, special dividends".
- The issuer "may take the necessary adjustment actions… in its duly exercised discretion".
- The issuer can terminate the product if an event "in the sole discretion of the Issuer requires a discontinuation". The issuer must give at least 30 business days notice.

## Fees

| Fee | Value | Source |
|---|---|---|
| Management fee | None at present. Up to 0.25% per year "may be introduced". | Amazon xStock product page |
| Issuance and redemption fee | Up to 0.50% | Amazon xStock product page |
| Maximum investor fees | "up to 5% of the market price of the Underlying" | Prospectus |

## Restricted jurisdictions and investor eligibility

- **United States:** the products "may not be offered, sold or delivered within the United States to, or for the account or benefit of U.S. Persons". CONFIRMED (prospectus).
- **United Kingdom:** "NOT available for UK Clients". The UK selling restriction permits offers only to qualified investors or to fewer than 150 persons. CONFIRMED.
- **Kraken FAQ:** not accessible in the US, Canada, the UK, or Australia. Available in "110+ countries".
- **Direct subscription:** only "Qualified Professional Investors" can subscribe directly with the issuer. Retail investors buy through Authorised Participants.
- The full restricted-country list is not public. UNCONFIRMED.

These restrictions apply to the sale of the tokens. They do not stop the issuer from buying US shares or US derivatives for its hedge.

## Counterparty rule

The Jersey FSC consent limits the issuer's brokers and prime borrowers. They must be:

> "reputable financial services companies subject to the appropriate regulation in (i) the European Union, (ii) in Jersey, (iii) in the United Kingdom, and (iv)" other jurisdictions that are not on the FSC higher-risk list.

This rule is the main legal filter for the venue list in [README.md](README.md#how-the-venues-were-filtered).

## Hedging permission

The issuer's "sole business purpose is the issuance and redemption" of products. The products are backed 1:1 by underlying shares ("Standard Collateral"). The research found no prospectus clause that permits the issuer to trade derivatives for hedging. The word "hedg" appears only in text that advises investors.

Possible results (inference, UNCONFIRMED):

1. Strategy A (financing) is closest to the existing business. The issuer already uses brokers. A short loan to buy the reinvestment shares early may need no new consent.
2. Strategies B and C (futures, options) may need a prospectus supplement or FSC consent.
3. A Payward-group company could hold the hedge and charge the issuer through an intercompany agreement.
