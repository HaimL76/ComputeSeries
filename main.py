from exponential import Exponential, ExponentialExpression
from polynomial import Polynomial
from series import SeriesProduct
from substitution import VariableSubstitution


def main():
    p1 = Polynomial.parse("3.v1+v2")
    p2 = Polynomial.parse("1+v3")


    print(f"p1 = {p1}")
    print(f"p2 = {p2}")

    v1 = Polynomial.parse("2.a+b+c")

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

    print(f"series_product = {series_product}")

    for series in list_series:
        print(f"series = {series}, sum = {series.sum()}")

    print(f"expression1 = {expression1}")
    print(f"expression2 = {expression2}")

    print(f"p = {p}")
    print(f"a = {a}")

main()