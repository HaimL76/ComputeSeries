import webbrowser

from debug_write import DebugWrite
from exponential import Exponential, ExponentialProduct
from parse_cases import parse_cases
from polynomial import Polynomial
from polynomial_rational import PolynomialProductRational, PolynomialSummationRational
from process_file import ProcessFile, ProcessFolder
from series import SeriesProduct, SeriesProductSum
from substitution import VariableSubstitution

const_coefficient: str = "(1-p^{-1})"
coeff: str = const_coefficient

def create_symmetry_factors_program():
    with open(".\\saved_output\\output_sage.txt", "r") as fr:
        with open(".\\saved_output\\compute_symmetry_factors.txt", "w") as fw:
            fw.write("# Define the polynomial ring\n")
            fw.write("R.<p,t> = PolynomialRing(QQ)\n")
            fw.write("# Define the fraction field\n")
            fw.write("F = R.fraction_field()\n")
            fw.write("psi = F.hom([1/p, 1/t], F)\n")

            for line in fr:
                if line.startswith("g_") or line.startswith("h_"):
                    arr: list[str] = line.split("=")
                    if isinstance(arr, list) and len(arr) > 1:
                        var_name = arr[0]
                        sf_var_name = f"sf_{var_name}"
                        fw.write(f"{line}\n")
                        fw.write(f"{sf_var_name}=psi({var_name})/{var_name}\n")
                        fw.write(f"print(f\"{sf_var_name}={{{sf_var_name}}}\")\n")
                        print(var_name)
                    else:
                        _ = 0

def main():
    create_symmetry_factors_program()
    return
    parse_cases(".\\input\\cases.tex", ".\\input\\")

    pf: ProcessFolder = ProcessFolder(".\\input\\", ".\\output\\")

    pf.process_folder(".txt$")

main()
