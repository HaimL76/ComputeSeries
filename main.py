from exponential import Exponential, ExponentialProduct
from polynomial import Polynomial
from polynomial_rational import PolynomialProductRational
from series import SeriesProduct, SeriesProductSum
from substitution import VariableSubstitution

const_coefficient: str = "(1-p^{-1})"
coeff: str = const_coefficient

def main():
    p1: Polynomial = Polynomial.parse_single(f"1+{coeff}.v2")
    p2: Polynomial = Polynomial.parse_single(f"1+{coeff}.v3")

    print(f"p1 = {p1}")
    print(f"p2 = {p2}")

    p: Polynomial = p1 * p2

    print(f"p = {p}")

    substitution: VariableSubstitution = VariableSubstitution.parse("v1=2.a+b+c+d,v2=a,v3=a+b+c,v4=a+b")

    p0: Polynomial = substitution.substitude_polynomial(p)

    print(f"p0 = {p0}")
    print(f"substitution: {substitution}")

    exp_prod: ExponentialProduct = ExponentialProduct.parse("p^{7.v1+10.v2+10.v3+7.v4}*t^{4.v1+6.v2+6.v3+4.v4}")
    exp_prod0: ExponentialProduct = substitution.substitude_exponential_product(exp_prod)

    print(f"exp_prod = {exp_prod}")
    print(f"exp_prod0 = {exp_prod0}")

    series_product = SeriesProduct.from_exponential_product(exp_prod0)

    l: list = series_product.multiply_by_polynomial(p0)

    counter: int = 0

    #total_sum: MultiplePolynomialRational = MultiplePolynomialRational(numer=[], denom=[])

    for ser_prod in l:
        print(f"[{counter}] ser_prod: {ser_prod}")
        counter += 1

        sum0: PolynomialProductRational = ser_prod.sum()

        #total_sum.add_polynomial_rational(sum0)

        print(f"sum: {sum0}")

    #print(f"total sum: {total_sum}")

main()