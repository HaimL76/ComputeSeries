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
                key: str = elem.symbol

                if elem.index is not None:
                    key += f"_{elem.index}"

                if elem.symbol not in self.elements:
                    self.elements[key] = Element(symb=elem.symbol, pow=elem.power, ind=elem.index)
                else:
                    self.elements[key] *= elem

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
        if text.startswith("p^{") and "t^{" in text:
            str0: str = ""

            found: bool = False
            i: int = 0
            while not found and i < len(text):
                ch = text[i]
                i += 1

                str0 += ch

                if ch == "}":
                    found = True

            str1: str = ""

            found: bool = False
            while not found and i < len(text):
                ch = text[i]
                i += 1

                str1 += ch

                if ch == "}":
                    found = True

            if len(str0) > 0 and len(str1) > 0:
                elem0: Element = Element.parse(str0)
                elem1: Element = Element.parse(str1)

                if elem0 is not None and elem1 is not None:
                    return Monomial(elems={elem0.symbol: elem0, elem1.symbol: elem1}, coeff=Rational(1), const_coeffs={})

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

                            found = True

                if not found:
                    found_coeff = None

                    if "/" in s:
                        arr01: list[str] = s.split("/")

                        if isinstance(arr01, list) and len(arr01) == 2:
                            if (arr01[0].isnumeric() and arr01[1].isnumeric()):
                                found_coeff = Rational(numer=int(arr01[0]), denom=int(arr01[1]))

                    if s.isnumeric() or found_coeff is not None:
                        coeff = found_coeff if found_coeff is not None else Rational.parse(s)
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

    Disable_Print_Sign = 0
    Print_Sign_If_Minus = 1
    Print_Sign_Anyway = 2

    def get_sage_str(self, print_sign: int = Disable_Print_Sign):
        return self.get_str(print_sign=print_sign, is_latex=False)

    def get_ltx_str(self, print_sign: int = Disable_Print_Sign):
        return self.get_str(print_sign=print_sign, is_latex=True)

    def get_str(self, print_sign: int = Disable_Print_Sign, is_latex: bool=True):
        str_output: str = ""

        counter: int = 0

        if self.coefficient != Rational(1) or (len(self.elements) < 1 and len(self.const_coefficients) < 1):
            str_output = f"{self.coefficient.get_str(is_latex=is_latex)}"

            if not is_latex and self.coefficient.denominator != Rational(1):
                str_output = f"({str_output})"

            counter += 1

        const_coeffs: dict = self.const_coefficients

        if isinstance(const_coeffs, dict) and len(const_coeffs) > 0:
            for key in const_coeffs.keys():
                const_coeff: Element = const_coeffs[key]

                if counter > 0:
                    str_output = f"{str_output}"

                str_const_coefficient = const_coeff.symbol

                if len(const_coeff.symbol) > 1:
                    str_const_coefficient = f"({str_const_coefficient})"
                else:
                    if not is_latex:
                        if str_const_coefficient == "A":
                            str_const_coefficient = "(1-p^{-1})" if is_latex else "(1-(p**-1))"

                            if const_coeff.power > 1:
                                str_const_coefficient = f"{str_const_coefficient}^{const_coeff.power}" if is_latex else f"({str_const_coefficient}**{const_coeff.power})"

                delimiter: str = ""

                if not is_latex and str_output and str_const_coefficient:
                    delimiter = "*"

                str_output = f"{str_output}{delimiter}{str_const_coefficient}"

                if is_latex and const_coeff.power != 1:
                    str_output = f"{str_output}^{const_coeff.power}"

                counter += 1

        if isinstance(self.elements, dict) and len(self.elements) > 0:
            s0: str = ""

            delimiter: str = "" if is_latex else "*"

            if len(self.elements) > 0:
                s0 = delimiter.join(f"{elem.get_str(is_latex=is_latex, remove_underscore=True)}" for elem in self.elements.values())

            if len(s0) > 0:
                if len(str_output) > 0:
                    str_output = f"{str_output}"

                delimiter = ""

                if not is_latex and str_output and s0:
                    delimiter = "*"

                str_output = f"{str_output}{delimiter}{s0}"
                counter += 1

        if print_sign != Monomial.Disable_Print_Sign:
            if print_sign == Monomial.Print_Sign_Anyway or self.is_minus:
                sign = "-" if self.is_minus else "+"

                str_output = f"{sign}{str_output}"

        return str_output