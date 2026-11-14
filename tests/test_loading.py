from pathlib import Path
import tempfile
import unittest

from ecommerce_market_basket import load_transactions
from tests.fixtures import transactions


class LoadingTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / 'input.csv'

    def test_missing_file_names_path_and_remedy(self):
        with self.assertRaisesRegex(FileNotFoundError, 'original input CSV') as error:
            load_transactions(self.path)
        self.assertIn(str(self.path), str(error.exception))

    def test_directory_is_not_csv(self):
        with self.assertRaises(FileNotFoundError):
            load_transactions(self.path.parent)

    def test_empty_file(self):
        self.path.write_bytes(b'')
        with self.assertRaisesRegex(ValueError, 'empty'):
            load_transactions(self.path)

    def test_malformed_csv(self):
        self.path.write_text('InvoiceNo,Description\n"unterminated')
        with self.assertRaisesRegex(ValueError, 'Malformed'):
            load_transactions(self.path)

    def test_incompatible_encoding(self):
        self.path.write_bytes(b'\xff\xfe')
        with self.assertRaisesRegex(ValueError, 'Cannot decode'):
            load_transactions(self.path, encoding='utf-8')

    def test_unknown_encoding(self):
        transactions().to_csv(self.path, index=False)
        with self.assertRaisesRegex(ValueError, 'Unknown CSV encoding'):
            load_transactions(self.path, encoding='not-an-encoding')

    def test_latin1_default_preserves_description(self):
        df = transactions()
        df.loc[0, 'Description'] = 'CAFÉ'
        df.to_csv(self.path, index=False, encoding='ISO-8859-1')
        self.assertEqual(load_transactions(self.path).loc[0, 'Description'], 'CAFÉ')

    def test_missing_schema_propagates(self):
        self.path.write_text('InvoiceNo\n1\n')
        with self.assertRaisesRegex(ValueError, 'Missing required columns'):
            load_transactions(self.path)

    def test_leading_zero_invoice_ids_remain_distinct(self):
        transactions([('001', 'A'), ('1', 'B')]).to_csv(self.path, index=False)
        self.assertEqual(load_transactions(self.path).InvoiceNo.tolist(), ['001', '1'])
