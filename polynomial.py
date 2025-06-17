import copy

from colorama import Fore, Style

from monomial import Monomial
from rational import Rational


class Polynomial:
    def __init__(self, monoms: list = [], nm: str = ""):
        self.monomials: list = copy.deepcopy(monoms)
        self.name: str = nm

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

        s = f"{s}{s0}"

        return s


class PolynomialWithPower(Polynomial):
    def __init__(self, monoms: list = [], nm: str = "", pow: Rational = Rational(1)):
        super().__init__(monoms=monoms, nm=nm)
        self.power: Rational = pow

    def __str__(self):
        s = super().__str__()

        if self.power != Rational(1):
            s = f"({s})^{Fore.LIGHTYELLOW_EX}{self.power}{Style.RESET_ALL}"

        return s

    def __eq__(self, other):
        equals: bool = False

        if len(self.monomials) == len(other.monomials):
            counter0: int = 0

            for monom in self.monomials:
                if monom in other.monomials:
                    counter0 += 1

            counter1: int = 0

            for monom in other.monomials:
                if monom in self.monomials:
                    counter1 += 1

            equals = counter0 == counter1 and counter0 == len(self.monomials)

        return equals

    @staticmethod
    def parse(text: str):
        list_list_monomials: list[(list[Monomial], str)] = Polynomial.parse_monomials(text)

        list_polynomials: list[PolynomialWithPower] = []

        for l0 in list_list_monomials:
            polynomial: PolynomialWithPower = PolynomialWithPower(monoms=l0[0], nm=l0[1])

            list_polynomials.append(polynomial)

        return list_polynomials

    @staticmethod
    def parse_single(text: str):
        l: list[PolynomialWithPower] = PolynomialWithPower.parse(text)

        if isinstance(l, list) and len(l) == 1:
            return l[0]
