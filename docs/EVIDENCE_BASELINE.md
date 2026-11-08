# Repository evidence and preservation baseline

Inspection date: 2026-11-08. Starting branch: `main`. Starting HEAD:
`ad13f98afac5c646bb38cd3521d69352c2d86e0c`.
`git status --porcelain=v1` was empty before any edits. No pre-existing changes
were present. No applicable `AGENTS.md` was found in the workspace or ancestors.

## Scope and method

All six tracked files were inspected: README, script, notebook JSON (all 15
cells, source, saved text/HTML outputs and metadata), requirements, license,
and the original PNG. The PNG was viewed at its stored 829 × 561 resolution.
The notebook also contains an embedded scatter plot. No dataset is tracked or
present in the initial workspace. No analysis, mining, dependency installation,
or output regeneration was performed.

The original implementation, notebook Markdown, outputs, image, requirements,
and license are protected. Only README, new documentation, CONTRIBUTING, and
one new SVG may change. Hashes below describe working-tree bytes before editing,
including their original line endings; they are not Git blob hashes.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `LICENSE` | 1091 | `72a967ad8f5674562cd5bcc81b8665f2791382f23a671d5e7ce595954f636d69` |
| `ecommerce_market_basket.ipynb` | 125761 | `f629ed810743f14bd406f998ed3aeee625f868a6c8cfb66e6c598384822a4206` |
| `ecommerce_market_basket.py` | 1915 | `192e57a7948635e26622d393c20be2a1ef4f858c3ddf7b9cb8647cd21e1c3170` |
| `images/association_rules_plot.png` | 143151 | `06449323da3a48d98d466d9cd0cfee5fe8224352657da5a9744933387a42f4b4` |
| `requirements.txt` | 45 | `134903ba774e841f42a04ee27bb2f3e43b610e893f7b3fcc2f26d3d2443a4929` |

The original, editable README was 11903 bytes, SHA-256
`e7c97f5990f4b80e3021cdbb1f6daf24c9d3413d155a1b0638159053b8e7c781`.

## Evidence locations

Notebook references use **zero-based cell indices** and one-based source lines
within a cell; these remain stable because the notebook is preserved.

| Stage | Notebook cell / ID | Script lines | Evidence |
| --- | --- | --- | --- |
| Load | 4 / `e33f3e0c` | 11–13 | Local `data.csv`, ISO-8859-1; saved five-row preview |
| Clean | 6 / `6678cd43` | 16–19 | Drop missing CustomerID/Description; exclude uppercase C; positive quantity |
| Select and basket | 8 / `37cb3381` | 22–29 | Global description counts, top 100; UK; invoice sums; binary; at least two descriptions |
| Apriori | 10 / `c7a26fb4` | 32–36 | Boolean input; support .02; names; low memory; maximum length 3; ten-row preview |
| Rules | 12 / `e9595a4d` | 39–43 | Lift ≥ 1; sort lift then confidence descending; ten-row preview |
| Plot | 14 / `3d581d79` | 46–50 | Support/confidence scatter; size and hue encode lift |

Notebook execution counts are 71–77; kernel metadata says Python 3.11.9.
These are saved historical metadata, not proof of execution during this review.
The script contains unterminated string literals at lines 34–35 and 41–42.
An in-memory `ast.parse` fails at line 34. Each notebook code cell parses.

## Claims requiring correction in the starting README

| Starting claim | Inspection conclusion |
| --- | --- |
| Approximately 500,000 transactions | No local shape is saved; line items must be distinguished from invoices |
| Kaggle source | A README attribution, not an acquisition or checksum record |
| Top 100 purchased products | Top descriptions by cleaned line frequency across all countries, not units or UK invoice frequency |
| Single-item removal is only a performance step | It changes the transaction population and all metric denominators |
| Support .02 excludes statistically insignificant combinations | Frequency threshold; no significance test is implemented |
| Rules ranked by all three metrics | Actual sorting uses lift, then confidence; support is not a sort key |
| Complete validation / actionable outcomes | No price, duplicate, identifier, holdout, or business-impact validation |
| `data/`, `notebooks/` and old clone target | Neither directory exists; actual entry points are in the repository root |
| Python 3.8+ and completed status | No tested version range; standalone script cannot parse |

No exact raw shape, full date range, cleaning counts, basket dimensions, total
itemsets, or total rules can be recovered reliably from the saved previews.
DataFrame row labels must not be treated as totals. Truncated product names
must not be reconstructed from context.
