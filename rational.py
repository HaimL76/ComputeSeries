import math


class Rational:
    primes: list[int] = [2, 3, 5, 7, 11]

    def reduce(self):
        check_reduce: bool = abs(self.numerator) != 1 and abs(self.denominator) != 1

        if check_reduce:
            is_reduced: bool = False

            index: int = 0

            while not is_reduced and index < len(Rational.primes):
                prime: int = Rational.primes[index]

                is_reduced_for_prime: bool = False

                while not is_reduced and not is_reduced_for_prime:
                    numer0 = self.numerator / prime
                    denom0 = self.denominator / prime

                    if numer0 == math.floor(numer0) and denom0 == math.floor(denom0):
                        self.numerator = int(numer0)
                        self.denominator = int(denom0)

                        if abs(self.numerator) == 1 or abs(self.denominator) == 1:
                            is_reduced = True
                    else:
                        is_reduced_for_prime = True

                index += 1

    def __init__(self, numer: int, denom: int = 1):
        self.numerator: int = numer
        self.denominator: int = denom

        self.reduce()

    def __gt__(self, other):
        return self.numerator * other.denominator > other.numerator * self.denominator

    def is_minus(self):
        return self.numerator * self.denominator < 0

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

    def __abs__(self):
        numer: int = self.numerator
        denom: int = self.denominator

        if numer < 0 < denom:
            numer *= -1

        if denom < 0 < numer:
            denom *= -1

        return Rational(numer=numer, denom=denom)

    def __sub__(self, other):
        minus_other: Rational = Rational(numer=other.numerator * -1, denom=other.denominator)

        return self + minus_other

    def __mul__(self, other):
        return Rational(numer=self.numerator * other.numerator, denom=self.denominator * other.denominator)

    def __eq__(self, other):
        return self.numerator == other.numerator and self.denominator == other.denominator

    def __str__(self):
        return self.get_str()

    def get_ltx_str(self):
        return self.get_str(is_latex=True)

    def get_sage_str(self):
        return self.get_str(is_latex=False)

    def get_str(self, is_latex: bool = True):
        s: str = f"{self.numerator}"

        if self.denominator != 1:
            if not is_latex:
                _ = 0

            s = f"\\frac{{{s}}}{{{self.denominator}}}" if is_latex else f"{s}/{self.denominator}"

        return s
