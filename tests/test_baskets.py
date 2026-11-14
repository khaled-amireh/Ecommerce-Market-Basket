import unittest

import pandas as pd

from ecommerce_market_basket import build_baskets, clean_transactions
from tests.fixtures import transactions


class BasketTests(unittest.TestCase):
    def test_invoice_grouping_repeated_lines_and_boolean_presence(self):
        df = transactions([('1', 'A'), ('1', 'A'), ('1', 'B'), ('2', 'B'), ('2', 'C')])
        df.loc[0, 'Quantity'] = 20
        result = build_baskets(clean_transactions(df))
        expected = pd.DataFrame([[True, True, False], [False, True, True]],
                                index=pd.Index(['1', '2'], name='InvoiceNo'),
                                columns=pd.Index(['A', 'B', 'C'], name='Description'))
        pd.testing.assert_frame_equal(result, expected)

    def test_singletons_are_excluded_by_distinct_selected_labels(self):
        df = transactions([('1', 'A'), ('1', 'B'), ('2', 'A'), ('2', 'A')])
        self.assertEqual(build_baskets(df).index.tolist(), ['1'])

    def test_country_match_is_exact(self):
        df = transactions()
        df.loc[2:, 'Country'] = ' United Kingdom '
        self.assertEqual(build_baskets(df).index.tolist(), ['1'])

    def test_whitespace_descriptions_are_distinct(self):
        df = transactions([('1', 'A'), ('1', 'A ')])
        self.assertEqual(build_baskets(df).columns.tolist(), ['A', 'A '])

    def test_empty_cleaned_input_and_absent_country(self):
        for df in [transactions().iloc[:0], transactions().assign(Country='France')]:
            with self.subTest(rows=len(df)):
                self.assertTrue(build_baskets(df).empty)

    def test_only_singletons_is_empty(self):
        self.assertTrue(build_baskets(transactions([('1', 'A'), ('2', 'B')])).empty)
