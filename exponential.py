from element import Element
from polynomial import Polynomial
from series import Series


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
            symbol: str = l[0]

            if symbol:
                symbol = symbol.strip()

            str_exp: str = l[1]

            if len(str_exp) > 2 and str_exp[0] == "{" and str_exp[-1] == "}":
                str_exp = str_exp[1:-1]

            if str_exp:
                str_exp = str_exp.strip()

            if str_exp and symbol:
                exponent: Polynomial = Polynomial.parse_single(str_exp)

                if exponent is not None:
                    exponential = Exponential(symb=symbol, exp=exponent)

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
        l: list = []

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

        for pow in exponent_symbols.keys():
            val: dict = exponent_symbols[pow]

            series: Series = Series(val, pow)

            l.append(series)

        return l

    @staticmethod
    def parse(text: str):
        exponential = None

        l: list = text.split("^")

        if isinstance(l, list) and len(l) == 2:
            symbol: str = l[0]

            if symbol:
                symbol = symbol.strip()

            str_exp: str = l[1]

            if len(str_exp) > 2 and str_exp[0] == "{" and str_exp[-1] == "}":
                str_exp = str_exp[1:-1]

            if str_exp:
                str_exp = str_exp.strip()

            if str_exp and symbol:
                exponent: Polynomial = Polynomial.parse_single(str_exp)

                if exponent is not None:
                    exponential = Exponential(symb=symbol, exp=exponent)

        return exponential
