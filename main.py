import re
import webbrowser

from debug_write import DebugWrite
from exponential import Exponential, ExponentialProduct
from orders import check_covering
from parse_cases import parse_cases
from polynomial import Polynomial
from polynomial_rational import PolynomialProductRational, PolynomialSummationRational
from process_file import ProcessFile, ProcessFolder
from series import SeriesProduct, SeriesProductSum
from stack import Stack
from substitution import VariableSubstitution

const_coefficient: str = "(1-p^{-1})"
coeff: str = const_coefficient

def create_symmetry_factors_program(level: int = 1):
    with open(".\\saved_output\\intermediates.txt", "r") as fr:
        with open(".\\saved_output\\compute_symmetry_factors.txt", "w") as fw:
            fw.write("# Define the polynomial ring\n")
            fw.write("R.<p,t> = PolynomialRing(QQ)\n")
            fw.write("# Define the fraction field\n")
            fw.write("F = R.fraction_field()\n")
            fw.write("psi = F.hom([1/p, 1/t], F)\n")

            for line in fr:
                arr: list[str] = line.split("=")

                if isinstance(arr, list) and len(arr) > 1:
                    var_name: str = arr[0]

                    if isinstance(var_name, str) and len(var_name) > 0 and not var_name.startswith("####"):
                        fw.write(f"{line}\n")

                        sf_var_name = f"sf_{var_name}"

                        fw.write(f"{sf_var_name}=psi({var_name})/{var_name}\n")

                        fw.write(f"print(f\"{sf_var_name}={{{sf_var_name}}}\")\n")

    return


def main():
    check_covering()
    return
    create_symmetry_factors_program()

    parse_cases(".\\input\\cases.tex", ".\\input\\")

    pf: ProcessFolder = ProcessFolder(".\\input\\", ".\\output\\")

    pf.process_folder(".txt$")


main()
