class Element:
    reverse_conversion_table: dict = None

    def __init__(self, symb: str = "", pow: int = 1, ind = None):
        self.power: int = pow
        self.symbol: str = symb
        self.index: int = ind

        if self.symbol.startswith("p^"):
            _ = 0

        if self.symbol.startswith("x") and self.index is None:
            _ = 0

    def __mul__(self, other):
        result = None

        equal_symbol: bool = self.symbol == other.symbol

        #no_index: bool = self.index is None and other.index is None
        equal_index: bool = self.index == other.index

        if equal_symbol and equal_index:
            result = Element(symb=self.symbol, ind=self.index)

            result.power = self.power + other.power

            ##result.coefficient = self.coefficient * other.coefficient

            ##result.sign = self.sign != other.sign

        return result

    def __eq__(self, other):
        return self.symbol == other.symbol and self.power == other.power

    @staticmethod
    def parse(text: str):
        index = None
        l: list = []

        l0: list = text.split("^")

        symb: str = text
        pow: int = 1

        if len(l0) == 2:
            symb = l0[0].strip()

            spow = l0[1].strip()

            if spow.isnumeric():
                pow = int(spow)

            if spow[0] == "{" and spow[-1] == "}":
                spow0: str = spow[1:-1]

                if spow0.isnumeric():
                    pow = int(spow0)

        l1: list[str] = symb.split("_")

        if len(l1) == 2:
            if l1[0] == "x" and l1[1].isnumeric():
                symb = "x"
                index = int(l1[1])

        return Element(symb, pow, ind=index)

    WithoutParentheses: int = 0
    WithParenthesesAnyway: int = 1
    WithParenthesesByLength: int = 2
    WithParenthesesByForPowerByLength: int = 3

    def get_sage_str(self, with_parentheses: int = WithParenthesesByLength, remove_underscore: bool = False):
        return self.get_str(with_parentheses=with_parentheses, is_latex=False, remove_underscore=remove_underscore)

    def get_ltx_str(self, with_parentheses: int = WithParenthesesByLength):
        return self.get_str(with_parentheses=with_parentheses, is_latex=True)

    def get_str(self, with_parentheses: int = WithParenthesesByLength, is_latex: bool = True, remove_underscore: bool = False):
        converted: bool = False

        str_output: str = self.symbol

        if remove_underscore:
            str_output = str_output.replace("_", "")

        if self.index is not None:
            s = f"{str_output}_{{{self.index}}}"

            if Element.reverse_conversion_table is not None:
                #rkey: str = f"{self.symbol}_{self.index}"
                rkey = self.index

                if rkey in Element.reverse_conversion_table:
                    p,t = Element.reverse_conversion_table[rkey]

                    str_output = f"p^{{{p}}}t^{{{t}}}"
                    converted = True
                else:
                    _ = 0
            else:
                _ = 0

        length_more_than_1: bool = len(self.symbol) > 1

        anyway: bool = with_parentheses == Element.WithParenthesesAnyway

        by_length: bool = with_parentheses == Element.WithParenthesesByLength and length_more_than_1

        for_power_by_length = with_parentheses == Element.WithParenthesesByForPowerByLength and length_more_than_1 and self.power != 1

        if anyway or by_length or for_power_by_length:
            if is_latex:
                str_output = f"\\left({str_output}\\right)"

        if self.power != 1:
            str_output = f"{str_output}^{{{self.power}}}" if is_latex else f"{str_output}^{self.power}"

        return str_output

    def __str__(self):
        return self.get_ltx_str()
