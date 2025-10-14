import copy
from typing import List, Dict, Optional, Tuple, Union

from colorama import Fore, Style

from element import Element
from monomial import Monomial
from rational import Rational


class Polynomial:
    def __init__(self, monoms: Optional[List[Monomial]] = None, nm: str = "", 
                 pow0: Rational = Rational(1), in_product: bool = False):
        """Initialize a polynomial with monomials, name, power, and product flag."""
        self.monomials: List[Monomial] = copy.deepcopy(monoms) if monoms else []
        self.name: str = nm
        self.power: Rational = pow0
        self.in_polynomial_product: bool = in_product

    @staticmethod
    def create_one() -> 'Polynomial':
        """Create a polynomial equal to 1."""
        return Polynomial(monoms=[Monomial()])

    def __iter__(self):
        """Iterate over monomials."""
        for monom in self.monomials:
            yield monom

    def is_one(self) -> bool:
        """Check if the polynomial is equal to 1."""
        return len(self.monomials) == 1 and next(iter(self.monomials)).is_one()

    def __mul__(self, other: 'Polynomial') -> 'Polynomial':
        """Multiply two polynomials."""
        if not isinstance(other, Polynomial):
            return NotImplemented
            
        monoms: List[Monomial] = []

        for monom_self in self.monomials:
            for monom_other in other.monomials:
                m = monom_self * monom_other
                if m is None:
                    continue

                found: bool = False
                for i, existing_monom in enumerate(monoms):
                    if Monomial.are_same_monomials(existing_monom, m):
                        if existing_monom.is_minus == m.is_minus:
                            existing_monom.coefficient = abs(existing_monom.coefficient + m.coefficient)
                        else:
                            coeff_diff: Rational = existing_monom.coefficient - m.coefficient
                            if coeff_diff < Rational(0):
                                existing_monom.is_minus = not existing_monom.is_minus
                            existing_monom.coefficient = abs(coeff_diff)
                        found = True
                        break

                if not found:
                    monoms.append(m)

        # Remove zero monomials
        monoms = [m for m in monoms if m.coefficient != Rational(0)]
        return Polynomial(monoms)

    def add_monomial(self, monomial: Monomial) -> None:
        """Add a monomial to the polynomial."""
        if not isinstance(monomial, Monomial):
            return
            
        found: bool = False
        for existing_monom in self.monomials:
            if Monomial.are_same_monomials(existing_monom, monomial):
                # Combine coefficients
                monomial_coeff = monomial.coefficient
                existing_coeff = existing_monom.coefficient

                if existing_monom.is_minus:
                    existing_coeff = -existing_coeff
                if monomial.is_minus:
                    monomial_coeff = -monomial_coeff

                sum_coefficients = existing_coeff + monomial_coeff

                if sum_coefficients < Rational(0):
                    existing_monom.is_minus = True
                    existing_monom.coefficient = abs(sum_coefficients)
                else:
                    existing_monom.is_minus = False
                    existing_monom.coefficient = sum_coefficients

                found = True
                break

        if not found:
            self.monomials.append(monomial)

    @staticmethod
    def parse_monomials(text: str, list_const_coeffs: List[str]) -> List[Tuple[List[Monomial], str]]:
        """Parse monomials from text input."""
        list_list_monomials: List[Tuple[List[Monomial], str]] = []
        
        if not text or not text.strip():
            return list_list_monomials

        parts: List[str] = text.split(",")

        for s in parts:
            s = s.strip()
            if not s:
                continue
                
            equation_parts: List[str] = s.split("=")
            if not equation_parts:
                continue
                
            name: str = ""
            s1: str = equation_parts[0]

            if len(equation_parts) > 1:
                name = s1
                s1 = equation_parts[1]

            monomial_parts: List[Tuple[str, bool]] = []
            buffer: List[str] = []
            is_minus: bool = False
            counter_round: int = 0
            counter_curly: int = 0

            for ch in s1:
                if ch == "(":
                    counter_round += 1
                elif ch == ")":
                    counter_round -= 1
                elif ch == "{":
                    counter_curly += 1
                elif ch == "}":
                    counter_curly -= 1

                check_sign: bool = counter_round == 0 and counter_curly == 0

                if check_sign and ch in ["+", "-"]:
                    if buffer:
                        monomial_parts.append(("".join(buffer), is_minus))
                        buffer = []
                    is_minus = ch == "-"
                else:
                    buffer.append(ch)

            if buffer:
                monomial_parts.append(("".join(buffer), is_minus))

            if monomial_parts:
                list_monomials: List[Monomial] = []

                for monomial_text, is_negative in monomial_parts:
                    monomial_text = monomial_text.strip()
                    if monomial_text:
                        monomial: Optional[Monomial] = Monomial.parse(monomial_text, list_const_coeffs)
                        if monomial:
                            monomial.is_minus = is_negative
                            list_monomials.append(monomial)

                if list_monomials:
                    list_list_monomials.append((list_monomials, name))

        return list_list_monomials

    def base_equals(self, other: 'Polynomial') -> bool:
        """Check if two polynomials have the same base structure (ignoring coefficients)."""
        if not isinstance(other, Polynomial):
            return False
            
        if len(self.monomials) != len(other.monomials):
            return False

        # Check if all monomials in self exist in other (ignoring coefficients)
        for monom_self in self.monomials:
            found = False
            for monom_other in other.monomials:
                if Monomial.are_same_monomials(monom_self, monom_other):
                    found = True
                    break
            if not found:
                return False

        # Check if all monomials in other exist in self (ignoring coefficients)
        for monom_other in other.monomials:
            found = False
            for monom_self in self.monomials:
                if Monomial.are_same_monomials(monom_self, monom_other):
                    found = True
                    break
            if not found:
                return False

        return True

    @staticmethod
    def parse_polynomial_with_round_brackets(text: str) -> List[str]:
        """Parse polynomial with round brackets."""
        list_strings: List[str] = []
        
        if not text:
            return list_strings
            
        index_left: int = text.find("(")
        index_right: int = text.find(")")

        if -1 < index_left < index_right:
            list_strs: List[str] = []
            list_buffer: List[str] = []
            str_to_append: str = ""

            for s1 in text:
                if s1 == "(" and list_buffer:
                    str_to_append = "".join(list_buffer)
                    if list_strs and list_strs[-1] == "-":
                        str_to_append = f"-{str_to_append}"
                    list_buffer = []
                elif s1 == ")" and list_buffer:
                    if str_to_append:
                        if (str_to_append[0] in ["+", "-"] and 
                            list_strs and list_strs[-1] in ["+", "-"]):
                            list_strs[-1] = str_to_append
                        else:
                            list_strs.append(str_to_append)
                    list_strs.append("".join(list_buffer))
                    list_buffer = []
                elif s1 in ["+", "-"]:
                    if list_buffer:
                        if str_to_append:
                            if (str_to_append[0] in ["+", "-"] and 
                                list_strs and list_strs[-1] in ["+", "-"]):
                                list_strs[-1] = str_to_append
                            else:
                                list_strs.append(str_to_append)
                        list_strs.append("".join(list_buffer))
                        list_strs.append(s1)
                        list_buffer = []
                else:
                    list_buffer.append(s1)

            if list_buffer:
                if str_to_append:
                    if (str_to_append[0] in ["+", "-"] and 
                        list_strs and list_strs[-1] in ["+", "-"]):
                        list_strs[-1] = str_to_append
                    else:
                        list_strs.append(str_to_append)
                list_strs.append("".join(list_buffer))

            if list_strs:
                list_strings.append("".join(list_strs))
        else:
            list_strings.append(text)

        return list_strings

    @staticmethod
    def parse_arithmetic_series(text: str) -> List[str]:
        """Parse arithmetic series from text."""
        list_strings: List[str] = []
        
        if not text:
            return list_strings
            
        arr: List[str] = text.split("...")

        if len(arr) == 2:
            s0: str = arr[0].strip()
            s1: str = arr[1].strip()

            if s0 and s1:
                list_strs = Polynomial.parse_polynomial_with_round_brackets(s0)
                list_strings.extend(list_strs)

                list_strs = Polynomial.parse_polynomial_with_round_brackets(s1)
                list_strings.extend(list_strs)

        return list_strings

    @staticmethod
    def compute_arithmetic_series(s0: str, s1: str, list_const_coeffs: List[str] = []) -> Optional['Polynomial']:
        """Compute arithmetic series from two strings."""
        p0: Optional[Polynomial] = Polynomial.parse_single(s0, list_const_coeffs)
        p1: Optional[Polynomial] = Polynomial.parse_single(s1, list_const_coeffs)
        
        if p0 is None or p1 is None:
            return None
            
        return p1 + p0

    @staticmethod
    def parse_curly(text: str, list_const_coeffs: List[str] = []) -> Optional['Polynomial']:
        """Parse polynomial with curly brackets."""
        if not text:
            return None
            
        text = text.replace("{", "|").replace("}", "|")
        list_strings: List[str] = [s for s in text.split("|") if s]

        if len(list_strings) == 3 and list_strings[1] in ["+", "-"]:
            str0 = list_strings[0]
            str2 = list_strings[2]

            if "..." in str2:
                index_left = str2.find("(")
                index_right = str2.find(")")

                if 0 < index_left < index_right:
                    pref = str2[0:index_left]
                    mon_pref = Monomial.parse(pref, list_const_coeffs=list_const_coeffs)
                    
                    if mon_pref is None:
                        return None
                        
                    pol_pref = Polynomial([mon_pref])
                    in_round_brackets = str2[index_left + 1:index_right]
                    list0: List[str] = in_round_brackets.split("...")

                    if len(list0) == 2:
                        s0, s1 = list0[0], list0[1]
                        p0 = Polynomial.parse_single(s0, list_const_coeffs=list_const_coeffs)
                        p1 = Polynomial.parse_single(s1, list_const_coeffs=list_const_coeffs)
                        
                        if p0 is None or p1 is None:
                            return None

                        p0_1 = p0 - Polynomial([Monomial(elems={}, coeff=Rational(1))])
                        p1_1 = p1 - Polynomial([Monomial(elems={}, coeff=Rational(1))])
                        p0 *= p0_1
                        p1 *= p1_1
                        pol2 = p1 - p0
                        half = Polynomial([Monomial(elems={}, coeff=Rational(1, 2))])
                        pol2 *= half
                        pol2 *= pol_pref

                        index_left = str0.find("(")
                        index_right = str0.find(")")

                        if 0 < index_left < index_right:
                            pref = str0[0:index_left]
                            mon_pref = Monomial.parse(pref, list_const_coeffs=list_const_coeffs)
                            
                            if mon_pref is None:
                                return None
                                
                            pol_pref = Polynomial([mon_pref])
                            in_round_brackets = str0[index_left + 1:index_right]
                            pol0 = Polynomial.parse_single(in_round_brackets, list_const_coeffs=list_const_coeffs)
                            
                            if pol0 is None:
                                return None
                                
                            pol0 *= pol_pref
                            return pol0 + pol2
        return None

    @staticmethod
    def parse_round_brackets(text: str, list_const_coeffs: List[str]) -> Optional['Polynomial']:
        """Parse polynomial with round brackets."""
        if not text:
            return None
            
        index_left = text.find("(")
        index_right = text.find(")")

        if 0 < index_left < index_right:
            pref = text[0:index_left]
            mon_pref = Monomial.parse(pref, list_const_coeffs=list_const_coeffs)
            
            if mon_pref is None:
                return None
                
            pol_pref = Polynomial([mon_pref])
            in_round_brackets = text[index_left + 1:index_right]
            pol = Polynomial.parse_single(in_round_brackets, list_const_coeffs=list_const_coeffs)
            
            if pol is None:
                return None
                
            pol *= pol_pref
            return pol
        return None

    @staticmethod
    def parse_brackets(text: str, list_const_coeffs: List[str]) -> Optional['Polynomial']:
        """Parse polynomial with square brackets."""
        if not text:
            return None
            
        text = text.replace("[", "|").replace("]", "|")
        list_strings: List[str] = [s for s in text.split("|") if s.strip()]
        list_polynomials: List[Polynomial] = []

        for text_part in list_strings:
            text_part = text_part.strip()
            if not text_part:
                continue
                
            list_polynoms: List[Polynomial] = []
            buffer: List[str] = []
            count_round = 0
            next_minus: bool = False

            for ch in text_part:
                if ch == "(":
                    count_round += 1
                    buffer.append(ch)
                elif ch == ")":
                    count_round -= 1
                    buffer.append(ch)
                elif ch in ["+", "-"] and count_round < 1:
                    if buffer:
                        str0 = "".join(buffer)
                        buffer = []
                        
                        pol0 = (Polynomial.parse_round_brackets(str0, list_const_coeffs=list_const_coeffs) 
                               if "(" in str0 else 
                               Polynomial.parse_single(str0, list_const_coeffs=list_const_coeffs))

                        if pol0 is not None:
                            if next_minus:
                                pol0 *= Polynomial([Monomial(coeff=Rational(-1))])
                                next_minus = False
                            list_polynoms.append(pol0)

                    if ch == "-":
                        next_minus = True
                else:
                    buffer.append(ch)

            if buffer:
                str0 = "".join(buffer)
                pol0 = (Polynomial.parse_round_brackets(str0, list_const_coeffs=list_const_coeffs) 
                       if "(" in str0 else 
                       Polynomial.parse_single(str0, list_const_coeffs=list_const_coeffs))

                if pol0 is not None:
                    if next_minus:
                        pol0 *= Polynomial([Monomial(coeff=Rational(-1))])
                    list_polynoms.append(pol0)

            if list_polynoms:
                pol = Polynomial([Monomial(coeff=Rational(0))])
                for p in list_polynoms:
                    pol += p
                list_polynomials.append(pol)

        if not list_polynomials:
            return None
            
        polynomial = Polynomial([Monomial(coeff=Rational(1))])
        for pol in list_polynomials:
            polynomial *= pol
        return polynomial

    @staticmethod
    def parse(text: str, list_const_coeffs: List[str]) -> List['Polynomial']:
        """Parse multiple polynomials from text."""
        list_list_monomials: List[Tuple[List[Monomial], str]] = Polynomial.parse_monomials(text, list_const_coeffs)
        list_polynomials: List[Polynomial] = []

        for monomials, name in list_list_monomials:
            polynomial: Polynomial = Polynomial(monoms=monomials, nm=name)
            list_polynomials.append(polynomial)

        return list_polynomials

    @staticmethod
    def parse_single(text: str, list_const_coeffs: List[str]) -> Optional['Polynomial']:
        """Parse a single polynomial from text."""
        polynomials: List[Polynomial] = Polynomial.parse(text, list_const_coeffs)
        if len(polynomials) == 1:
            return polynomials[0]
        return None

    # def __eq__(self, other):
    #   return

    def __add__(self, other: 'Polynomial') -> 'Polynomial':
        """Add two polynomials."""
        if not isinstance(other, Polynomial):
            return NotImplemented
            
        polynomial: Polynomial = Polynomial(self.monomials)
        for monom in other.monomials:
            polynomial.add_monomial(monom)
        return polynomial

    def __sub__(self, other: 'Polynomial') -> 'Polynomial':
        """Subtract two polynomials."""
        if not isinstance(other, Polynomial):
            return NotImplemented
            
        other0 = copy.deepcopy(other)
        other0 *= Polynomial([Monomial(elems={}, coeff=Rational(-1))])
        return self + other0

    def __str__(self) -> str:
        """String representation of the polynomial."""
        return self.get_ltx_str()

    def get_str(self) -> str:
        """Get string representation of the polynomial."""
        s: str = ""
        if self.name:
            s = f"{self.name} = "

        s0: str = " + ".join(f"{monom}" for monom in self.monomials)
        s0 = f"({s0})"

        if self.power != Rational(1):
            s0 = f"{s0}^{Fore.LIGHTYELLOW_EX}{self.power}{Style.RESET_ALL}"

        s = f"{s}{s0}"
        return s

    def get_ltx_str(self) -> str:
        """Get LaTeX string representation of the polynomial."""
        str_polynomial: str = ""
        monoms: List[Monomial] = [monom for monom in self.monomials if monom.coefficient != Rational(0)]

        for index, monom in enumerate(monoms):
            print_sign = Monomial.Print_Sign_Anyway if index > 0 else Monomial.Print_Sign_If_Minus
            str_monomial: str = monom.get_ltx_str(print_sign=print_sign)
            str_polynomial = f"{str_polynomial}{str_monomial}"

        if self.in_polynomial_product or self.power != Rational(1):
            str_polynomial = f"({str_polynomial})"

        if self.power != Rational(1):
            color = "red"
            str_polynomial = f"{str_polynomial}^{{\\textcolor{{{color}}}{{{self.power}}}}}"

        return str_polynomial


