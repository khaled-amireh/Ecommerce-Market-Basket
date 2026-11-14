# Phase 2 technical quality report

Date: 2026-11-14. Starting HEAD: `07c354c59119f124f8d6e2e38d63e9d6d268e9fb`,
clean `main`. Changes are on `phase2-technical-quality`. No push or deployment.
The complete tracked repository, all 15 notebook cells, saved outputs and metadata,
and all 14 audit findings were reviewed before source repair. No applicable
AGENTS.md was found. The [preservation manifest](PHASE2_BASELINE.json) records
pre-edit hashes. The original dataset is absent, not replaced.

## Confirmed original defects and repairs

Locations in this table refer to the script at the starting HEAD, before edits.
The implementation remains in [ecommerce_market_basket.py](../ecommerce_market_basket.py).

| Problem / original location | Correction / current function | Verification | Possible analytical effect |
| --- | --- | --- | --- |
| Unterminated prints, lines 34–35 and 41–42 | Two escaped newlines; dedicated syntax-only commit | py_compile and smoke test | None to intended calculations |
| Workflow runs on import, lines 11–50 | main guard and small stage functions | Import from empty temporary directory produces no output or files | None |
| Unvalidated schema/numeric values, lines 11–19 | validate_transactions; explicit schema, text-label and finite-real-number checks | Missing-column, malformed-value and nonmutation tests | Invalid input now fails as a whole; no rows silently dropped by validation |
| Opaque missing-file/malformed-input failures, line 11 | load_transactions with specific exceptions and path/encoding context | Temporary CSV tests, missing-file CLI exit 2 | No change for valid input; no fallback data |
| Null invoice IDs can become a shared string, line 17; CSV inference can merge leading-zero IDs, line 11 | Reject missing/blank InvoiceNo; load CSV invoice IDs as text | Null/blank rejection and 001 versus 1 regression | Rejects unsafe input; lexical IDs can split formerly conflated invoices and change all downstream metrics if present |
| No explicit empty-population/result policy, lines 29–47 | mine_itemsets rejects zero eligible baskets; generate_rules returns an empty schema; run_analysis reports empty stages | Empty-matrix/itemset/rule tests and workflow tests | No change to valid nonempty results |
| Chart path ambiguity and overwrite risk, line 49 | Explicit --plot-output, --no-show, --no-plot; exclusive creation in plot_rules | New PNG decoded; existing file unchanged; figures closed | Reporting only; default export remains outside tracked images |

No defect was found in the standard support, confidence or lift formulas. They
remain delegated to mlxtend. No price-sign filter, duplicate removal, label
normalization, alternative country policy or returns reconciliation was added.
The helper functions are stage boundaries, not a new application architecture.

## Analytical integrity and explicit differences

For valid historical-style input, the cleaning order and population remain:
known CustomerID and Description; uppercase-C cancellations excluded; Quantity
positive; global top 100 exact descriptions by cleaned line count; exact UK
matching; invoice/description quantity sums; at least two selected descriptions.
Duplicates are retained. Negative quantities may represent returns; excluding
them preserves a positive-line analysis and does not compute net purchases.
Zero/negative finite prices remain allowed because price is not a mining weight.

Boolean `gt(0)` replaces elementwise integer presence mapping. A synthetic
fixture executes the preserved notebook's analytical source cells in memory
and matches baskets, complete itemsets and complete rules against the revised
script. The notebook itself is never executed or saved by the workflow. This
is a computational parity test, not reproduction of historical data or outputs.

The new input contract is deliberately stricter: any missing/blank invoice ID,
malformed/nonfinite Quantity or UnitPrice, or nontext nonmissing label causes
rejection before cleaning, even if that row would later be excluded. Numeric
strings are accepted and converted; invoice labels retain their lexical CSV
form. pandas' standard CSV missing-value recognition remains enabled. No strict
invoice regex is invented. Identifier consistency across countries/customers,
aliases and blank descriptions still need source-specific investigation.

These safety checks can change which inputs are accepted. Preserving lexical
invoice IDs can change transaction counts, baskets, itemsets, rules and every
metric for affected data. Their presence in the missing historical CSV is
unknown. The notebook retains the older unchecked input behavior.

