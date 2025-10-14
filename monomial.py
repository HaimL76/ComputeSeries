import copy
from typing import Dict, List, Optional, Union

from element import Element
from rational import Rational


class Monomial:
    def __init__(self, elems: Union[Dict[str, Element], List[Element], None] = None, 
                 coeff: Rational = Rational(1),
                 const_coeffs: Optional[Dict[str, Element]] = None, 
                 minus: bool = False):
        """Initialize a monomial with elements, coefficient, and optional constant coefficients."""
        self.is_minus: bool = minus
        self.elements: Dict[str, Element] = {}

        if elems is None:
            elems = {}
        elif isinstance(elems, dict):
            self.elements = copy.deepcopy(elems)
        elif isinstance(elems, list):
            for elem in elems:
                if elem is None:
                    continue
                key: str = elem.symbol
                if elem.index is not None:
                    key += f"_{elem.index}"

                if key not in self.elements:
                    self.elements[key] = Element(symb=elem.symbol, pow=elem.power, ind=elem.index)
                else:
                    existing = self.elements[key]
                    multiplied = existing * elem
                    if multiplied is not None:
                        self.elements[key] = multiplied

        self.coefficient: Rational = abs(coeff)
        if coeff.is_minus():
            self.is_minus = not self.is_minus

        self.const_coefficients: Dict[str, Element] = copy.deepcopy(const_coeffs) if const_coeffs else {}

    @staticmethod
    def are_same_monomials(monom1: 'Monomial', monom2: 'Monomial') -> bool:
        """Check if two monomials have the same structure (elements and constant coefficients)."""
        if not isinstance(monom1, Monomial) or not isinstance(monom2, Monomial):
            return False

        # Check constant coefficients
        const_coeff1 = next(iter(monom1.const_coefficients.values())) if monom1.const_coefficients else None
        const_coeff2 = next(iter(monom2.const_coefficients.values())) if monom2.const_coefficients else None

        # If one has constant coefficients and the other doesn't, they're different
        if (const_coeff1 is None) != (const_coeff2 is None):
            return False

        # If both have constant coefficients, check if they're the same
        if const_coeff1 is not None and const_coeff2 is not None:
            if (const_coeff1.symbol != const_coeff2.symbol or 
                const_coeff1.power != const_coeff2.power):
                return False

        # Check elements
        if len(monom1.elements) != len(monom2.elements):
            return False

        for symb in monom1.elements:
            if symb not in monom2.elements:
                return False
            if monom1.elements[symb] != monom2.elements[symb]:
                return False

        return True

    def __eq__(self, other: object) -> bool:
        """Check equality of two monomials."""
        if not isinstance(other, Monomial):
            return NotImplemented
        
        return (self.coefficient == other.coefficient and
                self.is_minus == other.is_minus and
                self.elements == other.elements and
                self.const_coefficients == other.const_coefficients)

    def __iter__(self):
        """Iterate over element keys."""
        for symb in self.elements.keys():
            yield symb

    def __mul__(self, other: 'Monomial') -> 'Monomial':
        """Multiply two monomials."""
        if not isinstance(other, Monomial):
            return NotImplemented

        const_coeffs: Dict[str, Element] = copy.deepcopy(self.const_coefficients)

        # Handle constant coefficients from other monomial
        if other.const_coefficients:
            for key, val_other in other.const_coefficients.items():
                if key not in const_coeffs:
                    const_coeffs[key] = Element(symb=key, pow=0)

                val: Element = const_coeffs[key]
                const_coeffs[key] = Element(val.symbol, val.power + val_other.power)

        coeff: Rational = self.coefficient * other.coefficient
        elems: Dict[str, Element] = {}

        # Copy elements from self
        for symb, val in self.elements.items():
            elems[symb] = val

        # Multiply with elements from other
        for symb, val in other.elements.items():
            if symb not in elems:
                elems[symb] = val
            else:
                multiplied = elems[symb] * val
                if multiplied is not None:
                    elems[symb] = multiplied

        is_minus: bool = self.is_minus != other.is_minus
        return Monomial(elems, coeff=coeff, const_coeffs=const_coeffs, minus=is_minus)

    @staticmethod
    def parse(text: str, list_const_coeffs: List[str]) -> Optional['Monomial']:
        """Parse a string representation of a monomial."""
        if not text or not text.strip():
            return None
            
        text = text.strip()
        
        # Handle special case for p^{...}t^{...} format
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
            found = False
            while not found and i < len(text):
                ch = text[i]
                i += 1
                str1 += ch
                if ch == "}":
                    found = True

            if str0 and str1:
                elem0: Optional[Element] = Element.parse(str0)
                elem1: Optional[Element] = Element.parse(str1)
                if elem0 is not None and elem1 is not None:
                    return Monomial(elems={elem0.symbol: elem0, elem1.symbol: elem1}, 
                                   coeff=Rational(1), const_coeffs={})

        coeff: Rational = Rational(1)
        const_coeffs: Dict[str, Element] = {}
        elements: List[Element] = []

        parts: List[str] = text.split(".")

        for s in parts:
            s = s.strip()
            if not s:
                continue
                
            found = False

            # Handle constant coefficients with powers
            if "^" in s:
                power_parts = s.split("^")
                if len(power_parts) == 2:
                    base = power_parts[0]
                    power_str = power_parts[1]
                    
                    if base in list_const_coeffs and power_str.isnumeric():
                        if base not in const_coeffs:
                            const_coeffs[base] = Element(symb=base, pow=0)
                        val: Element = const_coeffs[base]
                        const_coeffs[base] = Element(val.symbol, val.power + int(power_str))
                        found = True

            if not found:
                # Handle rational coefficients
                if "/" in s:
                    frac_parts = s.split("/")
                    if len(frac_parts) == 2 and frac_parts[0].isnumeric() and frac_parts[1].isnumeric():
                        coeff = Rational(int(frac_parts[0]), int(frac_parts[1]))
                        found = True
                elif s.isnumeric():
                    coeff = Rational.parse(s)
                    found = True
                elif s in list_const_coeffs:
                    if s not in const_coeffs:
                        const_coeffs[s] = Element(symb=s, pow=0)
                    val: Element = const_coeffs[s]
                    const_coeffs[s] = Element(val.symbol, val.power + 1)
                    found = True
                else:
                    element: Optional[Element] = Element.parse(s)
                    if element is not None:
                        elements.append(element)
                        found = True

        return Monomial(elements, coeff=coeff, const_coeffs=const_coeffs)

    def is_one(self) -> bool:
        """Check if the monomial is equal to 1."""
        return (len(self.elements) == 0 and 
                len(self.const_coefficients) == 0 and 
                self.coefficient == Rational(1) and 
                not self.is_minus)

    def remove_element(self, symb: str) -> None:
        """Remove an element from the monomial."""
        if symb in self.elements:
            self.elements.pop(symb)

    def __str__(self) -> str:
        """String representation of the monomial."""
        return self.get_ltx_str()

    Disable_Print_Sign = 0
    Print_Sign_If_Minus = 1
    Print_Sign_Anyway = 2

    def get_ltx_str(self, print_sign: int = Disable_Print_Sign) -> str:
        """Get LaTeX string representation of the monomial."""
        str_output: str = ""
        counter: int = 0

        # Add coefficient if not 1 or if no elements/const_coeffs
        if self.coefficient != Rational(1) or (len(self.elements) == 0 and len(self.const_coefficients) == 0):
            str_output = f"{self.coefficient}"
            counter += 1

        # Add constant coefficients
        if self.const_coefficients:
            for const_coeff in self.const_coefficients.values():
                str_const_coefficient = const_coeff.symbol
                if len(const_coeff.symbol) > 1:
                    str_const_coefficient = f"({str_const_coefficient})"
                str_output = f"{str_output}{str_const_coefficient}"
                if const_coeff.power != 1:
                    str_output = f"{str_output}^{const_coeff.power}"
                counter += 1

        # Add elements
        if self.elements:
            s0: str = "".join(f"{elem}" for elem in self.elements.values())
            if s0:
                str_output = f"{str_output}{s0}"
                counter += 1

        # Add sign if needed
        if print_sign != Monomial.Disable_Print_Sign:
            if print_sign == Monomial.Print_Sign_Anyway or self.is_minus:
                sign = "-" if self.is_minus else "+"
                str_output = f"{sign}{str_output}"

        return str_output

    def get_str(self) -> str:
        """Get string representation of the monomial."""
        s: str = ""
        counter: int = 0

        # Add coefficient if not 1 or if no elements/const_coeffs
        if self.coefficient != Rational(1) or (len(self.elements) == 0 and len(self.const_coefficients) == 0):
            s = f"{self.coefficient}"
            counter += 1

        # Add constant coefficients
        if self.const_coefficients:
            for const_coeff in self.const_coefficients.values():
                if counter > 0:
                    s = f"{s}*"
                s = f"{s}({const_coeff.symbol})"
                if const_coeff.power != 1:
                    s = f"{s}^{const_coeff.power}"
                counter += 1

        # Add elements
        if self.elements:
            s0: str = "*".join(f"{elem}" for elem in self.elements.values())
            if s0:
                if s:
                    s = f"{s}*"
                s = f"{s}{s0}"
                counter += 1

        return s
