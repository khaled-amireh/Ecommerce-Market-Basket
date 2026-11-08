# Cleaning methodology and exclusions

Source: [notebook](../ecommerce_market_basket.ipynb) cell 6 (ID `6678cd43`),
source lines 1–4; [script](../ecommerce_market_basket.py#L16) lines 16–19.
The sequence is identical in both entry points. No removal counts are saved.

| Order | Implemented operation | What it guarantees | What it does not guarantee |
| --- | --- | --- | --- |
| 1 | `dropna(subset=['CustomerID', 'Description'])` | Surviving rows are non-null in these fields | Nonblank descriptions, valid IDs, complete invoices |
| 2 | `InvoiceNo.astype(str)` | Subsequent string operations are available | Missing invoice identifiers are rejected |
| 3 | Exclude `.str.startswith('C')` | Uppercase-C-prefixed rows are absent | Lowercase/whitespace variants or return reconciliation |
| 4 | Keep `Quantity > 0` | Nonpositive quantities cannot enter the basket sums | Valid price, unique lines, finite quantities, or net sales |

## Selection consequences

CustomerID is not used by the invoice-level miner, so dropping it is a population
choice rather than an algorithmic necessity. Invoices may be partially retained
if only some rows fail a filter. Therefore a surviving basket need not be a
complete representation of its original invoice.

Cancellation rows are removed independently. An original purchase later returned
is not removed by matching the return to its invoice. This is a positive-line
purchase analysis, without a demonstrated net-purchase ledger.

## Checks absent from the current implementation

There is no `drop_duplicates`, positive UnitPrice filter, description trimming,
StockCode reconciliation, invoice null check, or transaction consistency report.
These are confirmed omissions; the presence and prevalence of affected records
in the missing input remain unverified. Zero-price gifts, for example, should
not be called erroneous automatically: their inclusion needs an explicit policy.

Repeated positive lines become a single presence flag after aggregation, but
can still increase the global description row counts used for top-100 selection.
Deduplication would therefore require a data-specific definition, not blind
removal of every repeated description within an invoice.

## Future validation protocol, not implemented

In an authorized analysis change, retain per-step counts of rows and invoices,
missingness by field, rejected price/quantity categories, duplicate candidates,
and product mapping conflicts. Compare the final population with the baseline.
Any change to exclusions or product ranking needs new itemsets and rules; the
existing previews cannot be relabeled as results from corrected preprocessing.
