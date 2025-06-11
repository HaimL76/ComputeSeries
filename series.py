import copy

from element import Element
from monomial import Monomial
from polynomial import Polynomial
from rational import Rational
from polynomial_rational import PolynomialRational


class Series:
    def __init__(self, d: dict = {}, pow: str = "", start: int = 0, coeff: Rational = Rational(1)):
        self.start_index: int = start
        self.coefficient: Rational = coeff

        elems: dict = {}

        for key in d.keys():
            val: int = d[key]

            elems[key] = Element(symb=key, pow=val)

        self.monomial: Monomial = Monomial(elems=elems)
        self.power: str = pow

    def sum(self):
        numer: Polynomial = Polynomial.parse("1")
        denom: Polynomial = Polynomial.parse(f"1-{self.monomial}")

        return PolynomialRational(numer, denom)

    def __str__(self):
        s: str = ""

        s = f"{s}\sum_{{{self.power}={self.start_index}}}"

        if self.coefficient is not None:
            s = f"{s}{self.coefficient}*"

        s = f"{s}({self.monomial})^{self.power}"

        return s

class SeriesProduct:
    def __init__(self, sers: list = [], coeff: Rational = Rational(1)):
        self.list_series: list = sers
        self.coefficient: Rational = coeff

    def __str__(self):
        s: str = "*".join(f"{ser}" for ser in self.list_series)

        return s

    def multiply_by_polynomial(self, polynomial: Polynomial):
        l: list = []

        for monom in polynomial.monomials:
            new_list: list = copy.deepcopy(self.list_series)

            for series in new_list:
                if series.power in monom.elements:
                    elem: Element = monom.elements[series.power]

                    series.coefficient = elem

            new_series_product: SeriesProduct = SeriesProduct(new_list)

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