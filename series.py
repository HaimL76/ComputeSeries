from element import Element
from monomial import Monomial


class Series:
    def __init__(self, d: dict = {}, pow: str = ""):
        elems: dict = {}

        for key in d.keys():
            val: int = d[key]

            elems[key] = Element(symb=key, pow=val)

        self.monomial: Monomial = Monomial(elems=elems)
        self.power: str = pow

    def __str__(self):
        return f"({self.monomial})^{self.power}"
