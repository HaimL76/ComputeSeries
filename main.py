from exponential import Exponential, ExponentialProduct
from polynomial import Polynomial
from polynomial_rational import PolynomialProductRational, PolynomialSummationRational
from series import SeriesProduct, SeriesProductSum
from substitution import VariableSubstitution

import matplotlib.pyplot as plt

const_coefficient: str = "(1-p^{-1})"
coeff: str = const_coefficient

def main():
    process_line("[1+(1-p^{-1}).v_2][1+(1-p^{-1}).v_3];v_1=2.a+b+c+d,v_2=a,v_3=a+b+c,v_4=a+b;a>=0,b>=0,c>=0,"
                 "d>=1;p^{7.v_1+10.v_2+10.v_3+7.v_4}*t^{"
                 "4.v_1+6.v_2+6.v_3+4.v_4}")

def process_line(text: str):
    strs: list[str] = text.split(";")

    p: Polynomial = Polynomial.parse_brackets(strs[0])

    print(f"p = {p}")

    substitution: VariableSubstitution = VariableSubstitution.parse(strs[1])

    p0: Polynomial = substitution.substitude_polynomial(p)

    print(f"p0 = {p0}")
    print(f"substitution: {substitution}")

    exp_prod: ExponentialProduct = ExponentialProduct.parse(strs[3])
    exp_prod0: ExponentialProduct = substitution.substitude_exponential_product(exp_prod)

    print(f"exp_prod = {exp_prod}")
    print(f"exp_prod0 = {exp_prod0}")

    series_product = SeriesProduct.from_exponential_product(exp_prod0)

    series_product.parse_starting_indices(strs[2])

    l: list = series_product.multiply_by_polynomial(p0)

    counter: int = 0

    total_sum: PolynomialSummationRational = PolynomialSummationRational()

    debug_counter: int = 3

    for ser_prod in l:
        #if debug_counter <= 0:
         #   continue

        #debug_counter -= 1

        print(f"[{counter}] ser_prod: {ser_prod}")

        sum_product: PolynomialProductRational = ser_prod.sum()

        total_sum.add_polynomial_rational(sum_product)

        print(f"[{counter}] sum: {sum_product}")

        counter += 1

    output: str = f"\\[{p}\\]"
    output = f"{output}{substitution}"
    output = f"{output}\\[{p0}\\]"
    s0: str = "+".join([f"\\[{ser_prod}\\]" for ser_prod in l])
    output = f"{output}{s0}"
    output = f"{output}{total_sum}"

    with open(r"c:\gpp\1.tex", "w") as fw:
        fw.write(r"""
        \documentclass{article}
        \usepackage{graphicx} % Required for inserting images
        \begin{document}
        """)
        fw.write(output)
        fw.write("""\end{document}""")
main()