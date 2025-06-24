import copy

from colorama import Fore, Style

from element import Element
from monomial import Monomial
from rational import Rational


class Polynomial:
    def __init__(self, monoms: list = [], nm: str = "", pow0: Rational = Rational(1)):
        self.monomials: list = copy.deepcopy(monoms)
        self.name: str = nm
        self.power: Rational = pow0

    @staticmethod
    def create_one():
        return Polynomial(monoms=[Monomial()])

    def __iter__(self):
        for monom in self.monomials:
            yield monom

    def is_one(self):
        return len(self.monomials) == 1 and next(iter(self.monomials)).is_one()

    def __mul__(self, other):
        monoms: list = []

        for monom_self in self.monomials:
            for monom_other in other.monomials:
                m = monom_self * monom_other

                monoms.append(m)

        return Polynomial(monoms)

    def add_monomial(self, monomial: Monomial):
        index: int = 0
        found: bool = False

        while not found and index < len(self.monomials):
            monom: Monomial = self.monomials[index]
            index += 1

            if Monomial.are_same_monomials(monom, monomial):
                monom.coefficient += monomial.coefficient

                found = True

        if not found:
            self.monomials.append(monomial)

    @staticmethod
    def parse_monomials(text: str):
        list_list_monomials: list[(list[Monomial], str)] = []

        l0: list = text.split(",")

        for s in l0:
            s = s.strip()

            if s:
                l1: list = s.split("=")

                if isinstance(l1, list) and len(l1) > 0:
                    name: str = ""

                    s1: str = l1[0]

                    if len(l1) > 1:
                        name = s1
                        s1 = l1[1]

                    l2: list = s1.split("+")

                    if isinstance(l2, list) and len(l2) > 0:
                        list_monomials: list = []

                        for s2 in l2:
                            s2 = s2.strip()

                            if s2:
                                monomial: Monomial = Monomial.parse(s2)

                                if monomial:
                                    list_monomials.append(monomial)

                        if len(list_monomials) > 0:
                            list_list_monomials.append((list_monomials, name))

        return list_list_monomials

    def base_equals(self, other):
        equals: bool = False

        if len(self.monomials) == len(other.monomials):
            counter0: int = 0

            for monom in self.monomials:
                for monom0 in other.monomials:
                    if monom0 == monom:
                        counter0 += 1

            counter1: int = 0

            for monom in other.monomials:
                for monom0 in self.monomials:
                    if monom0 == monom:
                        counter1 += 1

            equals = counter0 == counter1 and counter0 == len(self.monomials)

        return equals

    @staticmethod
    def parse_brackets(text: str):
        text = text.replace("[", "|")
        text = text.replace("]", "|")

        l: list[str] = text.split("|")

        polynomial: Polynomial = Polynomial(monoms=[Monomial(coeff=Rational(1))])

        for s in l:
            s = s.strip()

            if s:
                p: Polynomial = Polynomial.parse_single(s)

                polynomial *= p

        return polynomial

    @staticmethod
    def parse(text: str):
        list_list_monomials: list[(list[Monomial], str)] = Polynomial.parse_monomials(text)

        list_polynomials: list[Polynomial] = []

        for l0 in list_list_monomials:
            polynomial: Polynomial = Polynomial(monoms=l0[0], nm=l0[1])

            list_polynomials.append(polynomial)

        return list_polynomials

    @staticmethod
    def parse_single(text: str):
        l: list = Polynomial.parse(text)

        if isinstance(l, list) and len(l) == 1:
            return l[0]

    # def __eq__(self, other):
    #   return

    def __add__(self, other):
        polynomial: Polynomial = Polynomial(self.monomials)

        for monom in other.monomials:
            polynomial.add_monomial(monom)

        return polynomial

    def __str__(self):
        s: str = ""

        if self.name:
            s = f"{self.name} = "

        s0: str = " + ".join(f"{monom}" for monom in self.monomials)

        s0 = f"({s0})"

        if self.power != Rational(1):
            s0 = f"{s0}^{Fore.LIGHTYELLOW_EX}{self.power}{Style.RESET_ALL}"

        s = f"{s}{s0}"

        return s

class PolynomialProduct:
    def __init__(self, polynoms=None, coeff: Rational = Rational(1), const_coeffs: dict[str, Element] = {}):
        if polynoms is None:
            polynoms = []

        self.list_polynomials = polynoms

        self.coefficient: Rational = coeff

        self.const_coefficients: dict[str, Element] = copy.deepcopy(const_coeffs)

        #if self.list_polynomials is None or len(self.list_polynomials) < 1:
         #   self.list_polynomials = [Polynomial.create_one()]

    def __iter__(self):
        for polynomial in self.list_polynomials:
            yield polynomial

    def mul_polynomial(self, input_polynomial):
        flag: bool = False

        for polynom in self.list_polynomials:
            if polynom.base_equals(input_polynomial):
                polynom.power += input_polynomial.power

                flag = True

        if not flag:
            self.list_polynomials.append(input_polynomial)

    def __str__(self):
        list_polynoms: list[Polynomial] = list(filter(lambda p: not p.is_one(), self.list_polynomials))

        if len(list_polynoms) < 1:
            list_polynoms = self.list_polynomials[0:1]

        s: str = "*".join(f"{polynom}" for polynom in list_polynoms)

        if len(self.const_coefficients) > 0:
            s0: str = "*".join([f"({const_coeff})" for const_coeff in self.const_coefficients])

            s = f"{Fore.RED}{s0}{Style.RESET_ALL}*{s}"

        if self.coefficient != Rational(1):
            s = f"{Fore.LIGHTMAGENTA_EX}{self.coefficient}{Style.RESET_ALL}*{s}"

        return s