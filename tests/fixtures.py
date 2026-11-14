"""Small invented transactions; never a substitute for the historical CSV."""
import pandas as pd


def transactions(rows=None):
    if rows is None:
        rows = [('1', 'A'), ('1', 'B'), ('2', 'A'), ('2', 'C')]
    return pd.DataFrame([
        dict(InvoiceNo=invoice, StockCode=description, Description=description,
             Quantity=1, InvoiceDate='2010-12-01', UnitPrice=2.5,
             CustomerID=123, Country='United Kingdom')
        for invoice, description in rows
    ])
