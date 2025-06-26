import webbrowser

from exponential import Exponential, ExponentialProduct
from polynomial import Polynomial
from polynomial_rational import PolynomialProductRational, PolynomialSummationRational
from series import SeriesProduct, SeriesProductSum
from substitution import VariableSubstitution

import matplotlib.pyplot as plt

const_coefficient: str = "(1-p^{-1})"
coeff: str = const_coefficient

def main():
    process_file("c:\\gpp\\1.txt")

def process_file(file_path: str):
    with open(file_path, 'r') as file:
        with open(r"c:\gpp\1.tex", "w") as fw:
            fw.write(r"""
            \documentclass{article}
            \usepackage{graphicx} % Required for inserting images
            \begin{document}
            """)
            for line in file:
                if line:
                    line = line.strip()

                if line:
                    process_line(line, fw)
            fw.write("""\end{document}""")

def process_line(text: str, fw):
    strs: list[str] = text.split(";")

    pt: str = strs[0]
    polynomials: str = strs[1]
    substitutes: str = strs[2]
    power_range: str = strs[3]

    p: Polynomial = Polynomial.parse_brackets(polynomials)

    print(f"p = {p}")

    substitution: VariableSubstitution = VariableSubstitution.parse(substitutes)

    p0: Polynomial = substitution.substitude_polynomial(p)

    print(f"p0 = {p0}")
    print(f"substitution: {substitution}")

    exp_prod: ExponentialProduct = ExponentialProduct.parse(pt)
    exp_prod0: ExponentialProduct = substitution.substitude_exponential_product(exp_prod)

    print(f"exp_prod = {exp_prod}")
    print(f"exp_prod0 = {exp_prod0}")

    series_product = SeriesProduct.from_exponential_product(exp_prod0)

    series_product.parse_starting_indices(power_range)

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

    output: str = f"\\[[{exp_prod}][{p}]\\]"
    output = f"{output}{substitution}"
    output = f"{output}\\[{exp_prod0}\\]"
    output = f"{output}\\[{p0}\\]"
    s0: str = "+".join([f"\\[{ser_prod}\\]" for ser_prod in l])
    output = f"{output}{s0}"
    output = f"{output}{total_sum}"

    if fw is not None:# check open
        fw.write(output)

    url: str = 'https://www.overleaf.com/project/685ae79d032d2247cd797478'

    # Windows
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
    #webbrowser.get('chrome').open_new_tab(url)
main()