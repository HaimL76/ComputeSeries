from monomial import Monomial


class Polynomial:
    def __init__(self, monoms: list = [], nm: str = ""):
        self.monomials: list = []
        self.name: str = nm

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
        list_polynomials: list = []

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
                            polynomial: Polynomial = Polynomial(monoms=list_monomials, nm=name)

                            list_polynomials.append(polynomial)

        return list_polynomials

    @staticmethod
    def parse_single(text: str):
        l: list = Polynomial.parse(text)

        if isinstance(l, list) and len(l) == 1:
            return l[0]


    def __add__(self, other):
        polynomial: Polynomial = Polynomial(self.monomials)

        for monom in other.monomials:
            polynomial.add_monomial(monom)

        return polynomial

    def __str__(self):
        s: str = ""

        if self.name:
            s = f"{self.name} = "

        s += " + ".join(f"{monom}" for monom in self.monomials)

        return s
