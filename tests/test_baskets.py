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

    def test_global_top100_uses_lines_not_uk_invoices_or_units(self):
        # 99 foreign labels each have four lines. A has three repeated lines
        # on one UK invoice; B has two UK invoices and far more units.
        rows = [(f'F{i}', f'foreign-{i}') for i in range(99) for _ in range(4)]
        rows += [('1', 'A')] * 3 + [('1', 'B'), ('2', 'B')]
        df = transactions(rows)
        df.loc[:395, 'Country'] = 'France'
        df.loc[df.Description.eq('B'), 'Quantity'] = 100
        basket = build_baskets(df)
        self.assertEqual(basket.columns.tolist(), ['A'])
        # The original A+B invoice becomes a selected singleton and vanishes.
        self.assertTrue(basket.empty)

    def test_singleton_policy_changes_support_denominator(self):
        df = transactions([('1', 'A'), ('1', 'B'), ('2', 'A'), ('3', 'C')])
        basket = build_baskets(df)
        self.assertEqual(len(basket), 1)  # Three original invoices, one eligible.
        self.assertEqual(basket[['A', 'B']].all(axis=1).mean(), 1.0)
        # Joint support would be 1/3 with all three invoices retained.

    def test_customer_invoices_stay_separate_observations(self):
        df = transactions([('1', 'A'), ('1', 'B'), ('2', 'A'), ('2', 'B')])
        self.assertEqual(build_baskets(df).index.tolist(), ['1', '2'])
