from monomial import Monomial
from polynomial import Polynomial


class VariableSubstitution:
    def __init__(self):
        self.substitution: dict = {}

    def add_mapping(self, symb: str, polynom: Polynomial):
        self.substitution[symb] = polynom

    def substitute_monomial(self, original_monomial: Monomial):
        l: list = []

        for symb in self.substitution.keys():
            if symb in original_monomial:
                val: Polynomial = self.substitution[symb]

                if val is not None:
                    original_monomial.remove_element(symb)

                    for monom in val:
                        m = original_monomial * monom

                        l.append(m)

        return l

    def substitude_polynomial(self, original_polynom: Polynomial):
        polynomial: Polynomial = Polynomial()

        for monom in original_polynom:
            monoms: list = self.substitute_monomial(monom)

            if not isinstance(monoms, list) or len(monoms) < 1:
                monoms = [monom]

            for monom in monoms:
                polynomial.add_monomial(monom)

        return polynomial