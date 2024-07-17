from money import Money


class Portfolio:
    """
    This is just a comment.
    """
    def __init__(self):
        """This is the class initializer."""
        self.moneys = []
        self._euro_to_usd = 1.2

    def __convert(self, a_money, a_currency):
        """This is a special method."""
        exchange_rates = {"EUR->USD": 1.2, "USD->KRW": 1100}
        if a_money.currency == a_currency:
            return a_money.amount
        key = f"{a_money.currency}->{a_currency}"
        return a_money.amount * exchange_rates[key]

    def add(self, *moneys):
        self.moneys.extend(moneys)

    def evaluate(self, bank, currency):
        total = 0.0
        failures = []
        for m in self.moneys:
            try:
                total += bank.convert(m, currency).amount
            except Exception as ex:
                failures.append(ex)
        if not failures:
            return Money(total, currency)

        failure_message = ",".join(f.args[0] for f in failures)
        raise Exception("No exchange rate(s):[" + failure_message + "]")
