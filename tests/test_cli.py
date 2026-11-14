import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

from ecommerce_market_basket import plot_rules
from tests.fixtures import transactions

SCRIPT = Path(__file__).resolve().parents[1] / 'ecommerce_market_basket.py'


class CliTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def run_cli(self, *arguments):
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, arguments)],
                              cwd=self.root, capture_output=True, text=True, timeout=30,
                              env={**os.environ, 'MPLBACKEND': 'Agg'})

    def test_help_is_available_without_dataset(self):
        result = self.run_cli('--help')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('--no-plot', result.stdout)

    def test_missing_input_exits_cleanly(self):
        result = self.run_cli(self.root / 'missing.csv', '--no-plot')
        self.assertEqual(result.returncode, 2)
        self.assertIn('Transaction CSV not found', result.stderr)
        self.assertNotIn('Traceback', result.stderr)

    def test_explicit_input_runs_from_other_working_directory(self):
        path = self.root / 'synthetic.csv'
        transactions().to_csv(path, index=False)
        result = self.run_cli(path, '--no-plot')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Top Association Rules', result.stdout)
        self.assertFalse((self.root / 'association_rules_plot.png').exists())

    def test_no_show_exports_new_png_and_closes_figure(self):
        rules = pd.DataFrame({'support': [.25, .5], 'confidence': [.5, .75], 'lift': [1.5, 2]})
        output = self.root / 'new.png'
        before = plt.get_fignums()
        plot_rules(rules, output, show=False)
        self.assertEqual(output.read_bytes()[:8], b'\x89PNG\r\n\x1a\n')
        self.assertGreater(plt.imread(output).shape[0], 0)
        self.assertEqual(plt.get_fignums(), before)

    def test_existing_output_is_never_overwritten(self):
        output = self.root / 'protected.png'
        output.write_bytes(b'historical evidence')
        rules = pd.DataFrame({'support': [.5], 'confidence': [.5], 'lift': [1]})
        with self.assertRaisesRegex(FileExistsError, 'Choose a new'):
            plot_rules(rules, output, show=False)
        self.assertEqual(output.read_bytes(), b'historical evidence')
