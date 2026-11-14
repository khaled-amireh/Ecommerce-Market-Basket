import unittest

import numpy as np
import pandas as pd

from ecommerce_market_basket import validate_transactions
from tests.fixtures import transactions


class InputTests(unittest.TestCase):
    def test_each_required_column_is_checked(self):
        df = transactions()
        for column in df.columns:
            with self.subTest(column=column), self.assertRaisesRegex(ValueError, column):
                validate_transactions(df.drop(columns=column))

    def test_header_only_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'no rows'):
            validate_transactions(transactions().iloc[:0])

    def test_numeric_strings_are_converted_without_mutation(self):
        df = transactions().astype({'Quantity': str, 'UnitPrice': str})
        original = df.copy(deep=True)
        result = validate_transactions(df)
        self.assertEqual(result.Quantity.tolist(), [1] * 4)
        self.assertEqual(result.UnitPrice.tolist(), [2.5] * 4)
        pd.testing.assert_frame_equal(df, original)

    def test_invalid_quantities_and_prices_are_rejected(self):
        for column in ['Quantity', 'UnitPrice']:
            for value in ['invalid', '', np.nan, np.inf, -np.inf]:
                df = transactions().astype({column: object})
                df.loc[0, column] = value
                with self.subTest(column=column, value=value):
                    with self.assertRaisesRegex(ValueError, column):
                        validate_transactions(df)

    def test_nonpositive_prices_are_not_a_population_filter(self):
        df = transactions()
        df.loc[0, 'UnitPrice'] = 0
        df.loc[1, 'UnitPrice'] = -1
        self.assertEqual(len(validate_transactions(df)), 4)

    def test_boolean_quantity_is_not_a_count(self):
        df = transactions()
        df['Quantity'] = True
        with self.assertRaisesRegex(ValueError, 'Quantity'):
            validate_transactions(df)

    def test_missing_invoice_cannot_become_a_shared_basket(self):
        for value in [None, np.nan, '', '   ']:
            df = transactions()
            df.loc[0, 'InvoiceNo'] = value
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, 'InvoiceNo'):
                validate_transactions(df)

    def test_nontext_labels_are_rejected(self):
        for column in ['Description', 'Country']:
            df = transactions().astype({column: object})
            df.loc[0, column] = 7
            with self.subTest(column=column), self.assertRaisesRegex(ValueError, column):
                validate_transactions(df)

    def test_complex_and_nullable_missing_quantities_are_rejected(self):
        for values in [[1j] * 4, pd.array([1, 1, 1, None], dtype='Int64')]:
            df = transactions()
            df['Quantity'] = values
            with self.assertRaisesRegex(ValueError, 'Quantity'):
                validate_transactions(df)
