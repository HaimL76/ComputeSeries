from typing import Optional, Dict, Tuple, List


class Element:
    reverse_conversion_table: Optional[Dict[int, Tuple[int, int]]] = None

    def __init__(self, symb: str = "", pow: int = 1, ind: Optional[int] = None):
        """Initialize an Element with symbol, power, and optional index."""
        self.power: int = pow
        self.symbol: str = symb
        self.index: Optional[int] = ind

    def __mul__(self, other: 'Element') -> Optional['Element']:
        """Multiply two elements if they have the same symbol and index."""
        if not isinstance(other, Element):
            return None
            
        equal_symbol: bool = self.symbol == other.symbol
        equal_index: bool = self.index == other.index

        if equal_symbol and equal_index:
            result = Element(symb=self.symbol, ind=self.index)
            result.power = self.power + other.power
            return result

        return None

    def __eq__(self, other: object) -> bool:
        """Check equality of two elements."""
        if not isinstance(other, Element):
            return NotImplemented
        return self.symbol == other.symbol and self.power == other.power

    @staticmethod
    def parse(text: str) -> Optional['Element']:
        """Parse a string representation of an element."""
        if not text or not text.strip():
            return None
            
        text = text.strip()
        index: Optional[int] = None
        
        # Split by power symbol
        parts: List[str] = text.split("^")
        symb: str = text
        pow: int = 1

        if len(parts) == 2:
            symb = parts[0].strip()
            spow = parts[1].strip()

            if spow.isnumeric():
                pow = int(spow)
            elif len(spow) > 2 and spow[0] == "{" and spow[-1] == "}":
                spow0: str = spow[1:-1]
                if spow0.isnumeric():
                    pow = int(spow0)

        # Check for index
        index_parts: List[str] = symb.split("_")
        if len(index_parts) == 2 and index_parts[0] == "x" and index_parts[1].isnumeric():
            symb = "x"
            index = int(index_parts[1])

        return Element(symb, pow, ind=index)

    def get_str(self) -> str:
        """Get string representation of the element."""
        s: str = self.symbol
        if self.power != 1:
            s = f"{s}^{self.power}"
        return s

    WithoutParentheses: int = 0
    WithParenthesesAnyway: int = 1
    WithParenthesesByLength: int = 2
    WithParenthesesByForPowerByLength: int = 3

    def get_ltx_str(self, with_parentheses: int = WithParenthesesByLength) -> str:
        """Get LaTeX string representation of the element."""
        converted: bool = False
        str_output: str = self.symbol

        if self.index is not None:
            s = f"{str_output}_{{{self.index}}}"

            if Element.reverse_conversion_table is not None:
                rkey = self.index
                if rkey in Element.reverse_conversion_table:
                    p, t = Element.reverse_conversion_table[rkey]
                    str_output = f"p^{{{p}}}t^{{{t}}}"
                    converted = True

        length_more_than_1: bool = len(self.symbol) > 1
        anyway: bool = with_parentheses == Element.WithParenthesesAnyway
        by_length: bool = with_parentheses == Element.WithParenthesesByLength and length_more_than_1
        for_power_by_length = (with_parentheses == Element.WithParenthesesByForPowerByLength and 
                              length_more_than_1 and self.power != 1)

        if anyway or by_length or for_power_by_length:
            str_output = f"\\left({str_output}\\right)"

        if self.power != 1:
            str_output = f"{str_output}^{{{self.power}}}"

        return str_output

    def __str__(self) -> str:
        """String representation of the element."""
        return self.get_ltx_str()
