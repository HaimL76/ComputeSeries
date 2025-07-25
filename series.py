import copy

from colorama import Fore, Style

from debug_write import DebugWrite
from element import Element
from exponential import ExponentialProduct
from monomial import Monomial
from polynomial import Polynomial, PolynomialProduct
from rational import Rational
from polynomial_rational import PolynomialRational, PolynomialProductRational


class Series:
    def __init__(self, monom: Monomial, pow: str = "", start: int = 0, coeff: Rational = Rational(1)):
        self.start_index: int = start
        self.coefficient: Monomial = Monomial(coeff=Rational(1))

        self.monomial: Monomial = monom
        self.power: str = pow

    def sum(self):
        numer: Polynomial = Polynomial.parse_single("1", list_const_coeffs=[])
        denom: Polynomial = Polynomial.parse_single(f"1-{self.monomial}", list_const_coeffs=[])

        if self.start_index == 1:
            numer = Polynomial([self.monomial], in_product=True)

        numer.in_polynomial_product = True
        denom.in_polynomial_product = True

        elems: dict = self.coefficient.elements

        if isinstance(elems, dict) and self.power in elems:
            elem: Element = elems[self.power]

            if elem.power == 1:
                numer = Polynomial([self.monomial], in_product=True)
                denom.power = Rational(2)
            elif elem.power == 2:
                numer = Polynomial([self.monomial*self.monomial, self.monomial], in_product=True)
                denom.power = Rational(3)

        polynomial_rational: PolynomialRational = PolynomialRational(numer, denom)

        ##debug_write: DebugWrite = DebugWrite.get_instance()

        ##debug_write.write(f"\\[{self}={polynomial_rational}\\]", level=1)

        return polynomial_rational

    def get_str(self):
        s: str = ""

        if self.coefficient is not None and not self.coefficient.is_one():
            s = f"{Fore.LIGHTGREEN_EX}{self.coefficient}{Style.RESET_ALL}"

        s = rf"\sum_{{{self.power}={self.start_index}}}{s}({self.monomial})"

        s = f"{s}^{Fore.LIGHTCYAN_EX}{self.power}{Style.RESET_ALL}"

        return s

    def get_ltx_str(self):
        s: str = ""

        color = "red"

        if self.coefficient is not None and not self.coefficient.is_one():
            s = f"\\textcolor{{{color}}}{{{self.coefficient}}}"

        s = f"\\sum_{{{self.power}\\geq{{{self.start_index}}}}}{s}({self.monomial})"

        s = f"{s}^{{{self.power}}}"

        return s

    def __str__(self):
        return self.get_ltx_str()

