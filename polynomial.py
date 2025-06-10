from monomial import Monomial


class Polynomial:
    def __init__(self, monoms: list = []):
        self.monomials: list = []

        for monom in monoms:
            self.monomials.append(monom)

    def __iter__(self):
        for monom in self.monomials:
            yield monom

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
    def parse(text: str):
        l: list = []

        l0: list = text.split("+")

        for s in l0:
            s = s.strip()

            if s:
                monomial: Monomial = Monomial.parse(s)

                if monomial:
                    l.append(monomial)

        return Polynomial(monoms=l)


    def __add__(self, other):
        polynomial: Polynomial = Polynomial(self.monomials)

        for monom in other.monomials:
            polynomial.add_monomial(monom)

        return polynomial

    def __str__(self):
        return " + ".join(f"{monom}" for monom in self.monomials)
