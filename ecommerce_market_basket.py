# E-Commerce Market Basket Analysis using Apriori Algorithm

# Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.frequent_patterns import apriori, association_rules

# Load Dataset
df = pd.read_csv('data.csv', encoding='ISO-8859-1')
print("Dataset Head:")
print(df.head())

# Data Preprocessing & Cleaning
df = df.dropna(subset=['CustomerID', 'Description'])
df['InvoiceNo'] = df['InvoiceNo'].astype(str)
df = df[~df['InvoiceNo'].str.startswith('C')]
df = df[df['Quantity'] > 0]

# Constructing the Transaction Basket Matrix
top_products = df['Description'].value_counts().head(100).index
df_filtered = df[df['Description'].isin(top_products)]

basket = (df_filtered[df_filtered['Country'] == 'United Kingdom']
          .groupby(['InvoiceNo', 'Description'])['Quantity']
          .sum().unstack().fillna(0))
basket_sets = basket.map(lambda x: 1 if x > 0 else 0)
basket_sets = basket_sets[(basket_sets.sum(axis=1) >= 2)]

# Apriori Algorithm & Frequent Itemsets Mining
frequent_itemsets = apriori(basket_sets.astype(bool), min_support=0.02, use_colnames=True, low_memory=True, max_len=3)
frequent_itemsets = frequent_itemsets.sort_values(by='support', ascending=False)
print("
Top Frequent Itemsets:")
print(frequent_itemsets.head(10))

# Extracting Association Rules
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)
rules = rules.sort_values(by=['lift', 'confidence'], ascending=[False, False])
print("
Top Association Rules:")
print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(10))

# Visualizing Association Rules
plt.figure(figsize=(8, 5))
sns.scatterplot(data=rules, x='support', y='confidence', size='lift', hue='lift', palette='viridis')
plt.title('Association Rules')
plt.savefig('association_rules_plot.png')
plt.show()
