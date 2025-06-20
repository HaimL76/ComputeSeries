import copy

from polynomial import Polynomial, PolynomialProduct
from rational import Rational


class PolynomialRational:
    def __init__(self, numer: Polynomial, denom: Polynomial):
        self.numerator: Polynomial = copy.deepcopy(numer)
        self.denominator: Polynomial = copy.deepcopy(denom)

    @staticmethod
    def parse(text: str):
        numer: int = 0
        denom: int = 1

        l: list = text.split("/")

        if isinstance(l, list) and len(l) > 0:
            s: str = l[0]

            if s:
                s = s.strip()

                if s and s.isnumeric():
                    numer = int(s)

                    if len(l) > 1:
                        s = l[1]

                        if s:
                            s = s.strip()

                            if s and s.isnumeric():
                                denom = int(s)

        return Rational(numer=numer, denom=denom)

    def __add__(self, other):
        denom: int = self.denominator * other.denominator

        numer1: int = self.numerator * other.denominator
        numer2: int = other.numerator * self.denominator

        return Rational(numer=numer1 + numer2, denom=denom)

    def __mul__(self, other):
        return Rational(numer=self.numerator * other.numerator, denom=self.denominator * other.denominator)

    def __eq__(self, other):
        return self.numerator == other.numerator and self.denominator == other.denominator

    def __str__(self):
        s: str = "*".join([f"({polynom})" for polynom in self.numerator])

        if self.denominator != [1]:
            s0: str = "*".join([f"({polynom})" for polynom in self.denominator])
            s = f"[{s}]/[{s0}]"

        return s

class PolynomialProductRational:
    def __init__(self, numer: PolynomialProduct, denom: PolynomialProduct):
        self.numerator: PolynomialProduct = copy.deepcopy(numer)
        self.denominator: PolynomialProduct = copy.deepcopy(denom)

    def add_polynomial_rational(self, polynomial_rational):
        numer_self: list[PolynomialWithPower] = self.numerator
        denom_self: list[PolynomialWithPower] = self.denominator
        numer_input: list[PolynomialWithPower] = polynomial_rational.numerator
        denom_input: list[PolynomialWithPower] = polynomial_rational.denominator

        for polynom_input in denom_input:
            flag: bool = False

            list_self: list = []
            list_input: list = []

            for polynom_self in denom_self:
                if polynom_input == polynom_self:
                    power_input: Rational = polynom_input.power
                    power_self: Rational = polynom_self.power

                    polynom_self.power = max(power_input, power_self)

                    if power_self > power_input:
                        pow0: Rational = power_self - power_input

                        list_input.append(polynom_input)
                    elif power_input > power_self:
                        pow0: Rational = power_input - power_self

                        list_self.append(polynom_input)

                    flag = True

            if not flag:
                denom_self.append(polynom_input)

            if len(list_self):
                for polynom in list_self:
                    numer_input = self.multiply(numer_input, polynom)

            if len(list_input):
                for polynom in list_input:
                    numer_self = self.multiply(numer_self, polynom)

        return self

    def multiply(self, list_polynomials, polynomial):
        list0: list = []

        for polynom in list_polynomials:
            if polynom == polynomial:
                _ = 0
            else:
                polynom *= polynomial

            list0.append(polynom)

        return list0

    def __mul__(self, other):
        for numer in other.numerator.keys():
            # numer = other.numerator[key]

            if numer not in self.numerator:
                self.numerator[numer] = 0

            self.numerator[numer] += 1





    def __eq__(self, other):
        return self.numerator == other.numerator and self.denominator == other.denominator

    def __str__(self):
        numerator0: list = list(filter(lambda p: not p.is_one(), self.numerator))

        s: str = "1"

        if len(numerator0) > 0:
            s = "*".join([f"({polynom})" for polynom in numerator0])

        denominator0: list = list(filter(lambda p: not p.is_one(), self.denominator))

        s0: str = "1"

        if len(denominator0):
            s0 = "*".join([f"({polynom})" for polynom in denominator0])
            s = f"[{s}]/[{s0}]"

        return s

class PolynomialSummationRational:
    def __init__(self):
        self.numerator: list[PolynomialProduct] = []
        self.denominator: PolynomialProduct = PolynomialProduct()

    def add_polynomial_rational(self, input_product: PolynomialProductRational):
        input_numerator = input_product.numerator
        input_denominator = input_product.denominator

        found: bool = False

        for polynomial_denominator_input in input_denominator.list_polynomials:
            found: bool = False

            for polynomial_denominator_self in self.denominator.list_polynomials:
                if polynomial_denominator_self.base_equals(polynomial_denominator_input):
                    found = True

                    power_input: Rational = polynomial_denominator_input.power
                    power_self: Rational = polynomial_denominator_self.power

                    diff = abs(power_self - power_input)

                    if diff > 0:
                        polynom = copy.deepcopy(polynomial_denominator_self)
                        polynom.power = diff

                        if power_input > power_self:
                            polynomial_denominator_self.power = power_input

                            if self.numerator is not None and len(self.numerator) > 0:
                                for product in self.numerator:
                                    product.mul_polynomial(polynom)
                            else:
                                self.numerator = [PolynomialProduct(polynoms=[polynom])]

                        if power_self > power_input:
                            _ = 0

            if not found:
                self.denominator.mul_polynomial(polynomial_denominator_input)