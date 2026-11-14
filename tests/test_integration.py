from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

from ecommerce_market_basket import (build_baskets, clean_transactions, generate_rules,
                                     mine_itemsets, run_analysis)
from tests.fixtures import transactions


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        # AB, AB, AC, CD; then a singleton, cancellation and anonymous line.
        self.df = transactions([('1', 'A'), ('1', 'B'), ('2', 'A'), ('2', 'B'),
                                ('3', 'A'), ('3', 'C'), ('4', 'C'), ('4', 'D'),
                                ('5', 'A'), ('C6', 'A'), ('7', 'B')])
        self.df.loc[10, 'CustomerID'] = float('nan')

    def test_complete_pipeline_has_hand_calculated_population_and_rule(self):
        cleaned = clean_transactions(self.df)
        self.assertEqual(len(cleaned), 9)
        baskets = build_baskets(cleaned)
        self.assertEqual(baskets.index.tolist(), ['1', '2', '3', '4'])
        rules = generate_rules(mine_itemsets(baskets))
        ab = rules[(rules.antecedents == frozenset('A')) & (rules.consequents == frozenset('B'))].iloc[0]
        self.assertAlmostEqual(ab.support, 2/4)
        self.assertAlmostEqual(ab.confidence, 2/3)
        self.assertAlmostEqual(ab.lift, 4/3)

    def test_valid_fixture_matches_preserved_notebook_computation(self):
        notebook = json.loads((Path(__file__).resolve().parents[1] /
                               'ecommerce_market_basket.ipynb').read_text(encoding='utf-8'))
        namespace = {'df': self.df.copy(deep=True), 'pd': pd,
                     'apriori': apriori, 'association_rules': association_rules}
        for index in [6, 8, 10, 12]:
            exec(compile(''.join(notebook['cells'][index]['source']), f'notebook-cell-{index}', 'exec'), namespace)
        baskets = build_baskets(clean_transactions(self.df))
        pd.testing.assert_frame_equal(baskets.astype(int), namespace['basket_sets'])
        itemsets = mine_itemsets(baskets)
        pd.testing.assert_frame_equal(itemsets, namespace['frequent_itemsets'])
        pd.testing.assert_frame_equal(generate_rules(itemsets), namespace['rules'])

    def test_csv_workflow_reports_counts_without_plotting(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'synthetic.csv'
            self.df.to_csv(path, index=False)
            output = io.StringIO()
            with redirect_stdout(output), patch('ecommerce_market_basket.plot_rules') as plot:
                run_analysis(path, no_plot=True)
            plot.assert_not_called()
            self.assertIn('Loaded: 11 rows, 7 invoices.', output.getvalue())
            self.assertIn('Cleaned: 9 rows, 5 invoices.', output.getvalue())
            self.assertIn('Eligible baskets: 4;', output.getvalue())

    def test_all_rows_cleaned_out_fails_with_population_message(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'cancelled.csv'
            transactions([('C1', 'A')]).to_csv(path, index=False)
            with redirect_stdout(io.StringIO()), self.assertRaisesRegex(ValueError, 'No eligible baskets'):
                run_analysis(path, no_plot=True)

    def test_empty_itemsets_and_rules_skip_plot(self):
        cases = [(pd.DataFrame(columns=['support', 'itemsets']), 'No frequent itemsets'),
                 (pd.DataFrame({'support': [.5], 'itemsets': [frozenset('A')]}), 'No association rules')]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'synthetic.csv'
            self.df.to_csv(path, index=False)
            for itemsets, message in cases:
                output = io.StringIO()
                with self.subTest(message=message), redirect_stdout(output):
                    with patch('ecommerce_market_basket.mine_itemsets', return_value=itemsets):
                        with patch('ecommerce_market_basket.plot_rules') as plot:
                            run_analysis(path)
                            plot.assert_not_called()
                self.assertIn(message, output.getvalue())
