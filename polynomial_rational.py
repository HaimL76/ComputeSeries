import copy

from polynomial import Polynomial, PolynomialWithPower
from rational import Rational


class PolynomialRational:
    def __init__(self, numer: PolynomialWithPower, denom: PolynomialWithPower):
        self.numerator: PolynomialWithPower = copy.deepcopy(numer)
        self.denominator: PolynomialWithPower = copy.deepcopy(denom)

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

class MultiplePolynomialRational:
    def __init__(self, numer: dict[Polynomial, int], denom: dict[Polynomial, int]):
        self.numerator: dict[Polynomial, int] = copy.deepcopy(numer)
        self.denominator: dict[Polynomial, int] = copy.deepcopy(denom)


    def __mul__(self, other):
        for numer in other.numerator.keys():
            #numer = other.numerator[key]

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
