# Input and derived feature dictionary

All eight input columns are visible in saved notebook cell 4. Meanings below
follow the [source schema](https://archive.ics.uci.edu/dataset/352/online+retail);
the implementation-use column is verified from notebook cells 6–12.
Input dtypes are inferred by `read_csv`; no explicit dtype contract is stored.

| Column | Meaning | Actual implementation use | Validation boundary |
| --- | --- | --- | --- |
| `InvoiceNo` | Invoice identifier; cancellation prefix convention | Cast to string, uppercase-C exclusion, basket row key | No null, uniqueness-across-customers, or formatting checks |
| `StockCode` | Product identifier | Loaded and previewed only | No code-to-description mapping validation |
| `Description` | Product name | Null exclusion, global frequency selection, basket column key | Whitespace, case, and aliases preserved |
| `Quantity` | Units on a line | Keep positive values, sum within invoice/description | No explicit numeric coercion or finite-value assertion |
| `InvoiceDate` | Invoice timestamp | Loaded and previewed only | No datetime parsing, range check, or temporal split |
| `UnitPrice` | Price per unit, source denomination sterling | Loaded and previewed only | No positive-price check; no revenue weighting |
| `CustomerID` | Customer identifier | Null exclusion only | Not a grouping key, model feature, or personalization input |
| `Country` | Customer country | Exact match to `United Kingdom` | No trim, alias normalization, or per-invoice consistency check |

## Derived objects

| Object | Grain / content | Interpretation |
| --- | --- | --- |
| `df` after cleaning | Surviving invoice lines across countries | Already excludes anonymous/missing-description rows |
| `top_products` | Up to 100 exact description strings | Ranked by surviving row counts, not units |
| `df_filtered` | Lines with selected descriptions | Still includes multiple countries |
| `basket` | Invoice × description quantity sums for UK | Dense pivot with zero for absent pairs |
| `basket_sets` | 0/1 matrix, ≥ 2 present descriptions per row | Mining population after projection and exclusion |
| `frequent_itemsets` | Support and immutable description sets | Sorted by support; entire table passed to rule generation |
| `rules` | Antecedent, consequent, and metrics | Lift-filtered; sorted by lift then confidence |

No derived object is exported as a full table. A DataFrame row index in a saved
preview is an inherited label, not a product identifier or a count. Descriptions
with trailing spaces remain literal keys; trimming them in documentation would
hide a possible product-identity issue.
