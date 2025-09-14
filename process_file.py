import copy
import os
import re

from debug_write import DebugWrite
from element import Element
from exponential import ExponentialProduct
from polynomial import Polynomial
from polynomial_rational import PolynomialSummationRational, PolynomialProductRational
from series import SeriesProduct
from substitution import VariableSubstitution

list_const_coeffs: list[str] = ["A"]

str_pt_product_1: str = "p^{8.v_1+11.v_2+11.v_3+7.v_4}*t^{4.v_1+6.v_2+6.v_3+4.v_4}"
str_pt_product_4: str = "p^{7.v_1+11.v_2+11.v_3+8.v_4}*t^{4.v_1+6.v_2+6.v_3+4.v_4}"


class ProcessFolder:
    pt_product_1: ExponentialProduct = ExponentialProduct.parse(str_pt_product_1,
                                                                list_const_coeffs=list_const_coeffs)

    pt_product_4: ExponentialProduct = ExponentialProduct.parse(str_pt_product_4,
                                                                list_const_coeffs=list_const_coeffs)

    def __init__(self, input_path: str, output_path: str = None):
        self.conversion_table: dict = {}

        self.input_folder_path: str = input_path

        self.output_folder_path: str = output_path

        if not self.output_folder_path:
            self.output_folder_path = self.input_folder_path

    def process_folder(self, pattern=None):
        file_paths: list = os.listdir(self.input_folder_path)

        output_full_path: str = os.path.abspath(self.output_folder_path)

        if not os.path.exists(output_full_path):
            os.makedirs(output_full_path)

        out_file_path = os.path.join(output_full_path, "output.tex")

        list_rationals: list = []

        with open(out_file_path, "w") as fw:
            debug_write: DebugWrite = DebugWrite.get_instance(fw=fw)
            debug_write.write(r"""
            \documentclass{article}
            \usepackage{graphicx} % Required for inserting images
            \usepackage{xcolor}
            \begin{document}
            """)

            dict_rationals: dict = {}

            for path in file_paths:
                if pattern:
                    search_result = re.search(pattern, path)

                    if search_result:
                        path = os.path.join(self.input_folder_path, path)
                        path = os.path.abspath(path)
                        print(path)
                        proc_file: ProcessFile = ProcessFile(path, output_directory=output_full_path)
                        proc_file.process_file(conversion_table=self.conversion_table,
                                               debug_write0=debug_write, list_rationals=dict_rationals)

                        cases: int = 0

                        for key in dict_rationals:
                            l: list = dict_rationals[key]

                            cases += len(l)

            debug_write.write("\\end{document}")


