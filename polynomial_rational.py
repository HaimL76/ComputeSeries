import copy

from colorama import Fore, Style

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

    def get_str(self):
        s: str = "*".join([f"({polynom})" for polynom in self.numerator])

        if self.denominator != [1]:
            s0: str = "*".join([f"({polynom})" for polynom in self.denominator])
            s = f"[{s}]/[{s0}]"

        return s

    def get_ltx_str(self):
        s: str = f"{self.numerator}"

        if self.denominator != [1]:
            s = f"\\frac{{{s}}}{{{self.denominator}}}"

        return s

    def __str__(self):
        return self.get_ltx_str()

class PolynomialProductRational:
    def __init__(self, numer: PolynomialProduct, denom: PolynomialProduct, minus: bool = False):
        self.numerator: PolynomialProduct = copy.deepcopy(numer)
        self.denominator: PolynomialProduct = copy.deepcopy(denom)
        self.is_minus: bool = minus

    def __eq__(self, other):
        return self.numerator == other.numerator and self.denominator == other.denominator

    def get_str(self):
        numerator0: list = list(filter(lambda p: not p.is_one(), self.numerator))

        s: str = "1"

        if len(numerator0) > 0:
            s = "*".join([f"({polynom})" for polynom in numerator0])

        if len(self.numerator.const_coefficients) > 0:
            s1 = "*".join([f"({const_coeff})" for const_coeff in self.numerator.const_coefficients])

            s = f"{Fore.RED}{s1}{Style.RESET_ALL}*{s}"

        if self.numerator.coefficient != Rational(1):
            s = f"{Fore.LIGHTMAGENTA_EX}{self.numerator.coefficient}{Style.RESET_ALL}*{s}"

        denominator0: list = list(filter(lambda p: not p.is_one(), self.denominator))

        s0: str = "1"

        if self.denominator.coefficient != Rational(1):
            s = f"{Fore.LIGHTMAGENTA_EX}{self.denominator.coefficient}{Style.RESET_ALL}*{s}"

        if len(denominator0):
            s0 = "*".join([f"({polynom})" for polynom in denominator0])
            s = f"[{s}]/[{s0}]"

        return s

    def get_ltx_str(self):
        numerator0: list = list(filter(lambda p: not p.is_one(), self.numerator))

        s: str = "1"

        if len(numerator0) > 0:
            s = "".join([f"{polynom}" for polynom in numerator0])

        if len(self.numerator.const_coefficients) > 0:
            s1 = "".join([f"({self.numerator.const_coefficients[const_coeff]})" for const_coeff in self.numerator.const_coefficients.keys()])

            s = f"{s1}{s}"

        if self.numerator.coefficient != Rational(1):
            s = f"{self.numerator.coefficient}{s}"

        denominator0: list = list(filter(lambda p: not p.is_one(), self.denominator))

        s0: str = "1"

        if self.denominator.coefficient != Rational(1):
            s = f"{self.denominator.coefficient}{s}"

        if len(denominator0):
            s0 = "".join([f"{polynom}" for polynom in denominator0])
            s = f"\\frac{{{s}}}{{{s0}}}"

            if self.is_minus:
                s = f"-{s}"

        return s

    def __str__(self):
        return self.get_ltx_str()


class PolynomialSummationRational:
    def __init__(self):
        self.numerator: list[PolynomialProduct] = []
        self.denominator: PolynomialProduct = PolynomialProduct()

    def __add__(self, other):
        self_copy = copy.deepcopy(self)

        other_denominator: PolynomialProduct = copy.deepcopy(other.denominator)
        other_numerator = copy.deepcopy(other.numerator)

        for pol_prod in other_numerator:
            pol_prod0 = copy.deepcopy(pol_prod)

            rational_product: PolynomialProductRational = PolynomialProductRational(numer=pol_prod0,
                                                                                    denom=other_denominator,
                                                                                    minus=pol_prod.is_minus)

            self_copy.add_polynomial_rational(rational_product)

        return self_copy

    def add_polynomial_rational(self, input_product: PolynomialProductRational):
        is_minus0: bool = input_product.is_minus

        input_numerator = copy.deepcopy(input_product.numerator)
        input_denominator = copy.deepcopy(input_product.denominator)

        if is_minus0:
            input_numerator.is_minus = is_minus0

        if (self.numerator is None or len(self.numerator) < 1) and (self.denominator is None or self.denominator.list_polynomials is None or len(self.denominator.list_polynomials) < 1):
            self.numerator = [copy.deepcopy(input_numerator)]
            self.denominator = copy.deepcopy(input_denominator)
        else:
            for polynomial_denominator_input in input_denominator.list_polynomials:
                found: bool = False

                for polynomial_denominator_self in self.denominator.list_polynomials:
                    if polynomial_denominator_self.base_equals(polynomial_denominator_input):
                        found = True

                        power_input: Rational = polynomial_denominator_input.power
                        power_self: Rational = polynomial_denominator_self.power

                        if power_input > 2:
                            _ = 0

                        diff = abs(power_self - power_input)

                        if diff > 0:
                            polynom = copy.deepcopy(polynomial_denominator_self)
                            polynom.power = diff

                            if diff > Rational(2):
                                _ = 0

                            if power_input > power_self:
                                polynomial_denominator_self.power = power_input

                                if self.numerator is not None and len(self.numerator) > 0:
                                    for product in self.numerator:
                                        product.mul_polynomial(polynom)
                                else:
                                    self.numerator = [PolynomialProduct(polynoms=[polynom])]

                            if power_self > power_input:
                                input_numerator.mul_polynomial(polynom)

                if not found:
                    self.denominator.mul_polynomial(polynomial_denominator_input)

                    if self.numerator is not None and len(self.numerator) > 0:
                        for product in self.numerator:
                            product.mul_polynomial(polynomial_denominator_input)
                    else:
                        self.numerator = [PolynomialProduct(polynoms=[polynomial_denominator_input])]

            self.numerator.append(input_numerator)

    def __str__(self):
        return self.get_ltx_str()

    def get_ltx_str(self):
        #s: str = "".join(f"\\[+\\frac{{{product}}}{{{self.denominator}}}+\\]" for product in self.numerator)

        s: str = ""

        for product in self.numerator:
            sign = "-" if product.is_minus else "+"
            s += f"\\[{sign}\\frac{{{product}}}{{{self.denominator}}}\\]"

        return s

    def get_str(self):
        s: str = " + ".join(f"{product}" for product in self.numerator)

        s = f"[{s}]/[{self.denominator}]"

        return s