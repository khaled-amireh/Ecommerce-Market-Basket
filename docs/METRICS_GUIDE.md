# Support, confidence, and lift

Use the same transaction population for every count. Here it is the retained
UK invoice population defined in [basket engineering](BASKET_ENGINEERING.md).
For disjoint itemsets A and B, `n(X)` counts baskets containing all items in X.

| Quantity | Formula | Meaning |
| --- | --- | --- |
| Support of X | `s(X) = n(X) / N` | Fraction containing X |
| Rule support | `s(A union B)` | Fraction containing both sides |
| Confidence A → B | `s(A union B) / s(A)` | Conditional occurrence of B given A |
| Lift A → B | `s(A union B) / (s(A) * s(B))` | Relative joint occurrence against independence |

These match [mlxtend's metric definitions](https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/association_rules/).
The notebook delegates metric calculation to `association_rules` (cell 12,
source line 1), rather than computing ratios manually.

## Worked example — illustrative only

Suppose 100 baskets include A in 20, B in 10, and both in 5:

| Calculation | A → B | B → A |
| --- | ---: | ---: |
| Joint support | 5/100 = 0.05 | 5/100 = 0.05 |
| Confidence | 5/20 = 0.25 | 5/10 = 0.50 |
| Lift | 0.25/0.10 = 2.5 | 0.50/0.20 = 2.5 |

This invented arithmetic example is separate from the saved project results.
It shows why a reverse rule is not equivalent in confidence, even though
support and lift are unchanged.

## Reading the actual visible rule

The saved pink → green rule has support 0.037421, confidence 0.836439, and lift
14.901311. Thus about 3.7421% of retained baskets contain both descriptions.
About 83.6439% of retained baskets containing pink also contain green. Lift
compares that conditional frequency with green's frequency in the same retained
population. It is not a 14.9-fold increase caused by a promotion.

From rounded metrics, `0.836439 / 14.901311` implies an approximate green
marginal support of 0.056132. This is an arithmetic consistency check, not a
new measured output. The reverse values imply pink support near 0.044739.
Rounding prevents recovery of exact counts or denominators.

## Common interpretation errors

- High confidence can reflect a common consequent; check its baseline frequency.
- High lift can coexist with low absolute coverage; inspect support and counts.
- Lift of 1 matches independence for these item-presence events; it is not a
  test that all product behavior is independent.
- Support .02 is not a p-value and does not control multiple comparisons.
- Filtering invoices changes the population; metrics do not automatically
  generalize to all customers, orders, or future dates.
- Product-set association does not establish sequence, causation, profit,
  or statistically validated recommendation performance.