class ProcessFile:
    def __init__(self, path: str, output_directory: str):
        self.file_path: str = path
        self.pt_product = None
        self.polynomials = None
        self.reset_polynomials = False
        self.substitution = None
        self.reset_substitution = False
        self.start_index = None
        self.substitution_counter: int = 0
        self.output_directory_path: str = output_directory
        self.case_indices: list[int] = []

    def process_file(self, conversion_table: dict, debug_write0: DebugWrite,
                     list_rationals: dict):
        with open(self.file_path, 'r') as file:
            file_name: str = os.path.basename(self.file_path)

            out_file_path: str = file_name.replace(".txt", ".tex")

            if not os.path.exists(self.output_directory_path):
                os.makedirs(self.output_directory_path)

            out_file_path = os.path.join(self.output_directory_path, out_file_path)

            with open(out_file_path, "w") as fw:
                debug_write: DebugWrite = DebugWrite.get_instance(fw=fw)
                debug_write.write(r"""
                \documentclass{article}
                \usepackage{graphicx} % Required for inserting images
                \usepackage{xcolor}
                \begin{document}
                """)

                for line in file:
                    if line:
                        line = line.strip()

                    if line and line[0] != "#":
                        self.process_line(line, conversion_table=conversion_table,
                                          debug_write0=debug_write0, list_rationals=list_rationals)

                for key in conversion_table.keys():
                    index: int = conversion_table[key]

                    s: str = f"x_{index}"

                    s = f"\\[{s}\\rightarrow{{p^{{{key[0]}}}t^{{{key[1]}}}}}\\]"

                    debug_write.write(s)

                debug_write.write("\\end{document}")

    def process_line(self, text: str, conversion_table: dict, debug_write0: DebugWrite,
                     list_rationals: dict):
        is_polynomial: bool = False
        is_substitution: bool = False
        is_index: bool = False

        debug_write: DebugWrite = DebugWrite.get_instance()

        if text:
            text = text.strip()

        prefix = "pt-product: "

        if text.startswith(prefix):
            text = text[len(prefix):]

            if text:
                text = text.strip()

            if text:
                arr11: list[str] = text.split("_")

                index11: int = 0

                if len(arr11) == 2 and arr11[0] == "v" and arr11[1] and arr11[1].isnumeric():
                    index11 = int(arr11[1])

                self.pt_product: ExponentialProduct = copy.deepcopy(ProcessFolder.pt_product_1) if index11 == 1 \
                    else copy.deepcopy(ProcessFolder.pt_product_4)

                _ = 0

        text0: str = text.strip()

        if text0.startswith("="):
            text0 = text0.strip("=").strip()

            list0: list[str] = text0.split(".")

            list1: list[int] = [0] * len(list0)

            not_num: bool = False
            index: int = 0

            while not not_num and index < len(list0):
                s: str = list0[index]

                if s.isnumeric():
                    list1[index] = int(s)
                else:
                    not_num = True

                index += 1

            if not not_num:
                self.case_indices = list1

        prefix = "polynomial: "

        if text.startswith(prefix):
            text = text[len(prefix):]

            if text:
                text = text.strip()

            if text:
                arr: list[str] = text.split(";")

                for s in arr:
                    if s:
                        s = s.strip()

                    if s:
                        p: Polynomial = Polynomial.parse_curly(s, list_const_coeffs) if "{" in s \
                            else Polynomial.parse_brackets(s, list_const_coeffs=list_const_coeffs)

                        if self.reset_polynomials:
                            self.polynomials = None

                        if not isinstance(self.polynomials, list):
                            self.polynomials = []

                        self.polynomials.append(p)

                        is_polynomial = True

        prefix = "substitution: "

        if text.startswith(prefix):
            text = text[len(prefix):]

            if text:
                text = text.strip()

            if text:
                is_substitution = True

                self.substitution = VariableSubstitution.parse(text, list_const_coeffs=list_const_coeffs,
                                                               substitution=self.substitution)

        prefix = "indices: "

        if text.startswith(prefix):
            text = text[len(prefix):]

            if text:
                text = text.strip()

            if text:
                arr = text.split(",")

                for s in arr:
                    if s:
                        s = s.strip()

                    if s:
                        arr_index: list[str] = s.split(">=")

                        if isinstance(arr_index, list) and len(arr_index) > 0:
                            is_index = True

                            s0 = arr_index[0]

                            index = 1

                            if len(arr_index) > 1:
                                s1 = arr_index[1]

                                index = 1 if s1 == "1" else 0

                            if not isinstance(self.start_index, dict):
                                self.start_index = {}

                            self.start_index[s0] = index

        if text == "run":

            s: str = ".".join([str(index) for index in self.case_indices])
            debug_write.write(f"\n{s}\n")
            debug_write0.write(f"\n{s}\n")
            for polynomial in self.polynomials:
                debug_write.write(f"\\[{polynomial}\\]", 1)

                self.substitution_counter += 1
                debug_write.write(f"Substitution no. {self.substitution_counter}")

                debug_write.write(f"{self.substitution}")

                converted_polynomial: Polynomial = self.substitution.substitude_polynomial(polynomial)

                debug_write.write(f"\\[{converted_polynomial}\\]", 1)

                converted_pt_product: ExponentialProduct = \
                    self.substitution.substitude_exponential_product(self.pt_product)

                series_product = SeriesProduct.from_exponential_product(converted_pt_product, conversion_table)

                if isinstance(series_product, SeriesProduct) and isinstance(self.start_index, dict) \
                        and len(self.start_index) > 0:
                    for key in self.start_index.keys():
                        if key:
                            val: int = self.start_index[key]

                            if isinstance(val, int):
                                series_product.add_start_index(key, val)

                list_series: list = series_product.multiply_by_polynomial(converted_polynomial)

                total_sum: PolynomialSummationRational = PolynomialSummationRational()

                debug_sums: list = []

                debug_write.write("All series and their sums")

                for ser_prod in list_series:
                    sum_product: PolynomialProductRational = ser_prod.sum()

                    debug_write.write(f"\\[{ser_prod}={sum_product}\\]", 1)

                    debug_sums.append(copy.deepcopy(sum_product))

                    total_sum.add_polynomial_rational(sum_product)

                store_by_indices(list_rationals=list_rationals, total_sum=total_sum,
                            case_indices=self.case_indices)

                debug_write: DebugWrite = DebugWrite.get_instance()

                if debug_write is not None:
                    # for sum_product in debug_sums:
                    #   str_to_print: str = f"\\[{sum_product}\\]"
                    #  debug_write.write(str_to_print)

                    str_to_print: str = f"{total_sum}"
                    debug_write.write(str_to_print)
                    debug_write0.write(str_to_print)

                _ = 0

            self.substitution = None
            self.start_index = None


def store_by_indices(list_rationals: dict, total_sum, case_indices):
    list_polynomials: list[Polynomial] = total_sum.denominator.list_polynomials

    if isinstance(list_rationals, dict) and isinstance(list_polynomials, list):
        indices: dict[int, int] = {}

        list_pols: list = total_sum.denominator.list_polynomials
        for pol in list_pols:
            list_mons: list = pol.monomials

            for mon in list_mons:
                dict_elems: dict = mon.elements

                for key in dict_elems:
                    elem: Element = dict_elems[key]

                    if elem.index is not None:
                        ind = elem.index

                        if ind is not None:
                            # we check that there is no other power of the same symbol
                            if ind in indices:
                                power: int = indices[ind]

                                if power != pol.power:
                                    _ = 0 #debug

                            indices[ind] = pol.power

        list_indices: list[int] = sorted(indices.keys())

        list0: list[str] = [""] * len(list_indices)

        index: int = 0

        for index in range(0, len(list_indices)):
            ind: int = list_indices[index]
            power: int = indices[ind]

            s: str = f"{ind}-{power}"

            list0[index] = s

        key = "=".join([s for s in list0])

        if len(list0) != 4:
            _ = 0

        if key not in list_rationals:
            list_rationals[key] = []

        list_rationals[key].append((total_sum, case_indices))

    _ = 0
