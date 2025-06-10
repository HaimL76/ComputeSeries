from polynomial import Polynomial


class Exponential:
    def __init__(self, symb: str, exp: Polynomial):
        self.symbol: str = symb
        self.exponent: Polynomial = exp

    def __mul__(self, other):
        return Exponential(symb=self.symbol, exp=self.exponent + other.exponent)

    def __str__(self):
        return f"{self.symbol}^({self.exponent})"

    @staticmethod
    def parse(text: str):
        exponential = None

        l: list = text.split("^")

        if isinstance(l, list) and len(l) == 2:
            exponential = Exponential(symb=l[0], exp=Polynomial.parse(l[1]))

        return exponential


class ExponentialExpression:
    def __init__(self, exps: list=[]):
        self.exponentials: dict = {}

        for exp in exps:
            if isinstance(exp, Exponential) and exp.symbol:
                self.add_exponential(exp)

    def add_exponential(self, exp: Exponential):
        if exp.symbol:
            if exp.symbol not in self.exponentials:
                self.exponentials[exp.symbol] = exp
            else:
                self.exponentials[exp.symbol] *= exp

    def __mul__(self, other):
        return Exponential(symb=self.symbol, exp=self.exponent + other.exponent)

    def __str__(self):
        return "*".join(f"{exp}" for exp in self.exponentials.values())

    def break_by_exponent(self):
        exponent_symbols: dict = {}

        for base_symbol in self.exponentials.keys():
            exp: Exponential = self.exponentials[base_symbol]

            exponent_polynomial: Polynomial = exp.exponent

            for monom in exponent_polynomial.monomials:
                elem_symbol: str = next(iter(monom.elements))
                elem: Element = monom.elements[elem_symbol]

                if elem_symbol not in exponent_symbols:
                    exponent_symbols[elem_symbol] = {}

                d = exponent_symbols[elem_symbol]

                if base_symbol not in d:
                    d[base_symbol] = monom.coefficient
                else:
                    d[base_symbol] += monom.coefficient

    @staticmethod
    def parse(text: str):
        exponential = None

        l: list = text.split("^")

        if isinstance(l, list) and len(l) == 2:
            exponential = Exponential(symb=l[0], exp=Polynomial.parse(l[1]))

        return exponential
