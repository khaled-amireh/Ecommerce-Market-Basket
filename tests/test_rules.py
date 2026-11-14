import unittest

import pandas as pd

from ecommerce_market_basket import generate_rules, mine_itemsets


class RuleTests(unittest.TestCase):
    def test_independent_joint_support_direction_confidence_and_lift(self):
        # Four baskets: AB, AB, AC, C.
        baskets = pd.DataFrame([[1, 1, 0], [1, 1, 0], [1, 0, 1], [0, 0, 1]],
                               columns=list('ABC'), dtype=bool)
        rules = generate_rules(mine_itemsets(baskets))
        self.assertEqual(len(rules), 2)  # AC lift is 2/3 and must be excluded.
        expected = {(frozenset('A'), frozenset('B')): 2/3,
                    (frozenset('B'), frozenset('A')): 1.0}
        for row in rules.itertuples():
            self.assertAlmostEqual(row.support, 2/4)
            self.assertAlmostEqual(row.confidence, expected[row.antecedents, row.consequents])
            self.assertAlmostEqual(row.lift, 4/3)
        self.assertEqual(rules.iloc[0].antecedents, frozenset('B'))

    def test_lift_one_is_included_without_confidence_cutoff(self):
        baskets = pd.DataFrame([[1, 1], [1, 0], [0, 1], [0, 0]], columns=['A', 'B'], dtype=bool)
        rules = generate_rules(mine_itemsets(baskets))
        self.assertEqual(len(rules), 2)
        self.assertTrue(rules.lift.eq(1).all())
        self.assertTrue(rules.confidence.eq(.5).all())

    def test_numeric_ranking_uses_lift_then_confidence(self):
        # Nested populations A (4/8), B (2/8), C (1/8).
        itemsets = pd.DataFrame({'itemsets': list(map(frozenset, ['A', 'B', 'C', 'AB', 'AC', 'BC'])),
                                 'support': [.5, .25, .125, .25, .125, .125]})
        rules = generate_rules(itemsets)
        self.assertEqual(list(zip(rules.lift, rules.confidence)),
                         [(4, 1), (4, .5), (2, 1), (2, 1), (2, .5), (2, .25)])

    def test_triples_have_nonempty_disjoint_sides(self):
        rules = generate_rules(mine_itemsets(pd.DataFrame([[1, 1, 1], [0, 0, 0]], columns=list('ABC'), dtype=bool)))
        self.assertEqual(len(rules), 12)  # Six pair directions, six triple partitions.
        for row in rules.itertuples():
            self.assertTrue(row.antecedents and row.consequents)
            self.assertFalse(row.antecedents & row.consequents)
            self.assertLessEqual(len(row.antecedents | row.consequents), 3)
