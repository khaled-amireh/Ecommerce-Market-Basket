# E-Commerce Market Basket Analysis using Apriori Algorithm

# Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from mlxtend.frequent_patterns import apriori, association_rules


REQUIRED_COLUMNS = (
    'InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate',
    'UnitPrice', 'CustomerID', 'Country',
)


def validate_transactions(df):
    """Validate the input contract without filtering or normalizing labels."""
    missing = sorted(set(REQUIRED_COLUMNS) - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    if df.empty:
        raise ValueError('Transaction input contains no rows.')
    result = df.copy()
    invoice = result['InvoiceNo'].astype('string')
    if invoice.isna().any() or invoice.str.strip().eq('').any():
        raise ValueError('InvoiceNo must be nonmissing and nonblank; unknown invoices cannot be grouped safely.')
    for column in ('Description', 'Country'):
        nonmissing = result[column].dropna()
        if not nonmissing.map(lambda value: isinstance(value, str)).all():
            raise ValueError(f'{column} must contain text labels or missing values.')
    for column in ('Quantity', 'UnitPrice'):
        try:
            numeric = pd.to_numeric(result[column], errors='raise')
        except (TypeError, ValueError) as exc:
            raise ValueError(f'{column} must contain finite numeric values.') from exc
        if (result[column].map(lambda value: isinstance(value, (bool, np.bool_))).any()
                or pd.api.types.is_complex_dtype(numeric)
                or numeric.isna().any() or not np.isfinite(numeric).all()):
            raise ValueError(f'{column} must contain finite numeric values.')
        result[column] = numeric
    return result


def load_transactions(path='data.csv', encoding='ISO-8859-1'):
    """Load an explicitly supplied CSV; never substitute a sample dataset."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(
            f'Transaction CSV not found: {path.resolve()}. '
            'Supply the original input CSV; the historical data is not bundled.'
        )
    try:
        df = pd.read_csv(path, encoding=encoding, dtype={'InvoiceNo': 'string'})
    except pd.errors.EmptyDataError as exc:
        raise ValueError(f'Transaction CSV is empty: {path}') from exc
    except pd.errors.ParserError as exc:
        raise ValueError(f'Malformed transaction CSV: {path}: {exc}') from exc
    except UnicodeDecodeError as exc:
        raise ValueError(f'Cannot decode {path} using {encoding}; specify its actual encoding.') from exc
    except LookupError as exc:
        raise ValueError(f'Unknown CSV encoding: {encoding}') from exc
    return validate_transactions(df)


def clean_transactions(df):
    """Preserve the historical positive-line, known-customer population."""
    df = validate_transactions(df)
    # Data Preprocessing & Cleaning
    df = df.dropna(subset=['CustomerID', 'Description'])
    df['InvoiceNo'] = df['InvoiceNo'].astype(str)
    df = df[~df['InvoiceNo'].str.startswith('C')]
    df = df[df['Quantity'] > 0]

    return df.copy()


def build_baskets(df):
    """Project cleaned rows onto global top-100 labels, then UK multi-item invoices."""
    # Constructing the Transaction Basket Matrix
    top_products = df['Description'].value_counts().head(100).index
    df_filtered = df[df['Description'].isin(top_products)]

    basket = (df_filtered[df_filtered['Country'] == 'United Kingdom']
              .groupby(['InvoiceNo', 'Description'])['Quantity']
              .sum().unstack().fillna(0))
    basket_sets = basket.gt(0)
    basket_sets = basket_sets[(basket_sets.sum(axis=1) >= 2)]

    return basket_sets


def mine_itemsets(baskets, min_support=0.02):
    """Mine complete itemsets up to length three over eligible baskets."""
    if baskets.empty:
        raise ValueError('No eligible baskets: require UK invoices with at least two selected descriptions.')
    if not baskets.columns.is_unique:
        raise ValueError('Basket description columns must be unique.')
    if baskets.isna().any().any() or not baskets.isin([0, 1]).all().all():
        raise ValueError('Basket values must be Boolean or binary 0/1 presence indicators.')
    if isinstance(min_support, bool) or not 0 < min_support <= 1:
        raise ValueError('min_support must be greater than 0 and at most 1.')
    itemsets = apriori(baskets.astype(bool), min_support=min_support,
                       use_colnames=True, low_memory=True, max_len=3)
    return itemsets.sort_values(by='support', ascending=False)


def generate_rules(itemsets):
    """Retain lift >= 1 and rank numerically by lift, then confidence."""
    rules = association_rules(itemsets, metric='lift', min_threshold=1.0)
    return rules.sort_values(by=['lift', 'confidence'], ascending=[False, False])


def main():
    # Load Dataset
    df = load_transactions()
    print("Dataset Head:")
    print(df.head())

    df = clean_transactions(df)

    basket_sets = build_baskets(df)

    frequent_itemsets = mine_itemsets(basket_sets)
    print("\nTop Frequent Itemsets:")
    print(frequent_itemsets.head(10))

    rules = generate_rules(frequent_itemsets)
    print("\nTop Association Rules:")
    print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(10))

    # Visualizing Association Rules
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=rules, x='support', y='confidence', size='lift', hue='lift', palette='viridis')
    plt.title('Association Rules')
    plt.savefig('association_rules_plot.png')
    plt.show()


if __name__ == "__main__":
    main()
