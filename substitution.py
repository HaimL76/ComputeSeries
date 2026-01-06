import sympy
from fontTools.ttLib.tables.otTables import DeltaSetIndexMap
from sympy import symbols

from element import Element
from exponential import Exponential, ExponentialProduct
from monomial import Monomial
from polynomial import Polynomial
from rational import Rational


class VariableSubstitution:
    def __init__(self):
        self.substitution: dict = {}

    def add_mapping(self, symb: str, polynom: Polynomial):
        self.substitution[symb] = polynom

    @staticmethod
    def parse(text: str, list_const_coeffs: list[str], substitution):
        if substitution is None:
            substitution: VariableSubstitution = VariableSubstitution()

        list_polynomials: list = Polynomial.parse(text, list_const_coeffs=list_const_coeffs)

        if isinstance(list_polynomials, list) and len(list_polynomials) > 0:
            for polynomial in list_polynomials:
                name: str = polynomial.name

                if name:
                    substitution.add_mapping(symb=name, polynom=polynomial)

        return substitution

    def subs_monomial(self, original_monomial: Monomial):
        str_monomial: str = original_monomial.get_sage_str()

        monom = sympy.parsing.parse_expr(str_monomial)

        subs_v1 = sympy.parsing.parse_expr(self.substitution["v_1"].get_sage_str())
        subs_v2 = sympy.parsing.parse_expr(self.substitution["v_2"].get_sage_str())
        subs_v3 = sympy.parsing.parse_expr(self.substitution["v_3"].get_sage_str())
        subs_v4 = sympy.parsing.parse_expr(self.substitution["v_4"].get_sage_str())

        v1, v2, v3, v4, a, b, c, d = symbols('v1 v2 v3 v4 a b c d')

        converted_monom = monom.subs(v1, subs_v1).subs(v2, subs_v2).subs(v3, subs_v3).subs(v4, subs_v4)

        return converted_monom

    def substitute_monomial(self, original_monomial: Monomial):
        is_minus: bool = original_monomial.is_minus

        elems: dict = original_monomial.elements

        if not isinstance(elems, dict) or len(elems) < 1:
            return [original_monomial]

        coeffs_monomial: Monomial = Monomial(coeff=original_monomial.coefficient,
                                    const_coeffs=original_monomial.const_coefficients)

        l: list = [coeffs_monomial]

        for key in elems.keys():
            elem: Element = elems[key]

            if key in self.substitution:
                val: Polynomial = self.substitution[key]

                power: int = elem.power

                if power > 1:
                    power0: int = power - 1

                    for i in range(power0):
                        val *= val

                l0: list = []

                for monom in val.monomials:
                    for mon in l:
                        monomial: Monomial = mon * monom

                        if isinstance(monomial, Monomial):
                            monomial.is_minus = is_minus
                            l0.append(monomial)

                l = l0

        return l


    def substitude_polynomial(self, original_polynom: Polynomial):
        sympy_polynomial = 0

        list_tuples: list[tuple] = []

        #result_polynomial: Polynomial = Polynomial()

        str_sage_polynomial: str = original_polynom.get_sage_str()
        
        # Use sympy to parse the sage polynomial string
        parsed_sympy_polynomial = sympy.sympify(str_sage_polynomial)

        list_monomials_total: list[Monomial] = []

        for monomial in original_polynom:
            str_monomial: str = monomial.get_sage_str(print_sign=Monomial.Print_Sign_Anyway)

            list_monomials: list[str] = []

            monomials: list = self.substitute_monomial(monomial)

            #######sympy_converted_monom = self.subs_monomial(monomial)

            #######sympy_polynomial += sympy_converted_monom

            #######result = sympy.expand(sympy_converted_monom)

            if isinstance(monomials, list) and len(monomials) > 0:
                for monom in monomials:
                    str_monomials: str = monom.get_sage_str(print_sign=Monomial.Print_Sign_Anyway)

                    list_monomials.append(str_monomials)
                    list_monomials_total.append(monom)

                    #result_polynomial.add_monomial(monom)

            tup: tuple = str_monomial, list_monomials

            list_tuples.append(tup)

        list0: list[str] = []

        for tup in list_tuples:
            str0: str = "".join(tup[1])

            list0.append(f"{tup[0]}->{str0}")

        str1: str = "\n".join(list0)

        list_monomials_total = [monom for monom in list_monomials_total if monom.coefficient != Rational(0)]

        result_polynomial: Polynomial = Polynomial()

        for monom in list_monomials_total:
            result_polynomial.add_monomial(monom)

        return result_polynomial, list_tuples, sympy_polynomial

    def substitude_exponential(self, original_exponential: Exponential):
        polynomial: Polynomial = original_exponential.exponent

        tup: tuple = self.substitude_polynomial(polynomial)

        polynomial = tup[0]

        return Exponential(symb=original_exponential.symbol, exp=polynomial)

    def substitude_exponential_product(self, original_exponential_product: ExponentialProduct):
        exponential_product: ExponentialProduct = ExponentialProduct()

        for key in original_exponential_product.exponentials.keys():
            exponential: Exponential = original_exponential_product.exponentials[key]

            if isinstance(exponential, Exponential):
                exp: Exponential = self.substitude_exponential(exponential)

                if isinstance(exp, Exponential):
                    exponential_product.add_exponential(exp)

        return exponential_product

    def __str__(self):
        return self.get_str()

    def get_ltx_str(self):
        return self.get_str(is_latex=True)

    def get_sage_str(self):
        return self.get_str(is_latex=False)

    def get_str(self, is_latex: bool = True):
        str_substitution: str = ""

        if is_latex:
            str_substitution = "".join(f"\\[{key}\\rightarrow{{{self.substitution[key].get_str(is_latex=is_latex)}}}\\]" for key in self.substitution)
        else:
            str_substitution = ",".join(f"{key.replace("_", "")}={self.substitution[key].get_str(is_latex=is_latex)}" for key in self.substitution)

        return str_substitution