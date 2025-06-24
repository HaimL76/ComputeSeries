from element import Element
from polynomial import Polynomial


class Exponential:
    def __init__(self, symb: str, exp: Polynomial):
        self.symbol: str = symb
        self.exponent: Polynomial = exp

    def __mul__(self, other):
        return Exponential(symb=self.symbol, exp=self.exponent + other.exponent)

    def __str__(self):
        return self.get_ltx_str()

    def get_str(self):
        return f"{self.symbol}^({self.exponent})"

    def get_ltx_str(self):
        return f"{self.symbol}^{{{self.exponent}}}"

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


class ExponentialProduct:
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

    def __iter__(self):
        for key in self.exponentials.keys():
            yield key

    @staticmethod
    def parse(text: str):
        exponential_product: ExponentialProduct = ExponentialProduct()

        l: list = text.split("*")

        if isinstance(l, list) and len(l) > 0:
            for s in l:
                s = s.strip()

                if s:
                    exponential: Exponential = Exponential.parse(s)

                    if isinstance(exponential, Exponential):
                        exponential_product.add_exponential(exponential)

        return exponential_product

    def __str__(self):
        return self.get_ltx_str()

    def get_str(self):
        return "*".join(f"{exp}" for exp in self.exponentials.values())

    def get_ltx_str(self):
        return "".join(f"{exp}" for exp in self.exponentials.values())