class SeriesProduct:
    def __init__(self, sers: dict = {}, coeff: Rational = Rational(1), const_coeffs: dict[str, Element] = {},
                 minus: bool = False):
        self.dict_series: dict = copy.deepcopy(sers)
        self.coefficient: Rational = coeff
        self.const_coefficients: dict[str, Element] = copy.deepcopy(const_coeffs)
        self.is_minus = minus

    def add_start_index(self, symbol: str, index: int):
        if symbol:
            symbol = symbol.strip()

        if symbol:
            ser: Series = self.dict_series[symbol]

            if isinstance(ser, Series):
                ser.start_index = index

    def parse_starting_indices(self, text: str):
        l: list[str] = text.split(",")

        for s in l:
            if s:
                s = s.strip()

            if s:
                l0: list[str] = s.split(">=")

                if len(l0) == 2:
                    s = l0[0]

                    if s:
                        s = s.strip()

                    if s and s in self.dict_series:
                        ser: Series = self.dict_series[s]

                        if ser is not None:
                            s = l0[1]

                            if s:
                                s = s.strip()

                            if s and s.isnumeric():
                                ser.start_index = int(s)



    def sum(self):
        result_numerator: PolynomialProduct = PolynomialProduct()
        result_denominator: PolynomialProduct = PolynomialProduct()

        for key in self.dict_series.keys():
            series: Series = self.dict_series[key]

            single_series_sum: PolynomialRational = series.sum()

            single_series_sum_numerator: Polynomial = single_series_sum.numerator
            single_series_sum_denominator: Polynomial = single_series_sum.denominator

            flag: bool = False

            for polynom in result_numerator.list_polynomials:
                if polynom.base_equals(single_series_sum_numerator):
                    if not polynom.is_one():
                        polynom.power += single_series_sum_numerator.power

                    flag = True

            if not flag:
                result_numerator.list_polynomials.append(single_series_sum_numerator)

            flag = False

            for polynom in result_denominator.list_polynomials:
                if polynom.base_equals(single_series_sum_denominator):
                    polynom.power += single_series_sum_denominator.power
                    flag = True

            if not flag:
                result_denominator.list_polynomials.append(single_series_sum_denominator)

        result_numerator.coefficient = self.coefficient

        result_numerator.const_coefficients = copy.deepcopy(self.const_coefficients)

        return PolynomialProductRational(numer=result_numerator, denom=result_denominator,
                                         minus=self.is_minus)

    @staticmethod
    def from_exponential_product(exponential_product: ExponentialProduct):
        d: dict = {}

        for symb in exponential_product.exponentials.keys():
            exponential: ExponentialProduct = exponential_product.exponentials[symb]

            polynomial: Polynomial = exponential.exponent

            for monom in polynomial.monomials:
                if len(monom.elements) == 1:
                    key: str = next(iter(monom.elements))

                    if key and key in monom.elements:
                        element: Element = monom.elements[key]

                        exp: str = element.symbol

                        if exp not in d:
                            d[exp]: dict = {}

                        val: dict = d[exp]

                        if symb not in val:
                            val[symb] = Rational(0)

                        val[symb] += monom.coefficient

        d0: dict = {}

        for symb in d.keys():
            elements: dict = {}

            val = d[symb]

            for key in val:
                num = val[key]

                elem: Element = Element(symb=key, pow=num)

                if elem.symbol not in elements:
                    elements[elem.symbol] = elem

            monomial: Monomial = Monomial(elems=elements)

            series: Series = Series(monom=monomial, pow=symb)

            d0[series.power] = series

        return SeriesProduct(sers=d0)

    def get_str(self):
        s: str = ""

        if self.coefficient is not None and self.coefficient != Rational(1):
            s = f"{Fore.LIGHTMAGENTA_EX}{self.coefficient}{Style.RESET_ALL}"

        if self.const_coefficients:
            if s:
                s = f"{s}*"

            s1: str = "*".join([f"({const_coeff})" for const_coeff in self.const_coefficients.values()])

            s = f"{s}{Fore.RED}{s1}{Style.RESET_ALL}"

        s0: str = "*".join(f"[{ser}]" for ser in self.dict_series.values())

        s = f"{s}{s0}"

        return s

    def get_ltx_str(self):
        s: str = ""

        if self.is_minus:
            s = "-"

        if self.coefficient is not None and self.coefficient != Rational(1):
            s += f"{self.coefficient}"

        if self.const_coefficients:
            s1: str = "".join([f"{const_coeff.get_copy_with_parentheses()}" for const_coeff in self.const_coefficients.values()])

            s = f"{s}{s1}"

        s0: str = "".join(f"{ser}" for ser in self.dict_series.values())

        s = f"{s}{s0}"

        return s

    def __str__(self):
        return self.get_ltx_str()

    def multiply_by_polynomial(self, polynomial: Polynomial):
        l: list = []

        monoms: list[Monomial] = [monom for monom in polynomial.monomials if monom.coefficient != Rational(0)]

        for monom in monoms:
            new_dict: dict = copy.deepcopy(self.dict_series)

            for key in new_dict.keys():
                series: Series = new_dict[key]

                pow: str = series.power

                d0: dict = {}

                if pow in monom.elements.keys():
                    elem: Element = monom.elements[pow]

                    symb: str = elem.symbol

                    if symb not in d0:
                        d0[symb] = Element(symb=symb, pow=0)

                    elem0 = d0[symb]

                    elem0 = Element(symb=elem0.symbol, pow=elem0.power + elem.power)

                    d0[symb] = elem0

                    if len(d0) > 0:
                        monomial: Monomial = Monomial(elems=d0)

                        series.coefficient = monomial

                        s: str = f"{monomial}"

                new_dict[pow] = series

            new_series_product: SeriesProduct = SeriesProduct(new_dict, coeff=monom.coefficient,
                                                              const_coeffs=monom.const_coefficients,
                                                              minus=monom.is_minus)

            l.append(new_series_product)

        return l

class SeriesProductSum:
    def __init__(self, ser_prods: list = []):
        self.series_products: list = ser_prods

    def __str__(self):
        return " +\n+ ".join(f"{ser_prod}" for ser_prod in self.series_products)

    @staticmethod
    def multiply_series_product_by_polynomial(series_product: SeriesProduct, polynomial: Polynomial):
        l: list = series_product.multiply_by_polynomial(polynomial)

        return SeriesProductSum(l)