import copy

from colorama import Fore, Style

from element import Element
from monomial import Monomial
from rational import Rational


class Polynomial:
    def __init__(self, monoms: list = [], nm: str = "", pow0: Rational = Rational(1), in_product: bool = False):
        self.monomials: list = copy.deepcopy(monoms)
        self.name: str = nm
        self.power: Rational = pow0
        self.in_polynomial_product: bool = in_product

        if self.power > Rational(0):
            _ = 0

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

                found: bool = False
                index: int = 0

                while not found and index < len(monoms):
                    mon: Monomial = monoms[index]
                    index += 1

                    if Monomial.are_same_monomials(mon, m):
                        if mon.is_minus == m.is_minus:
                            mon.coefficient = abs(mon.coefficient + m.coefficient)
                        else:
                            coeff0: Rational = mon.coefficient - m.coefficient

                            if coeff0 < Rational(0):
                                mon.is_minus = not mon.is_minus

                            mon.coefficient = abs(coeff0)

                        found = True

                if not found:
                    monoms.append(m)

        monoms = [m for m in monoms if m.coefficient != Rational(0)]

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
    def parse_monomials(text: str, list_const_coeffs: list[str]):
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

                    l2: list[(str, bool)] = []

                    buffer: list[str] = []

                    is_minus: bool = False

                    counter_round: int = 0
                    counter_square: int = 0
                    counter_curly: int = 0

                    for ch in s1:
                        if ch == "(":
                            counter_round += 1

                        if ch == ")":
                            counter_round -= 1

                        if ch == "{":
                            counter_curly += 1

                        if ch == "}":
                            counter_curly -= 1

                        check_sign: bool = counter_round == 0 and counter_curly == 0

                        if check_sign and ch in ["+", "-"]:
                            if buffer is not None and len(buffer) > 0:
                                l2.append(("".join(buffer), is_minus))
                                buffer = []

                            is_minus = ch == "-"
                        else:
                            if buffer is None:
                                buffer = []

                            buffer.append(ch)

                    if buffer is not None and len(buffer) > 0:
                        l2.append(("".join(buffer), is_minus))

                    if isinstance(l2, list) and len(l2) > 0:
                        list_monomials: list = []

                        for tup in l2:
                            s2: str = tup[0]

                            is_minus: bool = tup[1]

                            s2 = s2.strip()

                            if s2:
                                monomial: Monomial = Monomial.parse(s2, list_const_coeffs)

                                if monomial:
                                    monomial.is_minus = is_minus
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
    def parse_polynomial_with_round_brackets(text: str):
        list_strings: list[str] = []

        if text:
            index_left: int = text.find("(")
            index_right: int = text.find(")")

            if -1 < index_left < index_right:
                list_strs: list[str] = []

                list_buffer: list[str] = []

                str_to_append: str = ""

                for s1 in text:
                    if s1 == "(" and isinstance(list_buffer, list) and len(list_buffer) > 0:
                        str_to_append = "".join(list_buffer)

                        if list_strs[-1] == "-":
                            str_to_append = f"-{str_to_append}"

                        list_buffer = []
                    elif s1 == ")" and isinstance(list_buffer, list) and len(list_buffer) > 0:
                        if str_to_append:
                            if str_to_append[0] in ["+", "-"] and list_strs[-1] in ["+", "-"]:
                                list_strs[-1] = str_to_append
                            else:
                                list_strs.append(str_to_append)

                        list_strs.append("".join(list_buffer))
                        list_buffer = []
                    elif s1 in ["+", "-"]:
                        if list_buffer is not None and len(list_buffer) > 0:
                            if str_to_append:
                                if str_to_append[0] in ["+", "-"] and list_strs[-1] in ["+", "-"]:
                                    list_strs[-1] = str_to_append
                                else:
                                    list_strs.append(str_to_append)

                            list_strs.append("".join(list_buffer))

                            list_strs.append(s1)
                            list_buffer = []
                    else:
                        if list_buffer is None:
                            list_buffer = []

                        list_buffer.append(s1)

                if isinstance(list_buffer, list) and len(list_buffer) > 0:
                    if str_to_append:
                        if str_to_append[0] in ["+", "-"] and list_strs[-1] in ["+", "-"]:
                            list_strs[-1] = str_to_append
                        else:
                            list_strs.append(str_to_append)

                    list_strs.append("".join(list_buffer))
                    list_buffer = []

                if isinstance(list_strs, list) and len(list_strs) > 0:
                    list_strings.append("".join(list_strs))
            else:
                list_strings.append(text)

        return list_strings

    @staticmethod
    def parse_arithmetic_series(text: str):
        list_strings: list[str] = []

        arr: list[str] = text.split("...")

        if isinstance(arr, list) and len(arr) == 2:
            s0: str = arr[0]
            s1: str = arr[1]

            s0 = s0.strip()
            s1 = s1.strip()

            list_strs: list[str] = []

            if s0 and s1:
                list_strs = Polynomial.parse_polynomial_with_round_brackets(s0)

                if isinstance(list_strs, list) and len(list_strs) > 0:
                    for s in list_strs:
                        list_strings.append(s)

                list_strs = Polynomial.parse_polynomial_with_round_brackets(s1)

                if isinstance(list_strs, list) and len(list_strs) > 0:
                    for s in list_strs:
                        list_strings.append(s)

        return list_strings

    @staticmethod
    def compute_arithmetic_series(s0: str, s1: str, list_const_coeffs: list[str] = []):
        p0: Polynomial = Polynomial.parse_single(s0, list_const_coeffs)
        p1: Polynomial = Polynomial.parse_single(s1, list_const_coeffs)

        sum_elements: Polynomial = p1 + p0

        _ = 0

    @staticmethod
    def parse_brackets(text: str, list_const_coeffs: list[str]):
        text = text.replace("[", "|")
        text = text.replace("]", "|")

        list_polynomials: list[str] = text.split("|")

        list_strings: list[str] = []

        list_series_polynomials: list[str] = []

        for text in list_polynomials:
            text = text.strip()

            if text:
                list_strs: list[str] = []

                if "..." in text:
                    list_series_polynomials = Polynomial.parse_arithmetic_series(text)
                else:
                    list_strs = Polynomial.parse_polynomial_with_round_brackets(text)

                    if isinstance(list_strs, list) and len(list_strs) > 0:
                        for s in list_strs:
                            s = s.strip()

                            if s:
                                list_strings.append(copy.deepcopy(s))

        if len(list_strings) > 0:
            list_polynomials = copy.deepcopy(list_strings)

        polynomial: Polynomial = Polynomial(monoms=[Monomial(coeff=Rational(1))])

        for s in list_polynomials:
            s = s.strip()

            if s:
                p: Polynomial = Polynomial.parse_single(s, list_const_coeffs=list_const_coeffs)

                polynomial *= p

        if isinstance(list_series_polynomials, list) and len(list_series_polynomials) == 2:
            Polynomial.compute_arithmetic_series(list_series_polynomials[0], list_series_polynomials[1],
                                                 list_const_coeffs=list_const_coeffs)

        return polynomial

    @staticmethod
    def parse(text: str, list_const_coeffs: list[str]):
        list_list_monomials: list[(list[Monomial], str)] = Polynomial.parse_monomials(text, list_const_coeffs)

        list_polynomials: list[Polynomial] = []

        for l0 in list_list_monomials:
            polynomial: Polynomial = Polynomial(monoms=l0[0], nm=l0[1])

            list_polynomials.append(polynomial)

        return list_polynomials

    @staticmethod
    def parse_single(text: str, list_const_coeffs: list[str]):
        l: list = Polynomial.parse(text, list_const_coeffs)

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
        return self.get_ltx_str()

    def get_str(self):
        s: str = ""

        if self.name:
            s = f"{self.name} = "

        s0: str = " + ".join(f"{monom}" for monom in self.monomials)

        s0 = f"({s0})"

        if self.power != Rational(1):
            s0 = f"{s0}^{Fore.LIGHTYELLOW_EX}{self.power}{Style.RESET_ALL}"

        s = f"{s}{s0}"

        return s

    def get_ltx_str(self):
        s: str = ""

        s0: str = ""

        for monom in self.monomials:
            if len(s0) > 0:
                s1: str = "-" if monom.is_minus else "+"
                s0 = f"{s0}{s1}"

            s0 = f"{s0}{monom}"

        if self.in_polynomial_product or self.power != Rational(1):
            s0 = f"({s0})"

        if self.power != Rational(1):
            s0 = f"{s0}^{{{self.power}}}"

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
        input_polynomial = copy.deepcopy(input_polynomial)

        flag: bool = False

        for polynom in self.list_polynomials:
            if polynom.base_equals(input_polynomial):
                polynom.power += input_polynomial.power

                flag = True

        if not flag:
            self.list_polynomials.append(input_polynomial)

    def __str__(self):
        return self.get_ltx_str()

    def get_ltx_str(self):
        list_polynoms: list[Polynomial] = list(filter(lambda p: not p.is_one(), self.list_polynomials))

        if len(list_polynoms) < 1:
            list_polynoms = self.list_polynomials[0:1]

        s: str = "".join(f"{polynom}" for polynom in list_polynoms)

        if len(self.const_coefficients) > 0:
            s0: str = "".join([f"{const_coeff.get_copy_with_parentheses()}" for const_coeff in self.const_coefficients.values()])

            s = f"{s0}{s}"

        if self.coefficient != Rational(1):
            s = f"{self.coefficient}{s}"

        return s

    @property
    def get_str(self):
        list_polynoms: list[Polynomial] = list(filter(lambda p: not p.is_one(), self.list_polynomials))

        if len(list_polynoms) < 1:
            list_polynoms = self.list_polynomials[0:1]

        s: str = "*".join(f"{polynom}" for polynom in list_polynoms)

        if len(self.const_coefficients) > 0:
            s0: str = "*".join([f"({const_coeff})" for const_coeff in self.const_coefficients.values()])

            s = f"{Fore.RED}{s0}{Style.RESET_ALL}*{s}"

        if self.coefficient != Rational(1):
            s = f"{Fore.LIGHTMAGENTA_EX}{self.coefficient}{Style.RESET_ALL}*{s}"

        return s