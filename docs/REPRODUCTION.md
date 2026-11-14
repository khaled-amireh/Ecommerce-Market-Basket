# Reproduction and troubleshooting

## Evidence boundary

The standalone script is repaired and tested with synthetic input. The original
CSV is absent, and the saved notebook metrics have not been independently
reproduced. Inspect the notebook without executing/saving it. Use a separate
copy for any future historical experiment. See [technical changes](PHASE2_CHANGES.md),
[validation evidence](VALIDATION.md) and [dataset provenance](DATA_PROVENANCE.md).

## Prepare an independent environment

```bash
git clone https://github.com/khaled-amireh/Ecommerce-Market-Basket.git
cd Ecommerce-Market-Basket
python -m venv .venv
```

The repair commits are local and have not been pushed. A fresh remote clone will
not contain them until the owner separately publishes them. To validate these
changes now, use this local branch/worktree, or copy it to a disposable location.

PowerShell activation:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux activation:

```bash
source .venv/bin/activate
```

Install runtime packages and validate the repaired local checkout:

```bash
python -m pip install -r requirements.txt
python -m py_compile ecommerce_market_basket.py
python -m unittest discover -s tests -v
python ecommerce_market_basket.py --help
```

No pytest or notebook installation is required for the tests. The tested Python
and package versions are recorded in VALIDATION.md; the historical package
versions remain unknown. An unpinned fresh installation may differ from the
tested stack. No arbitrary compatibility bounds or major upgrades were added.

## Supply the actual input

Follow the provenance guide to identify an authorized CSV snapshot and record
its checksum, retrieval/version metadata, dimensions and date range. Do not
substitute a similarly named dataset or rename an Excel file to CSV.

All eight columns are required: InvoiceNo, StockCode, Description, Quantity,
InvoiceDate, UnitPrice, CustomerID, Country. The
[input dictionary](DATA_DICTIONARY.md) records validation versus unused fields.
Invoice IDs load as text; missing/blank IDs fail before grouping. Quantity and
UnitPrice must be finite real numbers (numeric strings are accepted). Nonmissing
Description/Country must be text. Validation rejects an invalid input file as a
whole, including invalid rows that historical cleaning might otherwise exclude.
UnitPrice signs are not filtered. Missing customer/description and nonpositive
quantity exclusions retain historical meaning.

Replace `/path/to/data.csv` with the actual input path; quote paths containing spaces:

```bash
python ecommerce_market_basket.py /path/to/data.csv --no-plot
python ecommerce_market_basket.py /path/to/data.csv --plot-output new_rules.png --no-show
```

The CLI default input is data.csv beside the script, independent of working
directory. An explicit relative input path is relative to the working directory.
The default encoding is ISO-8859-1; `--encoding utf-8` is available for an input
known to use UTF-8. Latin-1 decodes all bytes, so decoding success is not proof
of correct encoding. No automatic encoding fallback is applied.

The default plot is association_rules_plot.png in the working directory, distinct
from the historical images/association_rules_plot.png. Every existing plot path
is refused; choose a new filename for each run. --no-show exports without opening
a window; --no-plot skips both. No eligible baskets cause exit 2 with an explanation.
No frequent itemsets or qualifying rules are successful empty outcomes with an
explicit message and no plot. Support is .02, maximum length 3, low memory true;
rules require lift >= 1. No confidence cutoff is applied.

## Optional notebook review

In a disposable copy only:

```bash
python -m pip install notebook ipykernel
python -m ipykernel install --user --name market-basket --display-name "Market Basket"
python -m notebook ecommerce_market_basket.ipynb
```

Choose the intended kernel. The preserved notebook uses DataFrame.map, requiring
pandas 2.1+; the revised script uses vectorized gt(0). The notebook has the older
unchecked input path and cannot be assumed to have the script's validation or
empty/export guards. Never save a rerun over the original research evidence.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| Transaction CSV not found | Supply the exact authorized CSV path; data is absent from Git |
| Missing required columns | Check distribution, CSV header and delimiter; Excel needs actual conversion |
| Cannot decode / unknown encoding | Supply the actual file encoding; do not guess from filename |
| Nonfinite numeric field or missing invoice | Investigate source data; rejection is explicit, not silent filtering |
| No eligible baskets | Inspect cleaned UK population, global top-100 projection and singleton exclusion |
| No itemsets/rules | Inspect stage counts without changing thresholds to improve appearances |
| Plot output already exists | Choose a new --plot-output path; preserve prior outputs |
| Notebook missing map / API argument | Check installed environment and kernel; historical environment is unknown |
| Different historical metrics | Check input identity and environment; do not edit the saved metrics |

## Evidence for a future historical run

Retain the input checksum/acquisition record, Python/package versions, complete
stage counts and exclusion reasons, exact selected labels, basket dimensions and
support denominator, complete itemsets/rules, parameters and output paths.
The current script prints loaded/cleaned counts, basket width/count, parameters,
and itemset/rule counts plus previews; it does not export a full run manifest or
complete result tables. Record these separately for a scientific reproduction.
Compare with the [saved-result ledger](VERIFIED_RESULTS.md) without forcing a match.
