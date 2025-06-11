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
        s: str = f"\sum_{{{self.power}={self.start_index}}}"

        if self.coefficient != Rational(1):
            s = f"{s}{self.coefficient}"

        s = f"{s}({self.monomial})^{self.power}"

        return s

class SeriesProduct:
    def __init__(self, sers: list = []):
        self.list_series: list = sers

    def multiply_by_polynomial(self, polynomial: Polynomial):
        _ = 0