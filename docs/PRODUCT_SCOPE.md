# Product selection and country scope

Source: [notebook](../ecommerce_market_basket.ipynb) cell 8, source lines 1–6;
[script](../ecommerce_market_basket.py#L22) lines 22–27.

## What the top 100 actually means

`df['Description'].value_counts().head(100).index` ranks exact description
strings by the number of cleaned lines across all countries. Quantity is not
summed for ranking; invoice IDs are not deduplicated for ranking. UK selection
occurs later in `df_filtered[df_filtered['Country'] == 'United Kingdom']`.

**Illustration, not observed data:** a description appearing on 50 overseas
lines and 2 UK lines can outrank one appearing on 40 UK lines. A description
with many repeat lines can outrank one present in more distinct invoices.
The resulting universe should not be called the UK's top products by demand.

## Two distinct selection effects

1. **Column restriction:** descriptions outside the selected set cannot appear
   in itemsets or rules. Long-tail, low-row-frequency, and locally popular
   products can be excluded before mining.
2. **Row restriction:** invoices with no selected descriptions vanish in the
   pivot. The ≥ 2 selected-description condition then removes further invoices.
   A large original basket can become a singleton after projection.

Even a rule containing selected descriptions can have different metrics under
another product universe, because universe changes alter eligibility for the
two-description basket filter. This is stronger than simply hiding columns.

## Limits and alternatives to evaluate later

| Question | Current evidence | Future comparison |
| --- | --- | --- |
| Are 100 descriptions in the UK pivot? | Not recorded; some globally selected descriptions may have no UK rows | Record actual width and labels |
| Is the selection stable? | One saved configuration; no tie-order policy or lock | Persist selected labels and compare ranking stability |
| Does it reflect UK order frequency? | No; ranking is global line frequency | Compare UK unique-invoice frequency |
| Are excluded invoices materially different? | No population diagnostics | Compare retained and rejected invoice profiles |

Changing the country order or ranking definition is a methodological change,
not a documentation correction. Recompute basket counts, itemsets, and rules
before presenting results from any alternative. No such experiment was run.
