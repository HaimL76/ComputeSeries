class Rational:
    def __init__(self, numer: int, denom: int = 1):
        self.numerator: int = numer
        self.denominator: int = denom

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
        s: str = f"{self.numerator}"

        if self.denominator != 1:
            s = f"{s}/{self.denominator}"

        return s

class Element:
    def __init__(self, symb: str = "", pow: int = 1):
        self.power: int = pow
        self.symbol: str = symb

    def __mul__(self, other):
        result = None

        if self.symbol == other.symbol:
            result = Element(symb=self.symbol)

            result.power = self.power + other.power

            ##result.coefficient = self.coefficient * other.coefficient

            result.sign = self.sign != other.sign

        return result

    def __eq__(self, other):
        return self.symbol == other.symbol and self.power == other.power

    @staticmethod
    def parse(text: str):
        l: list = []

        l0: list = text.split("^")

        symb: str = text
        pow: int = 1

        if len(l0) == 2:
            symb = l0[0].strip()

            spow = l0[1].strip()

            if spow.isnumeric():
                pow = int(spow)

        return Element(symb, pow)

    def __str__(self):
        s: str = self.symbol

        if self.power != 1:
            s = f"{s}^{self.power}"

        return s


class Monomial:
    def __init__(self, elems: dict = {}, coeff: Rational = Rational(1), const_coeff: str = ""):
        self.elements: dict = {}

        if isinstance(elems, dict):
            self.elements = elems
        elif isinstance(elems, list):
            for elem in elems:
                if elem.symbol not in self.elements:
                    self.elements[elem.symbol] = Element(symb=elem.symbol, pow=elem.power)
                else:
                    self.elements[elem.symbol] *= elem

        self.coefficient: Rational = coeff
        self.const_coefficient: str = const_coeff

    @staticmethod
    def are_same_monomials(monom1, monom2):
        l: list = list(monom1.elements.keys())

        mons: list = [monom1, monom2]

        different: bool = False
        index = 0

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

    def __iter__(self):
        for symb in self.elements.keys():
            yield symb

    def __mul__(self, other):
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

        return Monomial(elems, coeff=coeff)

    @staticmethod
    def parse(text: str):
        coeff: Rational = Rational(1)

        l: list = []

        l0: list = text.split(".")

        for s in l0:
            s = s.strip()

            if s:
                if s.isnumeric():
                    coeff = Rational.parse(s)
                else:
                    element: Element = Element.parse(s)

                    if element:
                        l.append(element)

        return Monomial(l, coeff=coeff)

    def remove_element(self, symb: str):
        if symb in self.elements:
            self.elements.pop(symb)

    def __str__(self):
        s: str = ""

        if self.elements is None or len(self.elements) < 1:
            s = f"{self.coefficient}"
        else:
            if self.coefficient != Rational(1):
                s = f"{self.coefficient}"

            if self.const_coefficient:
                if len(s) > 0:
                    s = f"{s}*"

                s = f"{s}{self.const_coefficient}"

            s0: str = ""

            if len(self.elements) > 0:
                s0 = "*".join(f"{elem}" for elem in self.elements.values())

            if len(s0) > 0:
                if len(s) > 0:
                    s = f"{s}*"

                s = f"{s}{s0}"

        return s


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

class Exponential:
    def __init__(self, symb: str, exp: Polynomial):
        self.symbol: str = symb
        self.exponent: Polynomial = exp

    def __mul__(self, other):
        return Exponential(symb=self.symbol, exp=self.exponent + other.exponent)

    def __str__(self):
        return f"{self.symbol}^({self.exponent})"

    @staticmethod
    def parse(text: str):
        exponential = None

        l: list = text.split("^")

        if isinstance(l, list) and len(l) == 2:
            exponential = Exponential(symb=l[0], exp=Polynomial.parse(l[1]))

        return exponential


class ExponentialExpression:
    def __init__(self, exps: list=[]):
        self.exponentials: dict = {}

        for exp in exps:
            if isinstance(exp, Exponential) and exp.symbol:
                self.add_exponential(exp)

    def add_exponential(self, exp: Exponential):
        if exp.symbol:
            if exp.symbol not in self.exponentials:
                self.exponentials[exp.symbol] = exp
            else:
                self.exponentials[exp.symbol] *= exp

    def __mul__(self, other):
        return Exponential(symb=self.symbol, exp=self.exponent + other.exponent)

    def __str__(self):
        return "*".join(f"{exp}" for exp in self.exponentials.values())

    def break_by_exponent(self):
        exponent_symbols: dict = {}

        for base_symbol in self.exponentials.keys():
            exp: Exponential = self.exponentials[base_symbol]

            exponent_polynomial: Polynomial = exp.exponent

            for monom in exponent_polynomial.monomials:
                elem_symbol: str = next(iter(monom.elements))
                elem: Element = monom.elements[elem_symbol]

                if elem_symbol not in exponent_symbols:
                    exponent_symbols[elem_symbol] = {}

                d = exponent_symbols[elem_symbol]

                if base_symbol not in d:
                    d[base_symbol] = monom.coefficient
                else:
                    d[base_symbol] += monom.coefficient

    @staticmethod
    def parse(text: str):
        exponential = None

        l: list = text.split("^")

        if isinstance(l, list) and len(l) == 2:
            exponential = Exponential(symb=l[0], exp=Polynomial.parse(l[1]))

        return exponential


p1 = Polynomial.parse("3.v1+v2")
p2 = Polynomial.parse("1+v3")


print(f"p1 = {p1}")
print(f"p2 = {p2}")

v1 = Polynomial.parse("2.a+b+c")

print(f"v1 = {v1}")

substitution: VariableSubstitution = VariableSubstitution()

substitution.add_mapping(symb="v1", polynom=v1)

a = substitution.substitude_polynomial(p1)

p: Polynomial = p1 * p2

exp1: Exponential = Exponential.parse("p^2.a+3.b")
exp2: Exponential = Exponential.parse("p^5.a+3.c")

exp3: Exponential = Exponential.parse("t^67.a+3.b")
exp4: Exponential = Exponential.parse("t^5.a+13.c")

print(f"exp1={exp1}")
print(f"exp2={exp2}")

exp12: Exponential = exp1 * exp2

print(f"exp12={exp12}")

print(f"exp3={exp3}")
print(f"exp4={exp4}")

exp34: Exponential = exp3 * exp4

print(f"exp12={exp12}")
print(f"exp34={exp34}")

expression1: ExponentialExpression = ExponentialExpression(exps=[exp1, exp2, exp3, exp4])
expression2: ExponentialExpression = ExponentialExpression(exps=[exp12, exp34])

expression2.break_by_exponent()

print(f"expression1 = {expression1}")
print(f"expression2 = {expression2}")

print(f"p = {p}")
print(f"a = {a}")
