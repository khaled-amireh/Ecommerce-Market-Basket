import unittest

import numpy as np
import pandas as pd

from ecommerce_market_basket import mine_itemsets


class AprioriTests(unittest.TestCase):
    def setUp(self):
        # AB, AB, AC, C: s(A)=3/4, s(B)=2/4, s(C)=2/4,
        # s(AB)=2/4, s(AC)=1/4, s(BC)=0.
        self.basket = pd.DataFrame([[1, 1, 0], [1, 1, 0], [1, 0, 1], [0, 0, 1]],
                                   columns=['A', 'B', 'C']).astype(bool)

    def test_hand_calculated_complete_itemsets_and_support(self):
        result = mine_itemsets(self.basket)
        expected = {frozenset('A'): .75, frozenset('B'): .5, frozenset('C'): .5,
                    frozenset('AB'): .5, frozenset('AC'): .25}
        self.assertEqual(set(result.itemsets), set(expected))
        for row in result.itertuples():
            self.assertAlmostEqual(row.support, expected[row.itemsets])
        self.assertTrue(result.support.is_monotonic_decreasing)

    def test_threshold_is_inclusive(self):
        result = mine_itemsets(self.basket, min_support=.5)
        self.assertEqual(set(result.itemsets), {frozenset('A'), frozenset('B'),
                                              frozenset('C'), frozenset('AB')})
        result = mine_itemsets(self.basket, min_support=np.nextafter(.5, 1))
        self.assertEqual(set(result.itemsets), {frozenset('A')})

    def test_default_two_percent_boundary(self):
        basket = pd.DataFrame({'A': [True] + [False] * 49})
        self.assertAlmostEqual(mine_itemsets(basket).support.iloc[0], .02)
        self.assertTrue(mine_itemsets(pd.concat([basket, basket.iloc[[-1]]])).empty)

    def test_three_item_cap_and_triple_support(self):
        result = mine_itemsets(pd.DataFrame([[True] * 4] * 2, columns=list('ABCD')))
        self.assertEqual(len(result), 14)  # 4 singletons + 6 pairs + 4 triples.
        self.assertEqual(max(map(len, result.itemsets)), 3)
        self.assertTrue(result.support.eq(1).all())

    def test_empty_population_is_distinct_from_no_frequent_sets(self):
        with self.assertRaisesRegex(ValueError, 'No eligible baskets'):
            mine_itemsets(self.basket.iloc[:0])
        self.assertTrue(mine_itemsets(self.basket, min_support=1).empty)

    def test_invalid_matrix_and_duplicate_columns(self):
        for value in [2, -1, np.nan, 'yes']:
            basket = self.basket.astype(object)
            basket.iloc[0, 0] = value
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, 'binary'):
                mine_itemsets(basket)
        with self.assertRaisesRegex(ValueError, 'unique'):
            mine_itemsets(pd.DataFrame([[1, 1]], columns=['A', 'A']))

    def test_invalid_support(self):
        for support in [0, -1, 1.1, float('nan'), True]:
            with self.subTest(support=support), self.assertRaisesRegex(ValueError, 'min_support'):
                mine_itemsets(self.basket, support)
