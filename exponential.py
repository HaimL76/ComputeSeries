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

    def get_str(self, is_latex: bool = True):
        return f"{self.symbol}^({self.exponent.get_ltx_str()})" if is_latex else f"({self.symbol}^({self.exponent.get_sage_str()}))"

    def get_ltx_str(self):
        return self.get_str(is_latex=True)

    def get_sage_str(self):
        return self.get_str(is_latex=False)

    @staticmethod
    def parse(text: str, list_const_coeffs: list[str]):
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
                exponent: Polynomial = Polynomial.parse_single(str_exp, list_const_coeffs=list_const_coeffs)

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
    def parse(text: str, list_const_coeffs: list[str]):
        exponential_product: ExponentialProduct = ExponentialProduct()

        l: list = text.split("*")

        if isinstance(l, list) and len(l) > 0:
            for s in l:
                s = s.strip()

                if s:
                    exponential: Exponential = Exponential.parse(s, list_const_coeffs=list_const_coeffs)

                    if isinstance(exponential, Exponential):
                        exponential_product.add_exponential(exponential)

        return exponential_product

    def __str__(self):
        return self.get_ltx_str()

    def get_str(self, is_latex: bool = True):
        separator: str = "" if is_latex else "*"

        return separator.join(f"{exp.get_str(is_latex=is_latex)}" for exp in self.exponentials.values())

    def get_ltx_str(self):
        return self.get_str(is_latex=True)

    def get_sage_str(self):
        return self.get_str(is_latex=False)

    def get_ltx_pt_str(self):
        return self.get_pt_str(is_latex=True)

    def get_sage_pt_str(self):
        return self.get_pt_str(is_latex=False)

    def get_pt_str(self, is_latex: bool = True):
        exp_dict: dict = {}

        for exp in self.exponentials:
            exponential: Polynomial = self.exponentials[exp]

            exp_symb: str = exponential.symbol

            exponent: Polynomial = exponential.exponent

            for monomial in exponent.monomials:
                coeff = monomial.coefficient

                for elem in monomial.elements:
                    element: Element = monomial.elements[elem]

                    if element.symbol not in exp_dict:
                        exp_dict[element.symbol] = {}

                    inner_dict: dict = exp_dict[element.symbol]

                    inner_dict[exp_symb] = coeff

        list_exponents: list[tuple[str, dict[str, int]]] = [(key, exp_dict[key]) for key in list(exp_dict.keys())]

        len_list_exponents: int = len(list_exponents)

        list_str: list[str] = [""] * len_list_exponents

        for index in range(len_list_exponents):
            tup: tuple[str, dict[str, int]] = list_exponents[index]

            exp: dict[str, int] = tup[1]

            p: int = exp["p"]
            t: int = exp["t"]
            
            exponent: str = tup[0]

            str_exp: str = f"(p^{p}*t^{t})^{exponent}"

            list_str[index] = str_exp

        return "*".join([s_exp for s_exp in list_str])