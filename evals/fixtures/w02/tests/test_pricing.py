import unittest
from src.pricing import discounted_price


class PricingTests(unittest.TestCase):
    def test_partial_discount(self):
        self.assertEqual(discounted_price(80, 25), 60)

    def test_full_discount(self):
        self.assertEqual(discounted_price(80, 100), 0)

    def test_invalid_discount(self):
        for percent in (-1, 101):
            with self.assertRaises(ValueError):
                discounted_price(80, percent)
