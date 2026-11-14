# Phase 2 validation and integrity evidence

Validation date: 2026-11-14 (Asia/Amman). Starting HEAD:
`07c354c59119f124f8d6e2e38d63e9d6d268e9fb`; initial branch `main`, clean tree.
Final branch: `phase2-technical-quality`. See [technical report](PHASE2_CHANGES.md)
and [pre-edit artifact hashes](PHASE2_BASELINE.json).

## Executed checks

| Check | Actual result |
| --- | --- |
| `python -m py_compile ecommerce_market_basket.py` | Passed after syntax repair and at completion; syntax validation only |
| `python -m unittest discover -s tests -v` | 59 tests passed, 0 failures, 0 errors, 0 skipped; full run 12.744 seconds |
| Import smoke | Import in an empty temporary directory succeeds silently, without data loading or plot creation |
| Input validation | Missing file/schema, empty/header-only CSV, malformed CSV, encoding errors, invalid numeric values, missing/blank invoice IDs tested |
| Cleaning and baskets | Historical policies, positive-line aggregation, duplicates, exact labels/country, singletons, global top-100 and denominator verified |
| Apriori | Hand-counted supports, inclusive .02 threshold, length cap 3, invalid matrix and empty-result cases verified |
| Rules | Joint support, directional confidence, lift, lift >= 1, numeric ranking, partitions and empty output verified |
| Integration | Complete synthetic CSV workflow, stage counts and empty-stage messages pass; in-memory notebook source parity passes |
| CLI | Help, default/explicit missing input (exit 2), explicit input from another working directory, no-plot and full synthetic --no-show export verified |
| Plot export | A fresh PNG is decoded successfully; existing output bytes preserved; figure closed |
| Documentation | 95 relative Markdown links checked, README anchors resolve, 6 Python snippets compile; tree matches 35 tracked files |
| Whitespace | `git diff --check` against Phase 2 starting HEAD passes |
| Protected evidence | Notebook, embedded output PNG, tracked PNG, banner and license SHA-256 match the pre-edit manifest |
| Dependencies | All five runtime packages available; pytest absent, so unittest is used; no package installation or manifest modification |

All ordinary tests use invented synthetic data, never the missing historical CSV.
The parity test executes analytical source strings extracted from the notebook
in a temporary Python namespace, not a notebook kernel; it never saves outputs.
No full-dataset rerun or numerical reproduction of the saved teacup rule is claimed.
No coverage percentage is claimed. The original notebook's seven code cells parse.

## Tested environment

This records the installed environment, not a recovered historical lock or a
claim that other versions were tested. Existing requirements remain unpinned.

| Component | Version |
| --- | --- |
| Python | 3.11.9 |
| pandas | 3.0.3 |
| NumPy | 2.4.6 |
| mlxtend | 0.25.0 |
| Matplotlib | 3.11.0 |
| seaborn | 0.13.2 |
| SciPy | 1.17.1 |
| scikit-learn | 1.9.0 |

## SHA-256 comparisons

| Protected artifact | Before and after SHA-256 (identical) |
| --- | --- |
| ecommerce_market_basket.ipynb | `f629ed810743f14bd406f998ed3aeee625f868a6c8cfb66e6c598384822a4206` |
| images/association_rules_plot.png | `06449323da3a48d98d466d9cd0cfee5fe8224352657da5a9744933387a42f4b4` |
| Embedded notebook PNG | `61e561f49369df9604ebd27be818d150db3a6ccc443e6b669ed7a2d6c3c3786a` |
| images/market-basket-intelligence-banner.svg | `5536f6bf65011ba0716c4c051d54ea5a9284aa1e3b25ff6e35739a9799d5a579` |
| LICENSE | `72a967ad8f5674562cd5bcc81b8665f2791382f23a671d5e7ce595954f636d69` |
| requirements.txt (also unchanged) | `134903ba774e841f42a04ee27bb2f3e43b610e893f7b3fcc2f26d3d2443a4929` |

No original dataset file existed at baseline or completion; dataset comparison
is unavailable, not a passed checksum check. Full notebook byte identity also
protects all saved outputs and metadata. The script is intentionally repaired;
its older Phase 1 preservation restriction no longer applies to Phase 2.

## Git scope and remaining limits

Fifteen genuine local commits cover the independent repairs/tests/docs listed
in [the report](PHASE2_CHANGES.md). All original tracked paths remain. No history
rewrite, artificial commit, date manipulation, push or deployment was performed.
The final SHA is obtained with `git rev-parse HEAD` to avoid a self-referential
commit hash in this file. Final working-tree status is clean.

The historical input identity and historical package environment remain open.
Other limitations include invoice consistency, product mappings, duplicate/price
semantics, top-product boundary ties, selection bias and unmeasured business value.
Per-filter exclusion logs and full analytical exports remain future work.

