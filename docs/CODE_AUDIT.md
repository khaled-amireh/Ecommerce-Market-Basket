# Read-only analytical correctness audit

Review date: 2026-11-08. Baseline:
`ad13f98afac5c646bb38cd3521d69352c2d86e0c` on `main`.
All protected original files remain unchanged. No mining or dataset reconstruction was run.
See the [hash baseline](EVIDENCE_BASELINE.md) and [saved-result ledger](VERIFIED_RESULTS.md).

## Method and severity

The review covers every tracked file, every notebook source cell and saved
output, and both original chart artifacts. In-memory Python parsing confirms
the script syntax failure; all seven notebook code cells parse. A parsing check
does not establish end-to-end runtime success.

Notebook references below use zero-based cell index, cell ID where helpful,
and one-based source lines. Script references use one-based file lines.

- **Confirmed:** directly established code behavior, defect, or evidence gap.
  A confirmed design limitation is not automatically an algorithmic error.
- **Potential:** a concrete unchecked condition could affect results; its presence
  and magnitude in the absent input are unknown.
- **Unverified:** a reliability or outcome claim cannot be assessed with saved evidence.
- **High:** blocks an advertised execution path or independent result verification.
  **Medium:** can materially change population, identity, or interpretation.
  **Low:** edge-case robustness or reporting issue. No Critical issue was found.

| Severity | Confirmed | Potential | Unverified | Total |
| --- | ---: | ---: | ---: | ---: |
| Critical | 0 | 0 | 0 | 0 |
| High | 2 | 0 | 0 | 2 |
| Medium | 4 | 4 | 1 | 9 |
| Low | 2 | 1 | 0 | 3 |

## Confirmed defects and evidence gaps

### AUD-01 — Standalone script cannot parse

