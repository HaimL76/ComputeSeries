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

            ##result.sign = self.sign != other.sign

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

    def get_str(self):
        s: str = self.symbol

        if self.power != 1:
            s = f"{s}^{self.power}"

        return s

    def get_ltx_str(self):
        s: str = self.symbol

        if self.power != 1:
            s = f"({s})^{{{self.power}}}"

        return s

    def __str__(self):
        return self.get_ltx_str()
