# Apriori configuration and search boundaries

Source: [notebook](../ecommerce_market_basket.ipynb) cell 10, source lines 1–5;
[script](../ecommerce_market_basket.py#L32) lines 32–36.

| Setting | Verified value | Analytical consequence |
| --- | --- | --- |
| Input | `basket_sets.astype(bool)` | Presence-only matrix, not quantity weighting |
| Minimum support | `0.02` | Relative to retained invoices, not source line count |
| Maximum length | `3` | No four-or-more-description itemsets |
| Column names | `True` | Returned frozensets use description labels |
| Low memory | `True` | Iterator-based processing; no runtime benchmark is saved |
| Output ordering | Support descending | Display order only; all itemsets remain available |

## Frequency is not significance

If there are N retained baskets, an eligible itemset needs at least
`ceil(0.02 * N)` occurrences in the mathematical threshold definition. N is not
saved, so this repository cannot report an observed minimum occurrence count.
The cutoff excludes infrequent combinations, without testing independence,
confidence intervals, false discoveries, or business usefulness.

Apriori grows candidates from frequent subsets. A pair cannot be frequent if
one of its members is infrequent. Boolean encoding matches the documented
[mlxtend input contract](https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/apriori/).
Low-memory mode affects candidate processing rather than the intended support
definition; it is not evidence of a faster run.

## Correctly handled and unchecked conditions

The entire frequent-itemset table is retained for association rules, including
singleton supports needed for confidence and lift. The `.head(10)` expression
does not truncate the variable. Sorting also does not discard itemsets.

There are no explicit checks for zero retained baskets, zero columns, nonfinite
input quantities, or empty itemset results. Boolean conversion guarantees the
submitted values are Boolean, but cannot validate earlier transaction semantics.
With no frequent itemsets, downstream rule generation has no supported input;
the [library source](https://github.com/rasbt/mlxtend/blob/master/mlxtend/frequent_patterns/association_rules.py)
contains an empty-input rejection. Historical edge-case behavior depends on the
unrecorded package version.

## Future sensitivity study

Compare support thresholds, product-universe definitions, and itemset length
only after establishing the input and environment baseline. Record basket
counts, itemset counts by length, complete rule tables, runtime, memory, and
temporal stability. No threshold sweep or expensive mining was performed here.
