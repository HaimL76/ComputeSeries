import copy
import os
import re

from debug_write import DebugWrite
from exponential import ExponentialProduct
from polynomial import Polynomial
from polynomial_rational import PolynomialSummationRational, PolynomialProductRational
from series import SeriesProduct
from substitution import VariableSubstitution

list_const_coeffs: list[str] = ["A"]


class ProcessFolder:
    def __init__(self, input_path: str, output_path: str = None):
        self.input_folder_path: str = input_path

        self.output_folder_path: str = output_path

        if not self.output_folder_path:
            self.output_folder_path = self.input_folder_path

    def process_folder(self, pattern=None):
        file_paths: list = os.listdir(self.input_folder_path)

        output_full_path: str = os.path.abspath(self.output_folder_path)

        for path in file_paths:
            if pattern:
                search_result = re.search(pattern, path)

                if search_result:
                    path = os.path.join(self.input_folder_path, path)
                    path = os.path.abspath(path)
                    print(path)
                    proc_file: ProcessFile = ProcessFile(path, output_directory=output_full_path)
                    proc_file.process_file()


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

    def process_file(self):
        with open(self.file_path, 'r') as file:
            file_name: str = os.path.basename(self.file_path)

            out_file_path: str = file_name.replace(".txt", ".tex")

            if not os.path.exists(self.output_directory_path):
                os.makedirs(self.output_directory_path)q

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
                        self.process_line(line)
                debug_write.write("\\end{document}")

    def process_line(self, text: str):
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
                self.pt_product: ExponentialProduct = ExponentialProduct.parse(text,
                                                                               list_const_coeffs=list_const_coeffs)

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
            for polynomial in self.polynomials:
                debug_write.write(f"\\[{polynomial}\\]", 1)

                self.substitution_counter += 1
                debug_write.write(f"Substitution no. {self.substitution_counter}")

                debug_write.write(f"{self.substitution}")

                converted_polynomial: Polynomial = self.substitution.substitude_polynomial(polynomial)

                debug_write.write(f"\\[{converted_polynomial}\\]", 1)

                converted_pt_product: ExponentialProduct = \
                    self.substitution.substitude_exponential_product(self.pt_product)

                series_product = SeriesProduct.from_exponential_product(converted_pt_product)

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

                    _ = 0

                debug_write: DebugWrite = DebugWrite.get_instance()

                if debug_write is not None:
                    # for sum_product in debug_sums:
                    #   str_to_print: str = f"\\[{sum_product}\\]"
                    #  debug_write.write(str_to_print)

                    str_to_print: str = f"{total_sum}"
                    debug_write.write(str_to_print)

                _ = 0

            self.substitution = None
            self.start_index = None

    def aaa(self):
        polynomials: str = strs[1]
        substitutes: str = strs[2]
        power_range: str = strs[3]

        ##list_const_coeffs: list[str] = ["1-p^{-1}"]

        p: Polynomial = Polynomial.parse_curly(polynomials,
                                               list_const_coeffs) if "{" in polynomials else Polynomial.parse_brackets(
            polynomials, list_const_coeffs=list_const_coeffs)

        print(f"p = {p}")

        debug_write.write(f"\\[{p}\\]\\newline", 1)

        substitution: VariableSubstitution = VariableSubstitution.parse(substitutes,
                                                                        list_const_coeffs=list_const_coeffs)

        p0: Polynomial = substitution.substitude_polynomial(p)

        print(f"p0 = {p0}")
        print(f"substitution: {substitution}")

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
        s2: str = "".join(f"-" for i in range(25))
        debug_write.write(f"{s2}\\[{sum_product}\\]", 1)
        s2: str = "".join(f"+" for i in range(25))
        debug_write.write(f"{s2}{total_sum}", 1)

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
