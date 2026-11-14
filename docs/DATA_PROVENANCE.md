# Dataset provenance and acquisition

> **Phase 2 update (2026-11-14):** The historical CSV remains absent. No external data was acquired. The CLI now accepts an explicit CSV path and encoding; its default input is data.csv beside the script. Tests create temporary synthetic CSVs only. ISO-8859-1 remains the default and decodes arbitrary byte values, so successful decoding does not establish correct encoding or source identity.
> See [verified corrections](PHASE2_CHANGES.md). The original review below describes
> the preserved notebook and Phase 1 script; its script line numbers are historical.

## What is actually recorded

[Notebook](../ecommerce_market_basket.ipynb) cell 4, source line 1, and
[script](../ecommerce_market_basket.py#L11) line 11 read `data.csv` relative to
the working directory with ISO-8859-1 encoding. There is no download, version
identifier, checksum, schema assertion, or completeness check. The starting
README names [Kaggle E-Commerce Data](https://www.kaggle.com/datasets/carrie1/ecommerce-data).
That attribution is preserved, but the Kaggle page did not expose readable
dataset metadata to the web inspection on 2026-11-08.

The related [UCI record](https://archive.ics.uci.edu/dataset/352/online+retail)
provides a source reference: 541,909 records, eight schema variables, coverage
from 1 December 2010 to 9 December 2011, and an Excel distribution. UCI credits
Daqing Chen and lists CC BY 4.0. These describe that source distribution only.
The repository's MIT license does not relicense third-party data.

## Local evidence and its limits

| Question | Evidence | Confidence boundary |
| --- | --- | --- |
| Which input was opened historically? | Saved cell 4 shows the first five rows | Filename is recorded; file identity is not |
| Is its schema compatible with Online Retail? | Eight preview column names match the source schema | Schema agreement does not establish file identity |
| How many local records? | No `shape` or full dataset | Unknown |
| What dates were actually loaded? | Preview shows `12/1/2010 8:26` | No parsed date extrema or range validation |
| How much missing data? | Cleaning calls `dropna` on two fields | No saved null counts |
| Are all source records present? | No input checksum or acquisition manifest | Unverified |

## Acquisition for a future independent reproduction

Download the CSV from the attributed Kaggle distribution after reviewing its
current terms. In a disposable checkout, extract the actual CSV as root-level
`data.csv`; verify its header before execution. Keep any input outside this
preservation-only documentation change.

Record the distribution URL/version, retrieval date, original filename, byte
size, SHA-256, row/column count, null counts, parsed date range, and any conversion
steps. Compare preview rows, but never use a five-row match as a checksum.

The UCI download is Excel: renaming it `data.csv` does not convert it. Any Excel
conversion would require documented encoding, identifier handling, date formatting,
and equivalence checks. No conversion or new dataset was created in this review.

Suggested dataset citation: Chen, D. (2015), *Online Retail*, UCI Machine Learning
Repository, [DOI 10.24432/C5BW33](https://doi.org/10.24432/C5BW33). Confirm the
relationship to the acquired CSV before asserting this as its verified origin.
