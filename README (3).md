# E-Commerce Market Basket Analysis using the Apriori Algorithm

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458)
![NumPy](https://img.shields.io/badge/NumPy-Numerical%20Computing-blue)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-blue)
![Seaborn](https://img.shields.io/badge/Seaborn-Visualization-3776AB)
![Mlxtend](https://img.shields.io/badge/Mlxtend-Association%20Rules-orange)

## Project Overview

Market Basket Analysis is a data mining technique used to discover
relationships between products that are frequently purchased together.

This project applies the **Apriori Algorithm** to a large e-commerce
transaction dataset containing approximately **500,000 transaction
records**. The main objective is to identify frequent product
combinations and generate meaningful association rules that can support
business decisions such as product bundling, cross-selling,
recommendation systems, inventory planning, and warehouse optimization.

The project follows an end-to-end data mining workflow, starting with
data cleaning and preprocessing, followed by transaction basket
construction, frequent itemset mining, association rule generation, and
visualization.

------------------------------------------------------------------------

## Problem Statement

E-commerce transaction datasets typically store purchases as individual
line items. Each invoice may contain multiple products, but the
relationships between these products are not directly visible.

For example, a transaction dataset may look like this:

  InvoiceNo   Description   Quantity
  ----------- ------------- ----------
  10001       Product A     2
  10001       Product B     1
  10002       Product A     1
  10002       Product C     3

Although the data records each purchased item separately, it does not
directly reveal patterns such as:

> Customers who purchase Product A are also likely to purchase Product
> B.

The purpose of this project is to transform transaction-level data into
a format suitable for association rule mining and discover hidden
purchasing patterns between products.

------------------------------------------------------------------------

## Dataset

The dataset used in this project is the **E-Commerce Data Dataset**,
which contains transaction records from an online retail store.

**Dataset Source:**\
[E-Commerce Data on
Kaggle](https://www.kaggle.com/datasets/carrie1/ecommerce-data)

### Dataset Characteristics

The dataset contains approximately:

-   500,000 transaction records
-   Thousands of unique products
-   Multiple customer transactions
-   Purchases from different countries

### Important Features

  Feature         Description
  --------------- ------------------------------------------
  `InvoiceNo`     Unique transaction or invoice identifier
  `StockCode`     Product identification code
  `Description`   Product name or description
  `Quantity`      Number of purchased units
  `InvoiceDate`   Date and time of the transaction
  `UnitPrice`     Price per product unit
  `CustomerID`    Unique customer identifier
  `Country`       Customer country

------------------------------------------------------------------------

## Data Preprocessing

Raw transaction data cannot be directly used with the Apriori algorithm.
Several preprocessing steps were required to transform the dataset into
transaction baskets.

### Handling Missing Values

Records containing missing values in important attributes were removed.

``` python
df = df.dropna(subset=['CustomerID', 'Description'])
```

`CustomerID` and `Description` are important for identifying valid
customer transactions and products.

### Removing Cancelled Transactions

Invoices starting with the letter `C` represent cancelled transactions.

These records were removed because they do not represent completed
purchases and could negatively affect the discovered association
patterns.

``` python
df['InvoiceNo'] = df['InvoiceNo'].astype(str)
df = df[~df['InvoiceNo'].str.startswith('C')]
```

### Removing Invalid Quantities

Transactions with zero or negative quantities were removed.

``` python
df = df[df['Quantity'] > 0]
```

This ensures that the analysis focuses only on products that were
actually purchased.

------------------------------------------------------------------------

## Product Filtering and Memory Optimization

The original dataset contains thousands of unique products.

Applying Apriori directly to all products would generate a very large
number of possible product combinations. This can significantly increase
computational complexity and memory consumption.

To make the algorithm more efficient, the analysis focuses on the most
frequently purchased products.

``` python
top_products = df['Description'].value_counts().head(100).index
df_filtered = df[df['Description'].isin(top_products)]
```

Reducing the number of unique products significantly decreases the
number of candidate itemsets generated by Apriori while preserving the
most common purchasing patterns.

This step is particularly important when working with large
transactional datasets.

------------------------------------------------------------------------

## Transaction Basket Matrix Construction

The Apriori algorithm requires transactions to be represented in a
basket format.

The data was grouped by:

-   `InvoiceNo`
-   `Description`

The purchased quantities were aggregated to create a transaction-product
matrix.

``` python
basket = (
    df_filtered[df_filtered['Country'] == 'United Kingdom']
    .groupby(['InvoiceNo', 'Description'])['Quantity']
    .sum()
    .unstack()
    .fillna(0)
)
```

Each row represents a transaction, while each column represents a
product.

Example:

  InvoiceNo   Product A   Product B   Product C
  ----------- ----------- ----------- -----------
  10001       2           1           0
  10002       1           0           3

------------------------------------------------------------------------

## Binary Encoding

The quantity values were converted into binary values.

If a product was purchased, it receives a value of `1`. Otherwise, it
receives a value of `0`.

``` python
basket_sets = basket.map(lambda x: 1 if x > 0 else 0)
```

For Apriori processing, the transaction matrix was converted to Boolean
values.

``` python
basket_sets = basket_sets.astype(bool)
```

------------------------------------------------------------------------

## Transaction Filtering

Transactions containing fewer than two distinct products were removed.

A transaction containing only one product cannot provide meaningful
information about relationships between products.

``` python
basket_sets = basket_sets[
    basket_sets.sum(axis=1) >= 2
]
```

This ensures that the analysis focuses on valid co-purchase behavior.

------------------------------------------------------------------------

## Frequent Itemset Mining using Apriori

The Apriori algorithm was used to identify combinations of products that
frequently appear together in transactions.

The implementation uses the `mlxtend` library.

``` python
from mlxtend.frequent_patterns import apriori, association_rules
```

Frequent itemsets were generated using the following configuration:

``` python
frequent_itemsets = apriori(
    basket_sets,
    min_support=0.02,
    use_colnames=True,
    low_memory=True,
    max_len=3
)
```

The itemsets were then sorted according to their support values.

``` python
frequent_itemsets = frequent_itemsets.sort_values(
    by='support',
    ascending=False
)

frequent_itemsets.head(10)
```

------------------------------------------------------------------------

## Apriori Configuration

The following configuration was selected to balance pattern discovery
with computational efficiency.

  -----------------------------------------------------------------------
  Parameter                    Value              Purpose
  ---------------------------- ------------------ -----------------------
  `min_support`                `0.02`             Removes infrequent
                                                  product combinations

  `use_colnames`               `True`             Displays product names
                                                  instead of column
                                                  indices

  `low_memory`                 `True`             Reduces memory
                                                  consumption

  `max_len`                    `3`                Limits itemset
                                                  combinations to a
                                                  maximum of three
                                                  products
  -----------------------------------------------------------------------

The dataset size and the number of unique products can make Apriori
computationally expensive.

Limiting the number of products, increasing the minimum support
threshold, enabling memory-efficient processing, and restricting itemset
length help reduce computational complexity and memory usage.

------------------------------------------------------------------------

## Association Rule Generation

After identifying frequent itemsets, association rules were generated
using the `association_rules` function.

``` python
rules = association_rules(
    frequent_itemsets,
    metric='lift',
    min_threshold=1.0
)
```

The rules describe relationships in the following format:

``` text
Product A -> Product B
```

This can be interpreted as:

> Customers who purchase Product A are also likely to purchase Product
> B.

------------------------------------------------------------------------

## Evaluation Metrics

The strength of the generated association rules was evaluated using
three main metrics:

-   Support
-   Confidence
-   Lift

### Support

Support measures how frequently an item or itemset appears across all
transactions.

**Support(A) = Transactions containing A / Total transactions**

A higher support value indicates that the product or product combination
appears frequently in the dataset.

### Confidence

Confidence measures the probability that a customer purchases Product B
when Product A has already been purchased.

**Confidence(A -\> B) = Support(A and B) / Support(A)**

For example, a confidence value of `0.70` means that approximately 70%
of transactions containing Product A also contain Product B.

### Lift

Lift measures the strength of the relationship between two products
compared with what would be expected if they were statistically
independent.

**Lift(A -\> B) = Confidence(A -\> B) / Support(B)**

Lift values can be interpreted as follows:

-   `Lift > 1` indicates a positive association between products.
-   `Lift = 1` indicates no meaningful association.
-   `Lift < 1` indicates a negative association.

Rules with higher lift values indicate stronger relationships between
products.

------------------------------------------------------------------------

## Rule Analysis

The generated association rules can be ranked and filtered based on
different evaluation metrics.

For example, rules can be sorted according to Lift:

``` python
rules = rules.sort_values(
    by='lift',
    ascending=False
)

rules.head(10)
```

High-lift rules with reasonable support and confidence are generally
more useful for business applications than rules that rely on only one
metric.

A rule with extremely high confidence but very low support may represent
a rare pattern and may not be useful for large-scale business decisions.

For this reason, association rules should be evaluated using multiple
metrics rather than relying on a single value.

------------------------------------------------------------------------

## Association Rules Visualization

The relationship between Support, Confidence, and Lift can be visualized
using a scatter plot.

The visualization represents:

-   The x-axis as Support.
-   The y-axis as Confidence.
-   Point size and color intensity as Lift.

This makes it easier to identify rules that combine:

-   Strong product association
-   High confidence
-   Meaningful transaction frequency

Add your generated visualization below:

``` markdown
![Association Rules Visualization](images/association_rules_plot.png)
```

------------------------------------------------------------------------

## Business Insights and Applications

The association rules discovered in this project can support several
e-commerce strategies.

### Product Bundling

Products with strong association rules can be grouped into promotional
bundles.

For example:

> Buy Product A and Product B together at a discounted price.

This can increase the Average Order Value and encourage customers to
purchase related products.

### Cross-Selling Recommendations

Association rules can be used to create product recommendation systems.

For example:

> Customers who bought this product also purchased...

These recommendations can be displayed on:

-   Product pages
-   Shopping carts
-   Checkout pages

### Personalized Marketing

Association patterns can support targeted marketing campaigns.

Customers who previously purchased a particular product may receive
recommendations for strongly associated products.

This can improve the relevance of marketing campaigns and product
recommendations.

### Inventory Planning

Frequently associated products can provide useful information for
inventory planning.

Products that are often purchased together may experience related demand
patterns.

Understanding these relationships can help businesses improve:

-   Stock planning
-   Product availability
-   Demand forecasting

### Warehouse Optimization

Products that are frequently purchased together can potentially be
stored closer to each other in fulfillment centers.

This may help reduce picking time and improve order processing
efficiency.

------------------------------------------------------------------------

## Key Challenges

One of the main challenges in this project was applying the Apriori
algorithm to a large transaction dataset.

Apriori can become computationally expensive because the number of
possible product combinations increases rapidly as the number of unique
products grows.

Memory consumption therefore becomes an important consideration when
working with large-scale transaction data.

Several strategies were used to reduce computational complexity:

-   Filtering the dataset to the most frequently purchased products
-   Removing invalid and cancelled transactions
-   Removing transactions with fewer than two products
-   Using a higher minimum support threshold
-   Enabling `low_memory=True`
-   Limiting itemset size using `max_len`

These steps allow the analysis to focus on meaningful purchasing
patterns while keeping memory usage and computational requirements
manageable.

------------------------------------------------------------------------

## Technologies Used

This project was developed using the following technologies and
libraries:

-   Python
-   Pandas
-   NumPy
-   Matplotlib
-   Seaborn
-   Mlxtend
-   Jupyter Notebook

------------------------------------------------------------------------

## Conclusion

This project demonstrates how raw e-commerce transaction data can be
transformed into meaningful business insights using Association Rule
Mining.

The complete workflow includes:

1.  Cleaning transaction records.
2.  Removing cancelled and invalid purchases.
3.  Reducing the product search space.
4.  Constructing a transaction basket matrix.
5.  Applying binary encoding.
6.  Filtering transactions for meaningful co-purchase analysis.
7.  Mining frequent itemsets using the Apriori algorithm.
8.  Generating association rules.
9.  Evaluating rules using Support, Confidence, and Lift.
10. Visualizing product relationships.
11. Translating discovered patterns into practical business
    recommendations.

The discovered association patterns can support practical e-commerce
applications such as product bundling, cross-selling, recommendation
systems, inventory planning, and warehouse optimization.

This project also demonstrates an important real-world aspect of data
mining: algorithm performance and memory constraints must be considered
when working with large-scale transactional datasets.
