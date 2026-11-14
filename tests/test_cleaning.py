import unittest

import pandas as pd

from ecommerce_market_basket import clean_transactions
from tests.fixtures import transactions


class CleaningTests(unittest.TestCase):
    def test_valid_lines_and_caller_are_preserved(self):
        df = transactions()
        original = df.copy(deep=True)
        pd.testing.assert_frame_equal(clean_transactions(df), original)
        pd.testing.assert_frame_equal(df, original)

    def test_missing_customer_or_description_is_excluded(self):
        df = transactions()
        df.loc[0, 'CustomerID'] = float('nan')
        df.loc[1, 'Description'] = None
        self.assertEqual(clean_transactions(df).index.tolist(), [2, 3])

    def test_cancellations_and_nonpositive_quantities(self):
        df = transactions()
        df.loc[0, 'InvoiceNo'] = 'C1'
        df.loc[1, 'Quantity'] = -1
        df.loc[2, 'Quantity'] = 0
        self.assertEqual(clean_transactions(df).index.tolist(), [3])

    def test_original_sale_not_reconciled_with_return(self):
        df = transactions([('1', 'A'), ('C1', 'A')])
        df.loc[1, 'Quantity'] = -1
        self.assertEqual(clean_transactions(df).InvoiceNo.tolist(), ['1'])

    def test_duplicate_lines_are_retained(self):
        df = transactions([('1', 'A'), ('1', 'A')])
        self.assertEqual(len(clean_transactions(df)), 2)

    def test_case_whitespace_country_and_price_policies_remain_literal(self):
        df = transactions([('c1', ' A '), (' C2', 'A'), ('3', 'a')])
        df.loc[0, 'Country'] = ' United Kingdom '
        df.loc[0, 'UnitPrice'] = 0
        df.loc[1, 'UnitPrice'] = -1
        result = clean_transactions(df)
        self.assertEqual(result.InvoiceNo.tolist(), ['c1', ' C2', '3'])
        self.assertEqual(result.Description.tolist(), [' A ', 'A', 'a'])
        self.assertEqual(result.Country.iloc[0], ' United Kingdom ')