---

## Phase 1 record retained below (2026-11-08)

The following is historical evidence from the previous documentation-only phase.
Its preservation scope, execution statements and commit count apply to that phase,
not to this technical repair. Original script line numbers in that record are historical.

# Documentation validation and integrity record

Review date: 2026-11-08. Starting HEAD:
`ad13f98afac5c646bb38cd3521d69352c2d86e0c`, branch `main`, initially clean.
This record accompanies the final documentation/contribution-guidance commit.
It intentionally does not embed its own commit hash. To list all 15 local
commits, use `git log --reverse --oneline ad13f98..HEAD`.

## Preservation results

SHA-256 was checked before each commit and again at completion against the
[full byte/hash baseline](EVIDENCE_BASELINE.md). The editable README is excluded
from the protected set. All original tracked paths remain present.

| Protected artifact | Initial bytes | Final comparison |
| --- | ---: | --- |
| `LICENSE` | 1091 | SHA-256 identical |
| `ecommerce_market_basket.ipynb` | 125761 | SHA-256 identical, including Markdown and saved outputs |
| `ecommerce_market_basket.py` | 1915 | SHA-256 identical, including existing syntax defects |
| `images/association_rules_plot.png` | 143151 | SHA-256 identical |
| `requirements.txt` | 45 | SHA-256 identical |

No data file existed in the initial workspace; none was acquired or created.
No mining, notebook execution, output regeneration, code formatting, dependency
installation, history rewrite, or push was performed. Temporary rendering files
were kept outside the repository. Existing user changes were absent at baseline.

## Documentation and evidence checks

| Check | Method and result |
| --- | --- |
| README composition | Exactly 18 numbered second-level case-study sections |
| Markdown | Parsed with installed Mistune and table plugin; consistent table columns, valid separator rows, Python snippets parse |
| Local links | Relative file targets, image paths, README anchors, and script line references checked |
| Tracked structure | README tree compared with `git ls-files`; includes only actual project paths |
| Banner | XML valid; 1200 × 400 viewBox; no scripts, image embeds, remote references, or external fonts; all five requested palette colors |
| Banner appearance | Rendered in headless Chrome and visually inspected; original retail-node/basket composition, legible labels, no fabricated metric |
| Mermaid | README flowchart rendered successfully with Mermaid 11.4.1 in a temporary browser preview; one SVG, no parse error; stage order checked against notebook |
| README appearance | Local HTML preview visually inspected for hero, navigation, and tables; GitHub's own renderer may differ |
| Original visuals | Tracked PNG and embedded notebook PNG both viewed; resolution/provenance distinction recorded |
| Saved values | All ten itemset supports and thirty rule metric values matched to notebook HTML; fully readable pair names checked |
| Arithmetic | Metric example and rounded reciprocal teacup-rule consistency checked; no source-data recomputation claimed |
| Source syntax | In-memory parse confirms script failure at line 34; all seven notebook code cells parse |
| Audit coverage | Fourteen distinct findings; 0 Critical, 2 High, 9 Medium, 3 Low; eight Confirmed, five Potential, one Unverified |
| Git scope | Only README, 13 new documentation files, CONTRIBUTING, and one SVG differ from starting HEAD |
| Git whitespace | `git diff --check ad13f98..HEAD` and staged-diff checks pass |
| Git history | Fifteen nonempty local Conventional Commits; protected-file hashes checked before each |

The final commit records contribution standards, this validation evidence,
the exact final tree, and rendering/wording corrections found during review.
The banner is tracked in its own earlier commit; its final palette includes
Obsidian Navy, Deep Indigo, Electric Cyan, Refined Violet, and Soft White.

## External references and remaining uncertainties

Web-tool checks reached the repository, author GitHub, UCI source page, pandas
API, mlxtend guides, and mlxtend source. Kaggle resolved but provided no readable
metadata, so its attribution remains a repository claim. The DOI redirected to
the expected UCI path, but the tool failed on the redirect. The requested
[portfolio URL](https://portfolio-1kpn.onrender.com) was inaccessible via that
tool and is retained as supplied. Local shell HTTP requests were blocked by
the environment; they are not evidence that these websites are down.

No full input identity, local row count/date coverage, cleaning counts, basket
shape, total itemsets/rules, complete clipped rule names, historical dependency
versions, or commercial effects could be established. See the
[audit](CODE_AUDIT.md), [provenance record](DATA_PROVENANCE.md), and
[saved-output ledger](VERIFIED_RESULTS.md). No independent reproduction was
claimed. The repository is ready for documentation review and owner-controlled
publishing, with the implementation limitations explicitly disclosed.
