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

def create_symmetry_factors_program(level: int = 1):
    with open(".\\saved_output\\intermediates.txt", "r") as fr:
        with open(".\\saved_output\\compute_symmetry_factors.txt", "w") as fw:
            fw.write("# Define the polynomial ring\n")
            fw.write("R.<p,t> = PolynomialRing(QQ)\n")
            fw.write("# Define the fraction field\n")
            fw.write("F = R.fraction_field()\n")
            fw.write("psi = F.hom([1/p, 1/t], F)\n")

            hs: dict[str, list] = {}

            for line in fr:
                if line.startswith("h_"):
                    arr: list[str] = line.split("=")
                    if isinstance(arr, list) and len(arr) > 1:
                        fw.write(line)
                        var_name = arr[0]

                        arr_indices: list[int] = [int(str_index) for str_index in var_name.split("_") if str_index.isnumeric()]

                        list_indices: list[int] = []

                        for i in range(level):
                            if i < len(arr_indices):
                                list_indices.append(arr_indices[i])

                        str_indices: str = "_".join([str(i) for i in list_indices])

                        if str_indices not in hs.keys():
                            hs[str_indices] = []

                        hs[str_indices].append(var_name)

            for str_indices in hs.keys():
                list_vars: list[str] = hs[str_indices]

                var_h = f"h_{str_indices}"

                sf_var_name = f"sf_{var_h}"

                fw.write(f"{var_h} = QQ.zero()\n")

                for str_var in list_vars:
                    fw.write(f"{var_h}+={str_var}\n")

                fw.write(f"{sf_var_name}=psi({var_h})/{var_h}\n")
                fw.write(f"print(f\"{sf_var_name}={{{sf_var_name}}}\")\n")

def main():
    create_symmetry_factors_program()

    parse_cases(".\\input\\cases.tex", ".\\input\\")

    pf: ProcessFolder = ProcessFolder(".\\input\\", ".\\output\\")

    pf.process_folder(".txt$")

main()
