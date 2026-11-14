# Basket construction and the support denominator

> **Phase 2 update (2026-11-14):** The script now uses `build_baskets` on cleaned data. Vectorized `gt(0)` produces Boolean presence directly; synthetic notebook-parity tests confirm the same grouping and eligibility. Global top-100, exact UK matching and singleton exclusions remain unchanged. Empty eligible populations fail clearly before mining. Missing invoice IDs are rejected before grouping.
> See [verified corrections](PHASE2_CHANGES.md). The original review below describes
> the preserved notebook and Phase 1 script; its script line numbers are historical.

Source: [notebook](../ecommerce_market_basket.ipynb) cell 8, ID `37cb3381`,
source lines 4–8; [script](../ecommerce_market_basket.py#L25) lines 25–29.

The quantity sum for each UK `(InvoiceNo, Description)` pair becomes one matrix
cell. `unstack()` moves descriptions to columns; `fillna(0)` represents an absent
combination. `map(lambda x: 1 if x > 0 else 0)` creates integer presence flags.
The row filter counts present columns, and the later Apriori call casts Boolean.
This is internally consistent presence encoding for surviving positive lines.

## Population contract

Let S be the globally selected descriptions and D(i) the surviving UK description
set for invoice i. The implemented basket is `D(i) intersect S`, and the mining
population is `T = {i: size(D(i) intersect S) >= 2}`. All support denominators
are `N = size(T)`. Neither the number of raw lines nor all UK invoices is N.

The basket is invoice-level, not customer-level or session-level. Customer IDs
are only used for exclusion. Invoice uniqueness across customers and countries
is assumed, without an assertion. Invoices spanning inconsistent country labels
could be partially retained; their presence in this input is unverified.

## Why singleton exclusion matters

**Illustration only, not project data.** Suppose three invoices contain `{A,B}`,
`{A}`, and `{C}`; all descriptions are selected. Before exclusion, support of
`{A,B}` is 1/3, confidence A → B is 1/2, and lift is 1.5. Keeping only the first
invoice gives support 1, confidence 1, and lift 1. Removing baskets can raise
support while reducing lift. It is not simply removal of uninformative rows.

For any retained pair, removing only singleton/empty projected baskets leaves
the pair numerator unchanged and reduces N. Marginal counts may also change,
so neither confidence nor lift should be assumed to scale like joint support.

## Edge cases and future checks

| Condition | Current behavior / boundary | Proposed verification |
| --- | --- | --- |
| Repeated positive product lines | Sum quantities, then collapse to presence | Inspect duplicates before global ranking |
| Missing InvoiceNo | String conversion may create a shared textual key | Reject or resolve missing keys before grouping |
| No UK rows or eligible pairs | No explicit empty-basket guard | Fail with a population summary before mining |
| Description aliases | Treated as separate columns | Audit StockCode-to-description mapping |
| Repeated customer invoices | Separate observations | Assess customer dependence for validation |

No dimension or population count is saved. Correctness of this population for a
business objective is a separate question from correct binary encoding.
