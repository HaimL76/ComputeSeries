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
        result_polynomial: Polynomial = Polynomial()

        for monomial in original_polynom:
            monomials: list = self.substitute_monomial(monomial)

            if isinstance(monomials, list) and len(monomials) > 0:
                for monom in monomials:
                    result_polynomial.add_monomial(monom)

        return result_polynomial

    def substitude_exponential(self, original_exponential: Exponential):
        polynomial: Polynomial = original_exponential.exponent

        polynomial = self.substitude_polynomial(polynomial)

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
        return self.get_ltx_str()

    def get_ltx_str(self):
        return "".join(f"\\[{key}\\rightarrow{{{self.substitution[key]}}}\\]" for key in self.substitution)
    def get_str(self):
        return "\n".join(f"{key}->{self.substitution[key]}" for key in self.substitution)