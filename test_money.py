import unittest

from bank import Bank
from money import Money
from portfolios import Portfolio


class TestMoney(unittest.TestCase):
    """
    Just a few tests.
    """

    def setUp(self):
        self.bank = Bank()
        self.bank.add_exchange_rate("EUR", "USD", 1.2)
        self.bank.add_exchange_rate("USD", "KRW", 1100)

    def test_multiplication(self):
        ten_euros = Money(10, "EUR")
        twenty_euros = ten_euros.times(2)
        self.assertEqual(ten_euros.times(2), twenty_euros)

    def test_division(self):
        original_amount = Money(4002, "KRW")
        amount_after_division = original_amount.divide(4)
        expected_money = Money(1000.5, "KRW")
        self.assertEqual(expected_money, amount_after_division)

    def test_addition(self):
        five_dollars = Money(5, "USD")
        ten_dollars = Money(10, "USD")
        fifteen_dollars = Money(15, "USD")
        portfolio = Portfolio()
        portfolio.add(five_dollars, ten_dollars)
        self.assertEqual(fifteen_dollars, portfolio.evaluate(self.bank, "USD"))

    def test_add_dollars_to_euros(self):
        five_dollars = Money(5, "USD")
        ten_euros = Money(10, "EUR")
        portfolio = Portfolio()
        portfolio.add(five_dollars, ten_euros)
        expected_result = Money(17, "USD")
        actual_resut = portfolio.evaluate(self.bank, "USD")
        self.assertEqual(expected_result, actual_resut, f"{expected_result} != {actual_resut}")

    def test_addition_dollars_and_wons(self):
        one_dollar = Money(1, "USD")
        elevenhundred_won = Money(1100, "KRW")
        portfolio = Portfolio()
        portfolio.add(one_dollar, elevenhundred_won)
        expected_value = Money(2200, "KRW")
        actual_value = portfolio.evaluate(self.bank, "KRW")
        self.assertEqual(expected_value, actual_value, f"{expected_value} != {actual_value}")

    def test_addition_with_multiple_exchange_rates_missing(self):
        one_dollar = Money(1, "USD")
        one_euro = Money(1, "EUR")
        one_won = Money(1, "KRW")
        portfolio = Portfolio()
        portfolio.add(one_dollar, one_euro, one_won)
        with self.assertRaisesRegex(
            Exception,
            r"No exchange rate\(s\):\[USD\->Kalganid,EUR->Kalganid,KRW->Kalganid]",  # noqa: W605
        ):
            portfolio.evaluate(self.bank, "Kalganid")

    def test_conversion(self):
        ten_euros = Money(10, "EUR")
        self.assertEqual(self.bank.convert(ten_euros, "USD"), Money(12, "USD"))

        self.bank.add_exchange_rate("EUR", "USD", 1.3)
        self.assertEqual(self.bank.convert(ten_euros, "USD"), Money(13, "USD"))

    def test_conversion_with_missing_exchange_rate(self):
        ten_euros = Money(10, "EUR")
        with self.assertRaisesRegex(Exception, "EUR->Kalganid"):
            self.bank.convert(ten_euros, "Kalganid")


if __name__ == "__main__":
    unittest.main()