class PolynomialProduct:
    def __init__(self, polynoms: Optional[List[Polynomial]] = None, 
                 coeff: Rational = Rational(1),
                 const_coeffs: Optional[Dict[str, Element]] = None, 
                 minus: bool = False):
        """Initialize a polynomial product."""
        self.is_minus: bool = minus
        self.list_polynomials: List[Polynomial] = polynoms if polynoms is not None else []
        self.coefficient: Rational = coeff
        self.const_coefficients: Dict[str, Element] = copy.deepcopy(const_coeffs) if const_coeffs else {}

    def __iter__(self):
        """Iterate over polynomials in the product."""
        for polynomial in self.list_polynomials:
            yield polynomial

    def mul_polynomial(self, input_polynomial: Polynomial) -> None:
        """Multiply by a polynomial."""
        if not isinstance(input_polynomial, Polynomial):
            return
            
        input_polynomial = copy.deepcopy(input_polynomial)
        flag: bool = False

        for polynom in self.list_polynomials:
            if polynom.base_equals(input_polynomial):
                polynom.power += input_polynomial.power
                flag = True
                break

        if not flag:
            self.list_polynomials.append(input_polynomial)

    def __str__(self) -> str:
        """String representation of the polynomial product."""
        return self.get_ltx_str()

    def get_ltx_str(self) -> str:
        """Get LaTeX string representation of the polynomial product."""
        list_polynoms: List[Polynomial] = [p for p in self.list_polynomials if not p.is_one()]

        if len(list_polynoms) < 1:
            list_polynoms = self.list_polynomials[0:1]

        str_output: str = "".join(f"{polynom}" for polynom in list_polynoms)

        if self.const_coefficients:
            for const_coefficient in self.const_coefficients.values():
                str_output = f"{const_coefficient.get_ltx_str(with_parentheses=Element.WithParenthesesByLength)}{str_output}"

        if self.coefficient != Rational(1):
            str_output = f"{self.coefficient}{str_output}"

        return str_output

    @property
    def get_str(self) -> str:
        """Get string representation of the polynomial product."""
        list_polynoms: List[Polynomial] = [p for p in self.list_polynomials if not p.is_one()]

        if len(list_polynoms) < 1:
            list_polynoms = self.list_polynomials[0:1]

        s: str = "*".join(f"{polynom}" for polynom in list_polynoms)

        if self.const_coefficients:
            s0: str = "*".join([f"({const_coeff})" for const_coeff in self.const_coefficients.values()])
            s = f"{Fore.RED}{s0}{Style.RESET_ALL}*{s}"

        if self.coefficient != Rational(1):
            s = f"{Fore.LIGHTMAGENTA_EX}{self.coefficient}{Style.RESET_ALL}*{s}"

        return s
