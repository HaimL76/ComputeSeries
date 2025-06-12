from exponential import Exponential, ExponentialExpression
from polynomial import Polynomial
from series import SeriesProduct, SeriesProductSum
from substitution import VariableSubstitution

const_coefficient: str = "(1-p^{-1})"
coeff: str = const_coefficient

def main():
    p1 = Polynomial.parse_single(f"1+{coeff}.v2")
    p2 = Polynomial.parse_single(f"1+{coeff}.v3")
    substitution: VariableSubstitution = VariableSubstitution.parse("v1=2.a+b+c+d,v2=a,v3=a+b+c,v4=a+b")

    print(f"p1 = {p1}")
    print(f"p2 = {p2}")
    print(f"substitution: {substitution}")

    return

    print(f"v1 = {v1}")

    substitution: VariableSubstitution = VariableSubstitution()

    substitution.add_mapping(symb="v1", polynom=v1)

    a = substitution.substitude_polynomial(p1)

    p: Polynomial = p1 * p2

    exp1: Exponential = Exponential.parse("p^2.a+3.b")
    exp2: Exponential = Exponential.parse("p^5.a+3.c")

    exp3: Exponential = Exponential.parse("t^67.a+3.b")
    exp4: Exponential = Exponential.parse("t^5.a+13.c")

    print(f"exp1={exp1}")
    print(f"exp2={exp2}")

    exp12: Exponential = exp1 * exp2

    print(f"exp12={exp12}")

    print(f"exp3={exp3}")
    print(f"exp4={exp4}")

    exp34: Exponential = exp3 * exp4

    print(f"exp12={exp12}")
    print(f"exp34={exp34}")

    expression1: ExponentialExpression = ExponentialExpression(exps=[exp1, exp2, exp3, exp4])
    expression2: ExponentialExpression = ExponentialExpression(exps=[exp12, exp34])

    list_series = expression2.break_by_exponent()

    series_product: SeriesProduct = SeriesProduct(list_series)

    p0: Polynomial = Polynomial.parse("23.a^56+12.b")

    series_product.multiply_by_polynomial(p0)

    print(f"p0 = {p0}")

    print(f"series_product = {series_product}")

    ser_prod_sum: SeriesProductSum = SeriesProductSum.multiply_series_product_by_polynomial(series_product, p0)

    print(f"ser_prod_sum = {ser_prod_sum}")

    print(f"expression1 = {expression1}")
    print(f"expression2 = {expression2}")

    print(f"p = {p}")
    print(f"a = {a}")

main()