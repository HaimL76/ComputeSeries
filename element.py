class Element:
    def __init__(self, symb: str = "", pow: int = 1, ind = None):
        self.power: int = pow
        self.symbol: str = symb
        self.index: int = ind

        if self.symbol == "x_0":
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

        l1: list[str] = symb.split("_")

        if len(l1) == 2:
            if l1[0] == "x" and l1[1].isnumeric():
                symb = "x"
                index = int(l1[1])

        return Element(symb, pow, ind=index)

    def get_str(self):
        s: str = self.symbol

        if self.power != 1:
            s = f"{s}^{self.power}"

        return s

    def get_copy_with_parentheses(self):
        return Element(symb=f"({self.symbol})", pow=self.power)

    def get_ltx_str(self):
        s: str = self.symbol

        if self.index is not None:
            s = f"{s}_{{{self.index}}}"

        if self.power != 1:
            s = f"{s}^{{{self.power}}}"

        return s

    def __str__(self):
        return self.get_ltx_str()
