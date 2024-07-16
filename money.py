class Money():
    """
    Docstring goes here.
    """
    def __init__(self, amount, currency):
        """This is the class initializer."""
        self.amount = amount
        self.currency = currency

    def times(self, multiplier):
        """This is a method."""
        return Money(self.amount * multiplier, self.currency)

    def divide(self, divisor):
        """This is another method."""
        return Money(self.amount / divisor, self.currency)

    def __eq__(self, other):
        return self.amount == other.amount and self.currency == other.currency

    def __str__(self):
        return f"{self.currency} {self.amount:0.2f}"
