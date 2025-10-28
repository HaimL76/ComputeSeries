import copy

from element import Element
from monomial import Monomial
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

    def get_sage_str(self):
        return f"{self.numerator.get_sage_str()}/{self.denominator.get_sage_str()}"

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

    def get_sage_str(self):
        numerator0: list = list(filter(lambda p: not p.is_one(), self.numerator))

        s: str = "1"

        if len(numerator0) > 0:
            s = "".join([f"{polynom.get_sage_str()}" for polynom in numerator0])

        if len(self.numerator.const_coefficients) > 0:
            s1 = "".join([f"({self.numerator.const_coefficients[const_coeff].get_sage_str()})" for const_coeff in
                          self.numerator.const_coefficients.keys()])

            s = f"{s1}{s}"

        if self.numerator.coefficient != Rational(1):
            s = f"{self.numerator.coefficient.get_sage_str()}{s}"

        denominator0: list = list(filter(lambda p: not p.is_one(), self.denominator))

        s0: str = "1"

        if self.denominator.coefficient != Rational(1):
            s = f"{self.denominator.coefficient.get_sage_str()}{s}"

        if len(denominator0):
            s0 = "".join([f"{polynom}" for polynom in denominator0])
            s = f"{s}/{s0}"

            if self.is_minus:
                s = f"-{s}"

        return s

    def get_ltx_str(self):
        numerator0: list = list(filter(lambda p: not p.is_one(), self.numerator))

        s: str = "1"

        if len(numerator0) > 0:
            s = "".join([f"{polynom}" for polynom in numerator0])

        if len(self.numerator.const_coefficients) > 0:
            s1 = "".join([f"({self.numerator.const_coefficients[const_coeff]})" for const_coeff in
                          self.numerator.const_coefficients.keys()])

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
    def multiply(self):
        dict_monomials_by_powers: dict[(int, int), list[Monomial]] = {}

        index_products: int = 0

        sum_polynomials = Polynomial.create_zero_polynomial()

        list_polynomials: list[(PolynomialProduct, Polynomial)] = []

        num_monoms: int = 0

        for product in self.numerator:
            product_copy: PolynomialProduct = copy.deepcopy(product)

            product_polynomial: Polynomial = Polynomial.create_one_polynomial()

            index_polynomials: int = 0

            for pol_factor in product_copy.list_polynomials:
                print(f"product {index_products} of {len(self.numerator)},"
                      f" polynomial {index_polynomials} of {len(product_copy.list_polynomials)},"
                      f" pol={len(pol_factor.monomials)}, product={len(product_polynomial.monomials)}")
                index_polynomials += 1

                pol_powers: Polynomial = Polynomial.create_one_polynomial()

                pol_factor_copy: Polynomial = copy.deepcopy(pol_factor)

                factor_power: int = 1

                if pol_factor_copy.power is not None:
                    factor_power = pol_factor_copy.power.numerator

                if factor_power > 1:
                    pol_factor_copy.power = Rational(1)

                for i in range(factor_power):
                    pol_powers *= pol_factor_copy

                product_polynomial *= pol_powers

            coeff = copy.deepcopy(product.coefficient)
            const_coeffs = copy.deepcopy(product.const_coefficients)

            if coeff != Rational(1) or (isinstance(const_coeffs, dict) and len(const_coeffs) > 0) or product.is_minus:
                pol_coeff: Polynomial = Polynomial(monoms=[Monomial(coeff=coeff, const_coeffs=const_coeffs, minus=product.is_minus)])

                product_polynomial *= pol_coeff

            for monomial in product_polynomial.monomials:
                if isinstance(monomial.elements, dict) and 'p' in monomial.elements and 't' in monomial.elements:
                    pow_p: Element = monomial.elements['p']
                    pow_t: Element = monomial.elements['t']

                    key_p_t = (pow_p.power.numerator, pow_t.power.numerator)

                    if key_p_t not in dict_monomials_by_powers:
                        ##print(f"[{len(dict_monomials_by_powers)}], p={pow_p.power.numerator}, t={pow_t.power.numerator}")
                        dict_monomials_by_powers[key_p_t] = []

                    dict_monomials_by_powers[key_p_t].append(monomial)

            num_monoms += len(product_polynomial.monomials)

            list_polynomials.append((product_copy, product_polynomial))

            sum_polynomials += product_polynomial

            index_products += 1

        return sum_polynomials, list_polynomials, dict_monomials_by_powers

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

        for pol in input_denominator:
            if pol.power == Rational(4):
                _ = 0

        if is_minus0:
            input_numerator.is_minus = is_minus0

        if (self.numerator is None or len(self.numerator) < 1) and (
                self.denominator is None or self.denominator.list_polynomials is None or len(
                self.denominator.list_polynomials) < 1):
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

    def get_sage_str(self):
        s: str = ""

        for product in self.numerator:
            sign = "-" if product.is_minus else "+"
            s += f"\\[{sign}\\frac{{{product}}}{{{self.denominator}}}\\]"

        return s

    def get_ltx_str(self):
        # s: str = "".join(f"\\[+\\frac{{{product}}}{{{self.denominator}}}+\\]" for product in self.numerator)

        s: str = ""

        for product in self.numerator:
            sign = "-" if product.is_minus else "+"
            s += f"\\[{sign}\\frac{{{product}}}{{{self.denominator}}}\\]"

        return s

    def get_ltx_str_denominator(self):
        return f"\\[{self.denominator}\\]"

    def get_ltx_str_partial(self, skip: int, take: int):
        # s: str = "".join(f"\\[+\\frac{{{product}}}{{{self.denominator}}}+\\]" for product in self.numerator)

        s: str = ""

        index: int = skip

        end_index: int = index + take

        len_products: int = len(self.numerator)

        end_index0: int = min(end_index, len_products) if take > 0 else len_products

        while index < end_index0:
            product: PolynomialProduct = self.numerator[index]
            index += 1

            sign = "-" if product.is_minus else "+"
            s += f"\\[{sign}{product}\\]"

        more_products: bool = index < len_products

        return s, not more_products

    def get_str(self):
        s: str = " + ".join(f"{product}" for product in self.numerator)

        s = f"[{s}]/[{self.denominator}]"

        return s
