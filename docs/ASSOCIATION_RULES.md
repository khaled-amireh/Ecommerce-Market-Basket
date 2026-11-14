# Rule generation, ranking, and interpretation

> **Phase 2 update (2026-11-14):** The script now uses `generate_rules` with the same lift >= 1 threshold and numeric lift/confidence ranking. Empty itemsets return an empty five-column rule table; no qualifying rules skip plotting. Hand-counted fixtures verify metrics, direction, inclusive filtering and ranking.
> See [verified corrections](PHASE2_CHANGES.md). The original review below describes
> the preserved notebook and Phase 1 script; its script line numbers are historical.

Source: [notebook](../ecommerce_market_basket.ipynb) cell 12 (ID `e9595a4d`),
source lines 1–3; [script](../ecommerce_market_basket.py#L39) lines 39–43.

```python
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)
rules = rules.sort_values(by=['lift', 'confidence'], ascending=[False, False])
rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(10)
```

## Selection contract

The passed table is the complete Apriori result, including supports for subsets.
Rules partition a frequent itemset into disjoint, nonempty antecedent and
consequent sets. The three-item mining cap therefore allows 1 → 1, 1 → 2,
and 2 → 1 rules. The cap concerns the union, not three items on each side.

The metric threshold is inclusive: lift ≥ 1. A rule at exactly 1 qualifies even
though it provides no association above the independence baseline. There is
no independent minimum confidence filter. Joint support is constrained by the
itemset stage. Ranking is lexicographic: lift first, confidence as tie-breaker;
support is not a sort key. The original README's suggestion of a combined
three-metric rank was unsupported.

The [.head(10) preview](../ecommerce_market_basket.ipynb) does not limit the rules
used by the scatter plot. Original row labels survive sorting and cannot be
used as a rule count or rank. The complete rule count is not saved.

## Direction and scope

The saved pink → green teacup rule has confidence 0.836439; reversing it gives
0.666667. Both directions share support 0.037421 and lift 14.901311. This is
consistent with directional confidence and symmetric lift. It describes selected
invoices, without predicting which item was purchased first.

Multi-item sets mean **all** listed descriptions, not interchangeable options.
Do not guess the clipped members in the higher-ranked saved rule rows. The
notebook's HTML is truncated too; it does not contain a hidden full-name export.

## Reliability boundaries

The API invocation agrees with the [official rule guide](https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/association_rules/).
There is no manual metric arithmetic in the project and no confirmed library
misuse for a valid nonempty table. There are no guards for empty itemsets or no
qualifying rules, and no recorded historical package versions. Compatibility
with a fresh installation must be checked in a separate reproduction.

High lift is a relative association score. A useful retail decision also needs
absolute frequency, margin, availability, customer eligibility, and incremental
impact evidence. No causal claim, revenue estimate, or deployment follows from
the saved rule metrics alone.
