import copy

from element import Element
from rational import Rational


class Monomial:
    def __init__(self, elems: dict = {}, coeff: Rational = Rational(1),
                  const_coeffs: dict[str, Element] = {}, minus: bool = False):
        self.is_minus: bool = minus

        self.elements: dict = {}

        if isinstance(elems, dict):
            self.elements = copy.deepcopy(elems)
        elif isinstance(elems, list):
            for elem in elems:
                if elem.symbol not in self.elements:
                    self.elements[elem.symbol] = Element(symb=elem.symbol, pow=elem.power)
                else:
                    self.elements[elem.symbol] *= elem

        self.coefficient: Rational = abs(coeff)

        if coeff.is_minus():
            self.is_minus = not self.is_minus

        self.const_coefficients: dict[str, Element] = copy.deepcopy(const_coeffs)
        ##self.power: int = 1

    @staticmethod
    def are_same_monomials(monom1, monom2):
        l: list = list(monom1.elements.keys())

        mons: list = [monom1, monom2]

        different: bool = False
        index = 0

        const_coeff1 = None
        const_coeff2 = None

        if len(monom1.const_coefficients) > 0:
            const_coeff1 = next(iter(monom1.const_coefficients.values()))

        if len(monom2.const_coefficients) > 0:
            const_coeff2 = next(iter(monom2.const_coefficients.values()))

        counter = 0

        if const_coeff1 is not None:
            counter += 1

        if const_coeff2 is not None:
            counter += 1

        if counter == 1:
            return False

        if const_coeff1 is not None and const_coeff2 is not None:
            are_same = const_coeff1.symbol == const_coeff2.symbol and const_coeff1.power == const_coeff2.power

            if not are_same:
                return False

        while not different and index < len(mons):
            m1: Monomial = mons[index]
            m2: Monomial = mons[(index + 1) % 2]
            index += 1

            index0: int = 0

            l: list = list(m1.elements.keys())

            while not different and index0 < len(l):
                symb: str = l[index0]
                index0 += 1

                if symb not in m2:
                    different = True
                else:
                    elem1: Element = m1.elements[symb]
                    elem2: Element = m2.elements[symb]

                    if elem1 != elem2:
                        different = True

        return not different

    def __eq__(self, other):
        equals: bool = False

        if (self.coefficient == other.coefficient and
                len(self.elements) == len(other.elements)):
            counter0: int = 0

            for key in self.elements.keys():
                if key in other.elements.keys():
                    elem_self = self.elements[key]
                    elem_other = other.elements[key]

                    if elem_self.power == elem_other.power:
                        counter0 += 1

            counter1: int = 0

            for key in other.elements.keys():
                if key in self.elements.keys():
                    elem_self = self.elements[key]
                    elem_other = other.elements[key]

                    if elem_self.power == elem_other.power:
                        counter1 += 1

            return counter0 == counter1 and counter0 == len(self.elements)

        return equals

    def __iter__(self):
        for symb in self.elements.keys():
            yield symb

    def __mul__(self, other):
        const_coeffs: dict = copy.deepcopy(self.const_coefficients)

        if isinstance(other.const_coefficients, dict) and len(other.const_coefficients):
            for key in other.const_coefficients:
                val_other = other.const_coefficients[key]

                if key not in const_coeffs:
                    const_coeffs[key] = Element(symb=key, pow=0)

                val: Element = const_coeffs[key]
                const_coeffs[key] = Element(val.symbol, val.power + val_other.power)

        coeff: int = self.coefficient * other.coefficient

        elems: dict = {}

        for symb in self.elements.keys():
            val = self.elements[symb]

            elems[symb] = val

        for symb in other.elements.keys():
            val = other.elements[symb]

            if symb not in elems:
                elems[symb] = val
            else:
                elems[symb] *= val

        is_minus: bool = self.is_minus != other.is_minus

        return Monomial(elems, coeff=coeff, const_coeffs=const_coeffs, minus=is_minus)

    @staticmethod
    def parse(text: str, list_const_coeffs: list[str]):
        coeff: Rational = Rational(1)
        const_coeffs: dict = {}

        l: list = []

        l0: list = text.split(".")

        for s in l0:
            s = s.strip()

            if s:
                found = False

                if "^" in s:
                    list0 = s.split("^")

                    if len(list0) == 2:
                        s0_0 = list0[0]
                        s0_1 = list0[1]

                        if s0_0 in list_const_coeffs and s0_1.isnumeric():
                            if s0_0 not in const_coeffs:
                                const_coeffs[s0_0] = Element(symb=s0_0, pow=0)

                            val: Element = const_coeffs[s0_0]
                            const_coeffs[s0_0] = Element(val.symbol, val.power + int(s0_1))
                elif s.isnumeric():
                    coeff = Rational.parse(s)
                elif s in list_const_coeffs:
                    const_coeff: str = s

                    if const_coeff not in const_coeffs:
                        const_coeffs[const_coeff] = Element(symb=const_coeff, pow=0)

                    val: Element = const_coeffs[const_coeff]
                    const_coeffs[const_coeff] = Element(val.symbol, val.power + 1)
                else:
                    element: Element = Element.parse(s)

                    if element:
                        l.append(element)

        return Monomial(l, coeff=coeff, const_coeffs=const_coeffs)

    def is_one(self):
        return ((self.elements is None or len(self.elements) < 1)
                and (self.const_coefficients is None or len(self.const_coefficients) < 1)
                and self.coefficient == Rational(1))


    def remove_element(self, symb: str):
        if symb in self.elements:
            self.elements.pop(symb)

    def __str__(self):
        return self.get_ltx_str()

    def get_ltx_str(self):
        s: str = ""

        counter: int = 0

        if self.coefficient != Rational(1) or (len(self.elements) < 1 and len(self.const_coefficients) < 1):
            s = f"{self.coefficient}"
            counter += 1

        const_coeffs: dict = self.const_coefficients

        if isinstance(const_coeffs, dict) and len(const_coeffs) > 0:
            for key in const_coeffs.keys():
                const_coeff: Element = const_coeffs[key]

                if counter > 0:
                    s = f"{s}"

                s = f"{s}({const_coeff.symbol})"

                if const_coeff.power != 1:
                    s = f"{s}^{const_coeff.power}"

                counter += 1

        if isinstance(self.elements, dict) and len(self.elements) > 0:
            s0: str = ""

            if len(self.elements) > 0:
                s0 = "".join(f"{elem}" for elem in self.elements.values())

            if len(s0) > 0:
                if len(s) > 0:
                    s = f"{s}"

                s = f"{s}{s0}"
                counter += 1

        ##if self.power != 1:
          ##  s = f"({s}^{self.power})"

        return s

    def get_str(self):
        s: str = ""

        counter: int = 0

        if self.coefficient != Rational(1) or (len(self.elements) < 1 and len(self.const_coefficients) < 1):
            s = f"{self.coefficient}"
            counter += 1

        const_coeffs: dict = self.const_coefficients

        if isinstance(const_coeffs, dict) and len(const_coeffs) > 0:
            for key in const_coeffs.keys():
                const_coeff: Element = const_coeffs[key]

                if counter > 0:
                    s = f"{s}*"

                s = f"{s}({const_coeff.symbol})"

                if const_coeff.power != 1:
                    s = f"{s}^{const_coeff.power}"

                counter += 1

        if isinstance(self.elements, dict) and len(self.elements) > 0:
            s0: str = ""

            if len(self.elements) > 0:
                s0 = "*".join(f"{elem}" for elem in self.elements.values())

            if len(s0) > 0:
                if len(s) > 0:
                    s = f"{s}*"

                s = f"{s}{s0}"
                counter += 1

        ##if self.power != 1:
          ##  s = f"({s}^{self.power})"

        return s
