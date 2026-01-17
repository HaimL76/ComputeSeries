import re
import webbrowser

from debug_write import DebugWrite
from exponential import Exponential, ExponentialProduct
from list_orders import list_orders
from list_orders import list_orders
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

            list_var_h_subsets: list[tuple[str, list[str]]] = [
                ("hh_0",["h_7_1", "h_6_2", "h_5", "h_6_1", "h_7_3", "h_1", "h_7_2", "h_6_3"]),
                ("hh_2_1", ["h_2_1_1", "h_2_1_2", "h_2_1_3", "h_2_1_4", "h_2_1_5"]),
                ("hh_2_2", ["h_2_2_1", "h_2_2_2", "h_2_2_3"]),
                ("hh_3_1", ["h_3_1_1", "h_3_1_2", "h_3_1_3", "h_3_1_4", "h_3_1_5", "h_3_1_6", "h_3_1_7"]),
                ("hh_3_2", ["h_3_2_1", "h_3_2_2", "h_3_2_3", "h_3_2_4", "h_3_2_5", "h_3_2_6", "h_3_2_7"]),
                ("hh_4_1", ["h_4_1_1", "h_4_1_2", "h_4_1_3", "h_4_1_4", "h_4_1_5"]),
                ("hh_4_2", ["h_4_2_1", "h_4_2_2", "h_4_2_3"]),
                ("hh_4", ["hh_4_1", "hh_4_2"]),
                ("hh_8_1", ["h_8_1_1", "h_8_1_2", "h_8_1_3", "h_8_1_4", "h_8_1_5", "h_8_1_6", "h_8_1_7"]),
                ("hh_8_2", ["h_8_2_1", "h_8_2_2", "h_8_2_3", "h_8_2_4", "h_8_2_5", "h_8_2_6", "h_8_2_7"]),
                ("hh_01", ["hh_3_2", "hh_8_2"]),
                ("hh_02", ["hh_3_1", "hh_8_1"]),
            ]

            for i in range(len(list_var_h_subsets)):
                tuple_var_h: tuple[str, list[str]] = list_var_h_subsets[i]

                str_hh: str = "+".join(tuple_var_h[1])

                str_hh_i: str = tuple_var_h[0]
                fw.write(f"{str_hh_i}={str_hh}\n")

                sf_var_h = f"sf_{str_hh_i}"

                fw.write(f"{sf_var_h}=psi({str_hh_i})/{str_hh_i}\n")

                #sf_var_h_simplified = f"sf_hh_{i}_simplified"

                #fw.write(f"{sf_var_h_simplified}={sf_var_h}.simplify_full()\n")

                fw.write(f"print(f\"{sf_var_h}={{{sf_var_h}}}\")\n")

    return


def main():
    check_covering()
    #return
    create_symmetry_factors_program()

    list_orders(".\\input\\cases.tex")#, ".\\input\\")

    return

    parse_cases(".\\input\\cases.tex", ".\\input\\")

    pf: ProcessFolder = ProcessFolder(".\\input\\", ".\\output\\")

    pf.process_folder(".txt$")


main()