Default Apriori parameters remain support `.02`, maximum length `3`, column
names enabled, low memory enabled. Rules retain lift `>= 1`, with numeric lift
then confidence descending and no confidence cutoff. A support argument on
mine_itemsets supports explicit experiments; the CLI has no threshold override.
No top-100 tie-breaking policy is imposed beyond pandas' existing ordering.

run_analysis prints loaded/cleaned rows and invoices, eligible basket count,
matrix width, parameters, and itemset/rule counts. It still previews ten rows,
not full table exports or per-filter exclusion logs. A successful run does not
establish source provenance, historical parity, stability or commercial value.

## Reassessment of every audit finding

The original [audit](CODE_AUDIT.md) is retained; editing code does not erase it.

| Finding | Validated classification | Phase 2 status / remaining evidence needed |
| --- | --- | --- |
| AUD-01 syntax | Confirmed defect | Resolved for script: compile and import pass |
| AUD-02 absent snapshot | Reproducibility problem | Open, high priority: recover exact authorized CSV and checksum; full historical rerun unavailable |
| AUD-03 singleton exclusion | Methodological limitation | Deferred, preserved and tested; alternative denominator requires a new experiment |
| AUD-04 global line-frequency ranking | Methodological limitation | Deferred, preserved and tested; UK invoice-frequency alternative would change scope |
| AUD-05 known-customer exclusion | Methodological limitation | Deferred, preserved and tested; anonymous inclusion would change scope |
| AUD-06 duplicate influence | Unverified risk | Open: no evidence that repeated lines are erroneous; retain them |
| AUD-07 description identity | Unverified risk | Open: labels preserved; StockCode mapping/alias investigation needs data |
| AUD-08 price validity | Unverified risk | Partly addressed by finite numeric validation; economic validity and gift/adjustment policy remain open |
| AUD-09 invoice consistency | Unverified risk with confirmed unsafe null-key behavior | Partly addressed: null/blank rejection and lexical loading tested; cross-customer/country consistency remains unverified |
| AUD-10 cancellation variants | Unverified risk | Deferred: exact matching preserved; net-purchase accounting requires source-specific evidence |
| AUD-11 historical environment | Reproducibility problem | Open for history; current installed stack is tested and recorded in VALIDATION; manifests unchanged |
| AUD-12 stability/business value | Methodological limitation / unverified risk | Open; temporal validation and causal intervention are outside this repair scope |
| AUD-13 empty handling | Confirmed defect in robustness | Resolved for script with distinct empty-stage tests; notebook preserved |
| AUD-14 chart location | Confirmed reporting limitation | Resolved export contract: explicit path, unchanged default location, existing files protected; historical PNG provenance still unknown |

## Tests, dependencies and preservation

The focused suite uses standard-library unittest (pytest is not installed),
with temporary synthetic DataFrames/CSVs and hand-derived expected values.
See [validation evidence](VALIDATION.md) for the executed totals and environment,
and [reproduction instructions](REPRODUCTION.md) for commands.
No dependency installation, major upgrade, new runtime framework or speculative
version bound was necessary. Requirements remain unchanged. Recording the
installed versions does not recover the historical environment or promise
compatibility across untested versions.

The notebook, embedded PNG, tracked chart, banner and license must match the
SHA-256 manifest byte for byte. No original dataset exists to hash. Script and
documentation are intentionally changed; no historical output is regenerated.
The saved pink-to-green metrics `.037421 / .836439 / 14.901311` remain historical
evidence only and were not independently reproduced.

## Local review

The work is organized into 15 nonempty Conventional Commits. Obtain all exact
SHAs/messages, including the final evidence commit, with:

```bash
git log --reverse --format="%H %s" 07c354c59119f124f8d6e2e38d63e9d6d268e9fb..HEAD
git diff --stat 07c354c59119f124f8d6e2e38d63e9d6d268e9fb..HEAD
git diff --check 07c354c59119f124f8d6e2e38d63e9d6d268e9fb..HEAD
git status --short
```

Commit groups separate syntax, import safety, schema, loading, historical
cleaning, identifier safety, basket extraction, population regression, Apriori,
rules, empty stages, CLI/export, integration/diagnostics, audit reconciliation,
and reproduction/validation. No empty commits or timestamp manipulation.
