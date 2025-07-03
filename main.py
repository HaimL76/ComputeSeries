import webbrowser

from debug_write import DebugWrite
from exponential import Exponential, ExponentialProduct
from polynomial import Polynomial
from polynomial_rational import PolynomialProductRational, PolynomialSummationRational
from series import SeriesProduct, SeriesProductSum
from substitution import VariableSubstitution

import matplotlib.pyplot as plt

const_coefficient: str = "(1-p^{-1})"
coeff: str = const_coefficient


def main():
    process_file("1.txt")


def process_file(file_path: str):
    with open(file_path, 'r') as file:
        with open("1.tex", "w") as fw:
            debug_write: DebugWrite = DebugWrite.get_instance(fw=fw)
            debug_write.write(r"""
            \documentclass{article}
            \usepackage{graphicx} % Required for inserting images
            \begin{document}
            """)
            for line in file:
                if line:
                    line = line.strip()

                if line and line[0] != "#":
                    process_line(line)
            debug_write.write("\\end{document}")


def process_line(text: str):
    debug_write: DebugWrite = DebugWrite.get_instance()

    strs: list[str] = text.split(";")

    pt: str = strs[0]
    polynomials: str = strs[1]
    substitutes: str = strs[2]
    power_range: str = strs[3]

    ##list_const_coeffs: list[str] = ["1-p^{-1}"]
    list_const_coeffs: list[str] = ["A"]

    p: Polynomial = Polynomial.parse_curly(polynomials,
                                           list_const_coeffs) if "{" in polynomials else Polynomial.parse_brackets(
        polynomials, list_const_coeffs=list_const_coeffs)

    print(f"p = {p}")

    substitution: VariableSubstitution = VariableSubstitution.parse(substitutes, list_const_coeffs=list_const_coeffs)

    p0: Polynomial = substitution.substitude_polynomial(p)

    print(f"p0 = {p0}")
    print(f"substitution: {substitution}")

    exp_prod: ExponentialProduct = ExponentialProduct.parse(pt, list_const_coeffs=list_const_coeffs)
    exp_prod0: ExponentialProduct = substitution.substitude_exponential_product(exp_prod)

    print(f"exp_prod = {exp_prod}")
    print(f"exp_prod0 = {exp_prod0}")

    series_product = SeriesProduct.from_exponential_product(exp_prod0)

    series_product.parse_starting_indices(power_range)

    l: list = series_product.multiply_by_polynomial(p0)

    counter: int = 1

    total_sum: PolynomialSummationRational = PolynomialSummationRational()

    debug_counter: int = 3

    for ser_prod in l:
        # if debug_counter <= 0:
        #   continue

        # debug_counter -= 1

        print(f"[{counter}] ser_prod: {ser_prod}")

        sum_product: PolynomialProductRational = ser_prod.sum()

        total_sum.add_polynomial_rational(sum_product)

        s2: str = "".join(f"{counter}" for i in range(25))

        debug_write.write(f"{s2}\\newline", 1)
        debug_write.write(f"\\[{sum_product}\\]", 1)
        debug_write.write(f"\\[{total_sum}\\]", 1)

        debug_write.write(f"\\[{ser_prod}\\]", 1)
        debug_write.write(f"\\[{sum_product}\\]", 1)

        print(f"[{counter}] sum: {sum_product}")

        counter += 1

    output: str = f"\\[[{exp_prod}][{p}]\\]"
    output = f"{output}{substitution}"
    output = f"{output}\\[{exp_prod0}\\]"
    output = f"{output}\\[{p0}\\]"
    s0: str = "+".join([f"\\[{ser_prod}\\]" for ser_prod in l])
    output = f"{output}{s0}"
    output = f"{output}{total_sum}"

    if debug_write is not None:  # check open
        debug_write.write(output)

    url: str = 'https://www.overleaf.com/project/685ae79d032d2247cd797478'

    # Windows
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
    # webbrowser.get('chrome').open_new_tab(url)


main()
