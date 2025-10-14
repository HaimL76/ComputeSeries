from typing import List, Dict, Optional

from element import Element
from polynomial import Polynomial


class Exponential:
    def __init__(self, symb: str, exp: Polynomial):
        """Initialize an exponential with symbol and exponent."""
        self.symbol: str = symb
        self.exponent: Polynomial = exp

    def __mul__(self, other: 'Exponential') -> 'Exponential':
        """Multiply two exponentials with the same symbol."""
        if not isinstance(other, Exponential):
            return NotImplemented
        if self.symbol != other.symbol:
            raise ValueError("Cannot multiply exponentials with different symbols")
        return Exponential(symb=self.symbol, exp=self.exponent + other.exponent)

    def __str__(self) -> str:
        """String representation of the exponential."""
        return self.get_ltx_str()

    def get_str(self) -> str:
        """Get string representation."""
        return f"{self.symbol}^({self.exponent})"

    def get_ltx_str(self) -> str:
        """Get LaTeX string representation."""
        return f"{self.symbol}^{{{self.exponent}}}"

    @staticmethod
    def parse(text: str, list_const_coeffs: List[str]) -> Optional['Exponential']:
        """Parse an exponential from text."""
        if not text or not text.strip():
            return None
            
        text = text.strip()
        parts: List[str] = text.split("^")

        if len(parts) == 2:
            symbol: str = parts[0].strip()
            str_exp: str = parts[1].strip()

            if len(str_exp) > 2 and str_exp[0] == "{" and str_exp[-1] == "}":
                str_exp = str_exp[1:-1]

            if str_exp and symbol:
                exponent: Optional[Polynomial] = Polynomial.parse_single(str_exp, list_const_coeffs=list_const_coeffs)
                if exponent is not None:
                    return Exponential(symb=symbol, exp=exponent)

        return None


class ExponentialProduct:
    def __init__(self, exps: Optional[List[Exponential]] = None):
        """Initialize an exponential product."""
        self.exponentials: Dict[str, Exponential] = {}

        if exps:
            for exp in exps:
                if isinstance(exp, Exponential) and exp.symbol:
                    self.add_exponential(exp)

    def add_exponential(self, exp: Exponential) -> None:
        """Add an exponential to the product."""
        if not isinstance(exp, Exponential) or not exp.symbol:
            return
            
        if exp.symbol not in self.exponentials:
            self.exponentials[exp.symbol] = exp
        else:
            self.exponentials[exp.symbol] *= exp

    def __iter__(self):
        """Iterate over exponential symbols."""
        for key in self.exponentials.keys():
            yield key

    @staticmethod
    def parse(text: str, list_const_coeffs: List[str]) -> 'ExponentialProduct':
        """Parse an exponential product from text."""
        exponential_product: ExponentialProduct = ExponentialProduct()

        if not text or not text.strip():
            return exponential_product

        parts: List[str] = text.split("*")

        for s in parts:
            s = s.strip()
            if s:
                exponential: Optional[Exponential] = Exponential.parse(s, list_const_coeffs=list_const_coeffs)
                if exponential is not None:
                    exponential_product.add_exponential(exponential)

        return exponential_product

    def __str__(self) -> str:
        """String representation of the exponential product."""
        return self.get_ltx_str()

    def get_str(self) -> str:
        """Get string representation."""
        return "*".join(f"{exp}" for exp in self.exponentials.values())

    def get_ltx_str(self) -> str:
        """Get LaTeX string representation."""
        return "".join(f"{exp}" for exp in self.exponentials.values())