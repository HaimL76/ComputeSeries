import copy

from element import Element
from exponential import ExponentialProduct
from monomial import Monomial
from polynomial import Polynomial
from rational import Rational
from polynomial_rational import PolynomialRational


class Series:
    def __init__(self, monom: Monomial, pow: str = "", start: int = 0, coeff: Rational = Rational(1)):
        self.start_index: int = start
        self.coefficient: Monomial = Monomial(coeff=Rational(1))

        self.monomial: Monomial = monom
        self.power: str = pow

    def sum(self):
        numer: Polynomial = Polynomial.parse("1")
        denom: Polynomial = Polynomial.parse(f"1-{self.monomial}")

        return PolynomialRational(numer, denom)

    def __str__(self):
        s: str = ""

        if self.coefficient is not None:
            s = f"{self.coefficient}"

        s = rf"{s}\sum_{{{self.power}={self.start_index}}}({self.monomial})"

        return s


class SeriesProduct:
    def __init__(self, sers: dict = {}, coeff: Rational = Rational(1)):
        self.dict_series: list = copy.deepcopy(sers)
        self.coefficient: Rational = coeff

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

    def __str__(self):
        s: str = "*".join(f"{ser}" for ser in self.dict_series.values())

        return s

    def multiply_by_polynomial(self, polynomial: Polynomial):
        l: list = []

        for monom in polynomial.monomials:
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

                    elem = d0[symb]

                    elem = Element(symb=elem.symbol, pow=elem.power + 1)

                    d0[symb] = elem

                    if len(d0) > 0:
                        monomial: Monomial = Monomial(elems=d0)

                        series.coefficient = monomial

                        s: str = f"{monomial}"

                new_dict[pow] = series

            new_series_product: SeriesProduct = SeriesProduct(new_dict)

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