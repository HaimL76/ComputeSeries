import re
import webbrowser

from debug_write import DebugWrite
from exponential import Exponential, ExponentialProduct
from parse_cases import parse_cases
from polynomial import Polynomial
from polynomial_rational import PolynomialProductRational, PolynomialSummationRational
from process_file import ProcessFile, ProcessFolder
from series import SeriesProduct, SeriesProductSum
from stack import Stack
from substitution import VariableSubstitution

const_coefficient: str = "(1-p^{-1})"
coeff: str = const_coefficient


def build_order(symbols: list[str], index: int, stack: Stack, list_strs: list[(str, str)]):
    if index >= len(symbols):
        str0: str = "".join([str(obj) for obj in stack])
        str1: str = ",".join(symbols)

        tup: tuple[str, str] = str0, str1

        list_strs.append(tup)
    else:
        symbol: str = symbols[index]

        arr: list[str] = symbol.split("_")

        if isinstance(arr, list) and len(arr) == 2 and arr[1].isnumeric():
            var_index: int = int(arr[1])

            stack.push(var_index)
            build_order(symbols, index + 1, stack=stack, list_strs=list_strs)
            _ = stack.pop()

        if symbol == ">":
            stack.push(symbol)
            build_order(symbols, index + 1, stack=stack, list_strs=list_strs)
            _ = stack.pop()

        if symbol == r"\geq":
            stack.push(">")
            build_order(symbols, index + 1, stack=stack, list_strs=list_strs)
            _ = stack.pop()

            stack.push("=")
            build_order(symbols, index + 1, stack=stack, list_strs=list_strs)
            _ = stack.pop()

        if symbol == "0":
            stack.push(symbol)
            build_order(symbols, index + 1, stack=stack, list_strs=list_strs)
            _ = stack.pop()



def check_covering():
    dict_order: dict = {}

    regex_overset: str = r"\\overset\{[a-z]\}"
    regex_var: str = r"v_\d"
    regex_var_start: str = rf"^{regex_var}"

    regex_geq: str = r"\\geq"
    regex_geq_start: str = rf"^{regex_geq}"

    arr_order: list[list[tuple]] = []

    list_strs: list[(str, str)] = []

    list_symbols: list[list[str]] = []

    with open(".\\input\\cases.tex") as fr:
        for line in fr:
            line0: str = line
            list_vars: list = []

            while len(line) > 0:
                offset: int = 1

                finds = re.findall(regex_var_start, line)

                if isinstance(finds, list) and len(finds) > 0:
                    str_var: str = finds[0]

                    offset = len(str_var)

                    list_vars.append(str_var)
                else:
                    str0: str = line[:1]

                    if str0 in [">", "<", "+", "0"]:
                        list_vars.append(str0)
                    else:
                        finds = re.findall(regex_geq_start, line)

                        if isinstance(finds, list) and len(finds) > 0:
                            str_geq: str = finds[0]

                            offset = len(str_geq)

                            list_vars.append(str_geq)

                line: str = line[offset:]

            index: int = 0

            var_index: int = 0

            operator1: int = 0
            operator2: int = 1

            for symbol in list_vars:
                arr0: list[str] = symbol.split("_")

                if isinstance(arr0, list) and len(arr0) == 2 and arr0[1].isnumeric():
                    var_index: int = int(arr0[1])

            list_vars0: list[str] = []

            for index in range(len(list_vars)):
                prev_symbol: str = ""
                next_symbol: str = ""
                curr_symbol: str = list_vars[index]

                if index > 0:
                    prev_symbol = list_vars[index - 1]

                if index < (len(list_vars) - 1):
                    next_symbol = list_vars[index + 1]

                sum_of_vars: bool = "+" in [prev_symbol, curr_symbol, next_symbol]

                if not sum_of_vars:
                    list_vars0.append(curr_symbol)

            cleaned_doubles: bool = False

            while not cleaned_doubles:
                list_vars = list_vars0
                list_vars0 = []

                doubles_counter: int = 0

                for index in range(len(list_vars)):
                    prev_symbol: str = ""
                    curr_symbol: str = list_vars[index]

                    if index > 0:
                        prev_symbol = list_vars[index - 1]

                    double_found: bool = curr_symbol == prev_symbol

                    if double_found:
                        doubles_counter += 1

                    if not double_found:
                        list_vars0.append(curr_symbol)

                if doubles_counter < 1:
                    cleaned_doubles = True

            list_vars = list_vars0
            list_vars0 = []

            for index in range(len(list_vars)):
                prev_symbol: str = ""
                next_symbol: str = ""
                curr_symbol: str = list_vars[index]

                if index > 0:
                    prev_symbol = list_vars[index - 1]

                if index < len(list_vars) - 1:
                    next_symbol = list_vars[index + 1]

                remove: bool = curr_symbol in [">", r"\geq"] and ">" in [prev_symbol, next_symbol]

                if not remove:
                    list_vars0.append(curr_symbol)

            if len(list_vars0) > 0 and list_vars0[0] in [">", r"\geq"]:
                list_vars0 = list_vars0[1:]

            if len(list_vars0) > 1 and list_vars0[-1] == "0" and list_vars0[-2]:
                list_vars0 = list_vars0[:-2]

            order_: list[tuple] = [()] * 3

            curr_var: int = 0

            index = 0

            if "overset" in line0:
                build_order(list_vars0, 0, stack=Stack(), list_strs=list_strs)
                #print(f"{list_vars0} {line0}")
                list_symbols.append(list_vars0)

    with open(".\\saved_output\\orders.txt", "w") as fw:
        for order in list_strs:
            fw.write(f"{order}\n")

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