- **Severity / status:** High / Confirmed.
- **Location:** [script](../ecommerce_market_basket.py#L34), lines 34–35 and 41–42.
- **Evidence:** each `print("` is followed by a literal newline before closing
  the string. `ast.parse` reports an unterminated string literal at line 34.
- **Explanation:** ordinary quoted strings cannot span these source lines.
- **Impact:** the entire script fails before loading data or mining. This does
  not prove that the separately saved notebook outputs are wrong.
- **Minimal recommended correction:** in a future authorized code change, use
  escaped newlines or separate print calls for both affected statements.
- **New evaluation necessary:** parsing and script/notebook parity execution
  are needed after repair; no new mining parameters are implied by this fix.

### AUD-02 — Input snapshot is absent and lineage cannot be established

- **Severity / status:** High / Confirmed.
- **Location:** [script](../ecommerce_market_basket.py#L11), line 11; notebook
  cell 4 (`e33f3e0c`), source lines 1–2 and saved preview; initial six-file tree
  in [baseline](EVIDENCE_BASELINE.md).
- **Evidence:** local `data.csv` loader; no tracked or initially present CSV,
  acquisition record, input hash, full shape, or date-range output.
- **Explanation:** a source attribution and a five-row preview cannot identify
  the exact input or establish completeness.
- **Impact:** historical metrics cannot be independently verified or assigned
  to a known snapshot. High severity reflects this central verification barrier,
  not a request to bundle a third-party dataset in Git.
- **Minimal recommended correction:** identify the authorized source snapshot
  and publish a checksum/acquisition manifest with schema and stage counts.
- **New evaluation necessary:** yes, an isolated full reproduction is required
  to verify historical values once the input is identified.

### AUD-03 — Singleton filtering changes the meaning of every metric

- **Severity / status:** Medium / Confirmed; intentional population restriction.
- **Location:** [script](../ecommerce_market_basket.py#L29), lines 23–29;
  notebook cell 8 (`37cb3381`), source lines 2–8.
- **Evidence:** only selected descriptions enter the pivot and rows with fewer
  than two present selected descriptions are removed.
- **Explanation:** N is eligible projected invoices, not all UK orders. Original
  multi-item invoices can become excluded singletons after projection.
- **Impact:** joint support is higher than it would be if additional singleton
  and empty projected invoices were retained; confidence and lift can also change.
  This materially limits any interpretation as an all-order association.
- **Minimal recommended correction:** keep the conditional population explicit
  (now documented). For an all-order objective, retain the appropriate invoice
  index and evaluate a revised denominator in a separate implementation change.
- **New evaluation necessary:** no for labeling the current scope; yes for
  estimating its magnitude or reporting an alternative population.

### AUD-04 — Global row-frequency selection precedes UK filtering

- **Severity / status:** Medium / Confirmed; selection-design limitation.
- **Location:** [script](../ecommerce_market_basket.py#L22), lines 22–27;
  notebook cell 8, source lines 1–6.
- **Evidence:** `Description.value_counts().head(100)` runs before the exact
  `Country == 'United Kingdom'` condition; no invoice-level frequency is used.
- **Explanation:** selected descriptions reflect global line counts, not UK
  unique invoice frequency, units, or revenue.
- **Impact:** catalog membership and invoice eligibility may differ from a
  UK-specific analysis; excluded products have no chance to appear in rules.
- **Minimal recommended correction:** name the selection precisely (now done),
  persist selected labels, and compare a UK/invoice-based definition if desired.
- **New evaluation necessary:** yes to compare universes or quantify bias;
  none for the documentation clarification itself.

### AUD-05 — CustomerID exclusion is unnecessary for the basket key

- **Severity / status:** Medium / Confirmed; population choice, not a null bug.
- **Location:** [script](../ecommerce_market_basket.py#L16), lines 16 and 25–27;
  notebook cell 6 source line 1 and cell 8 source lines 4–6.
- **Evidence:** missing CustomerID rows are dropped, while baskets group only
  by InvoiceNo and Description. Missing Description rows are also dropped.
- **Explanation:** known-customer status restricts an invoice-level analysis.
  Row-wise removal can also leave partial invoices.
- **Impact:** anonymous purchases are excluded; population differences and
  partial-invoice effects cannot be quantified without input-level diagnostics.
- **Minimal recommended correction:** justify the known-customer scope and log
  exclusions; only retain anonymous purchases after validating invoice keys in
  a separately authorized change. Null descriptions need an explicit policy.
- **New evaluation necessary:** yes if inclusion policy changes or bias is quantified.

### AUD-11 — Historical dependency environment is not recoverable

- **Severity / status:** Medium / Confirmed.
- **Location:** [requirements](../requirements.txt), lines 1–5; notebook metadata
  `language_info.version`; cell 8 source line 7; cell 12 source line 1.
- **Evidence:** five unpinned package names, no Jupyter tooling or lock; metadata
  records Python 3.11.9 only. `DataFrame.map` is used.
- **Explanation:** the [pandas API](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.map.html)
  dates DataFrame.map to 2.1.0. Package APIs and supported Python versions can
  differ from the historical run. No particular installed-version failure is asserted.
- **Impact:** a fresh install is not a reproducible environment; the original
  Python 3.8+ README badge was not evidence of a tested compatibility range.
- **Minimal recommended correction:** recover and record a verified environment
  in a future dependency change; install notebook/kernel tooling separately for review.
- **New evaluation necessary:** an isolated compatibility run is needed. Existing
  requirements were deliberately preserved.

### AUD-13 — No explicit empty-population or empty-result handling

- **Severity / status:** Low / Confirmed omission; triggering input unverified.
- **Location:** [script](../ecommerce_market_basket.py#L29), lines 29–47;
  notebook cell 8 source line 8, cell 10 source line 3, cell 12 source lines 1–3,
  and cell 14 source line 2.
- **Evidence:** calls proceed without `.empty`, shape, or eligible-rule guards.
- **Explanation:** no eligible UK baskets, no frequent sets, and no qualifying
  rules are distinct cases needing explicit reports. Current
  [mlxtend source](https://github.com/rasbt/mlxtend/blob/master/mlxtend/frequent_patterns/association_rules.py)
  rejects an empty frequent-itemset table; historical behavior is version-dependent.
- **Impact:** alternative inputs may fail or produce an uninformative chart;
  this does not invalidate the nonempty saved previews.
- **Minimal recommended correction:** add explicit population/itemset/rule checks
  and clear summaries in a future code change.
- **New evaluation necessary:** small edge-case checks after implementation;
  no expensive mining required.

### AUD-14 — Script export location differs from documented chart location

- **Severity / status:** Low / Confirmed.
- **Location:** [script](../ecommerce_market_basket.py#L49), line 49; tracked
  `images/association_rules_plot.png`; notebook cell 14 source lines 1–4.
- **Evidence:** script saves `association_rules_plot.png` relative to the current
  directory; notebook displays without `savefig`. The two saved PNGs differ in size.
- **Explanation:** executing the repaired script would not update the tracked
  README image path by default.
- **Impact:** chart provenance and refresh expectations can be misunderstood;
  no proof exists that the tracked image was produced by the current script.
- **Minimal recommended correction:** document the distinction (now done) and
  establish a canonical export path in an authorized implementation change.
- **New evaluation necessary:** visual/export parity check after any path change.

## Potential data-dependent risks

### AUD-06 — Duplicate lines can influence catalog selection

- **Severity / status:** Medium / Potential.
- **Location:** [script](../ecommerce_market_basket.py#L16), lines 16–28;
  notebook cells 6 and 8, especially cell 8 source line 1.
- **Evidence:** no duplicate detection/removal; selection uses row counts.
- **Explanation:** repeated positive lines collapse to one binary presence
  within a fixed invoice/product, but increase pre-selection frequency.
- **Impact:** duplicates could move descriptions into or out of the top 100 and
  thereby change basket eligibility and rules. Prevalence is unknown.
- **Minimal recommended correction:** inspect duplicate candidates with a business
  key and distinguish legitimate repeated lines before any removal.
- **New evaluation necessary:** data-quality inspection first; rerun if selection changes.

### AUD-07 — Description strings may split or merge product identities

- **Severity / status:** Medium / Potential.
- **Location:** [script](../ecommerce_market_basket.py#L22), lines 22–28;
  notebook cell 8 source lines 1–7; cell 10 saved rows 44, 83, and 62.
- **Evidence:** Description is the item key, StockCode is unused, no string
  normalization or mapping checks; saved names include repeated/trailing spaces.
- **Explanation:** whitespace exists in labels, but that alone does not prove
  duplicates. Aliases or shared descriptions across codes remain unverified.
- **Impact:** if mapping conflicts exist, support may be fragmented or distinct
  products merged, altering apparent relationships.
- **Minimal recommended correction:** audit description/code cardinalities and
  define a canonical product identity with display names before changing keys.
- **New evaluation necessary:** mapping inspection; full new results if identities change.

### AUD-08 — Price validity is unchecked

- **Severity / status:** Medium / Potential.
- **Location:** [script](../ecommerce_market_basket.py#L16), lines 16–28;
  notebook cell 6 source lines 1–4 and cell 8 source lines 1–7.
- **Evidence:** positive Quantity filtering exists; UnitPrice is never filtered
  or used after loading. No saved invalid-price counts are available.
- **Explanation:** positive-quantity free or invalid-priced lines could survive;
  a zero-price gift is not necessarily an invalid transaction.
- **Impact:** such lines may influence selection and presence rules. Revenue,
  margin, and profitable bundle claims cannot be inferred from this miner.
- **Minimal recommended correction:** profile price categories and document
  whether gifts, adjustments, and invalid values belong in the target population.
- **New evaluation necessary:** yes if policy excludes previously included lines.

### AUD-09 — Invoice and country consistency is assumed

- **Severity / status:** Medium / Potential.
- **Location:** [script](../ecommerce_market_basket.py#L17), lines 17 and 25–27;
  notebook cell 6 source line 2 and cell 8 source lines 4–6.
- **Evidence:** no InvoiceNo null check before string conversion; only exact
  country matching; no invoice/customer/country consistency assertions.
- **Explanation:** missing IDs may become a shared string key; malformed or
  inconsistent country labels may exclude rows or partially retain invoices.
- **Impact:** if present, key collisions can fabricate co-occurrence, while
  partial or excluded invoices alter the population. None is proven in the input.
- **Minimal recommended correction:** inspect invoice nulls, formatting, and
  within-invoice consistency; resolve collisions and country policy explicitly.
- **New evaluation necessary:** transaction-level validation and a rerun if affected.

### AUD-10 — Cancellation matching does not define net purchases

- **Severity / status:** Low / Potential.
- **Location:** [script](../ecommerce_market_basket.py#L18), lines 18–19;
  notebook cell 6 source lines 3–4.
- **Evidence:** case-sensitive uppercase-C prefix and positive-quantity tests;
  no reconciliation to an original purchase invoice.
- **Explanation:** lowercase or whitespace variants would not match that prefix,
  although nonpositive quantities are still excluded. Returned original sales
  remain unless separately removed. Variant presence is unknown.
- **Impact:** the result is not proven to describe final net retained purchases.
  Standard uppercase-C rows and nonpositive quantities are correctly excluded.
- **Minimal recommended correction:** inspect actual conventions and choose a
  positive-sale versus net-purchase definition before normalizing or reconciling.
- **New evaluation necessary:** only if variant handling or return policy changes.

## Unverified analytical generalization

### AUD-12 — Stability and commercial value have not been evaluated

- **Severity / status:** Medium / Unverified.
- **Location:** [notebook](../ecommerce_market_basket.ipynb) cells 10, 12, and 14,
  all source lines; [script](../ecommerce_market_basket.py#L32), lines 32–50.
- **Evidence:** one support setting, one product scope, one length cap, in-sample
  rankings and scatter; no temporal holdout, sensitivity, uncertainty, or intervention.
- **Explanation:** high lift is descriptive. Repeated customer behavior, seasonal
  products, and catalog selection could affect future stability; no effect size
  or instability is established. Promotional gain is not estimated.
- **Impact:** the saved analysis cannot establish robust prediction, causal
  sales uplift, profitability, or representative all-order behavior.
- **Minimal recommended correction:** frame business uses as hypotheses (now
  done); assess temporal stability and population sensitivity before any deployment,
  then use a controlled experiment for incremental business impact.
- **New evaluation necessary:** yes for generalization or business-outcome claims;
  no new evaluation is needed to state the present evidence limits.

## Positive checks and coverage

| Area | Read-only conclusion |
| --- | --- |
| Missing CustomerID / Description | Explicit row exclusions; no counts saved |
| Zero / negative quantities | Explicitly excluded by `> 0` |
| Standard cancellation rows | Uppercase-C exclusion is implemented |
| Invoice grouping | InvoiceNo and Description, with quantity aggregation |
| Binary input | Positive totals map to 1, others 0; Boolean cast at Apriori call |
| Frequent itemsets | Support .02, maximum length 3, low memory enabled; complete table retained |
| Rule API | Standard lift-threshold call; no confirmed metric formula misuse |
| Rule ordering | Lift descending, confidence descending; support is not a key |
| Directionality | Saved reciprocal pair has equal support/lift, differing confidence |
| Saved arithmetic | Rounded teacup metrics are internally consistent; no mismatch found |
| Chart | Support x, confidence y, size/hue lift; not an evaluation or revenue chart |
| Completeness | Full input, population counts, and full results unavailable |

No finding asserts that an unobserved duplicate, malformed invoice, invalid price,
or catalog alias actually occurs. No manual bug in support/confidence/lift
calculation was found. Routine ideas such as a different mining algorithm are
not scored as defects. The chart alone cannot establish exact counts.

## Overall technical verdict and priorities

**The notebook implements a coherent exploratory presence-based Apriori pipeline
for a narrowly selected invoice population. The standalone script is broken,
and the repository does not support independent reproduction of saved results.**
Confirmed population choices can materially affect metrics relative to an
all-UK-order analysis; their magnitude remains unknown. They are not evidence
that mlxtend calculated the conditional metrics incorrectly.

1. Restore executability in a separately authorized code change (AUD-01), and
   identify the input snapshot before claiming reproduced results (AUD-02).
2. Preserve the explicit population definition and evaluate all-invoice versus
   projected multi-item scope, global versus UK ranking, and known-customer
   exclusion (AUD-03–05).
3. Validate invoice identity, product mapping, duplicates, and price policy before
   interpreting rules as product relationships (AUD-06–10).
4. Recover a tested environment and complete run evidence, including counts and
   untruncated exports (AUD-11); assess stability and business effects separately
   (AUD-12). Add empty-result and export safeguards when code work is authorized
   (AUD-13–14).

These recommendations were documented only. No original code, notebook, data,
requirements, result, license, or chart was modified.
