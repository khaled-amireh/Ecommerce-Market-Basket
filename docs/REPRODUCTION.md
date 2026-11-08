# Reproduction and troubleshooting

## Review without modifying evidence

Open [the tracked notebook](../ecommerce_market_basket.ipynb) to inspect saved
outputs. Do not execute and save it in the preservation checkout. The script
has confirmed syntax errors at lines 34–35 and 41–42; this documentation does
not repair them. The notebook's seven code cells parse, but end-to-end execution
was not attempted. Mining and dependency installation were not performed here.

## Prepare an independent environment

Run these commands in a separate working directory:

```bash
git clone https://github.com/khaled-amireh/Ecommerce-Market-Basket.git
cd Ecommerce-Market-Basket
python -m venv .venv
```

PowerShell activation:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux activation:

```bash
source .venv/bin/activate
```

Install the existing manifest and additional notebook tooling:

```bash
python -m pip install -r requirements.txt
python -m pip install notebook ipykernel
python -m ipykernel install --user --name market-basket --display-name "Market Basket"
python -m notebook ecommerce_market_basket.ipynb
```

Choose the registered Market Basket kernel. The notebook records Python 3.11.9,
but the original package versions are unknown. These commands are a preparation
recipe, not a tested historical environment. `DataFrame.map` needs pandas 2.1+
([official API](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.map.html));
that minimum alone is not a complete compatibility specification.

Obtain root-level `data.csv` following [the provenance guide](DATA_PROVENANCE.md).
The loader expects a CSV compatible with ISO-8859-1 and the eight columns in
[the feature dictionary](DATA_DICTIONARY.md). Match the working directory to the
repository root, verify the input checksum, then run notebook cells in order in
the disposable clone. Saving after execution changes the notebook evidence.

## Troubleshooting map

| Symptom | Likely cause / evidence | Next step in an independent reproduction |
| --- | --- | --- |
| Script SyntaxError before any output | Broken print literals, AUD-01 | Use notebook for inspection; repair script only in authorized code work |
| `data.csv` not found | CSV is absent or working directory differs | Acquire correct CSV and confirm root working directory |
| Unicode or column errors | Wrong distribution, format, header, or encoding | Inspect actual input; do not rename Excel as CSV |
| DataFrame has no `map` attribute | pandas predates the required API | Check pandas version in the selected kernel |
| Missing `association_rules` argument or changed behavior | Unpinned mlxtend API compatibility | Inspect installed version/signature and recover a tested environment |
| Empty frequent-itemset error | No eligible baskets or no sets above threshold | Inspect upstream populations before changing parameters |
| Empty or unexpected plot | No qualifying rules, kernel state, or different input | Inspect complete rules and stage counts; do not infer totals from pixels |
| Installed package unavailable in notebook | Wrong kernel interpreter | Select the registered virtual-environment kernel |
| Root PNG differs from README image | Script exports to current directory | Compare provenance; tracked image is under `images/` |

Do not silently change support, filters, or product ranking to make a run
produce attractive results. A changed configuration is a new experiment.

## Evidence to retain after a future run

Record input checksum and provenance, Python/package versions, ordered execution,
row and invoice counts after each filter, exact selected descriptions, basket
shape/dtypes, support denominator, full frequent itemsets and rules, metric
definitions, timings, and chart export path. Check the visible teacup rule against
[the historical ledger](VERIFIED_RESULTS.md), allowing for display rounding.
Differences should be investigated, not edited into the old outputs.

Package manifests, data, and results in this repository remain unchanged.
