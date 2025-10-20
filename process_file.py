import copy
import os
import re

from debug_write import DebugWrite
from element import Element
from exponential import ExponentialProduct
from monomial import Monomial
from polynomial import Polynomial
from polynomial_rational import PolynomialSummationRational, PolynomialProductRational
from rational import Rational
from series import SeriesProduct
from substitution import VariableSubstitution

list_const_coeffs: list[str] = ["A"]

str_pt_product_1: str = "p^{8.v_1+11.v_2+11.v_3+7.v_4}*t^{4.v_1+6.v_2+6.v_3+4.v_4}"
str_pt_product_4: str = "p^{7.v_1+11.v_2+11.v_3+8.v_4}*t^{4.v_1+6.v_2+6.v_3+4.v_4}"


class ProcessFolder:
    file_prefix: str = r"""
        \documentclass{article}
        \usepackage{graphicx} % Required for inserting images
        \usepackage{xcolor}
        \begin{document}
    """

    pt_product_1: ExponentialProduct = ExponentialProduct.parse(str_pt_product_1,
                                                                list_const_coeffs=list_const_coeffs)

    pt_product_4: ExponentialProduct = ExponentialProduct.parse(str_pt_product_4,
                                                                list_const_coeffs=list_const_coeffs)

    def __init__(self, input_path: str, output_path: str = None):
        self.conversion_table: dict = {}
        self.reverse_conversion_table: dict = {}

        self.input_folder_path: str = input_path

        self.output_folder_path: str = output_path

        if not self.output_folder_path:
            self.output_folder_path = self.input_folder_path

    def process_folder(self, pattern=None):
        input_file_paths: list = os.listdir(self.input_folder_path)

        output_full_path: str = os.path.abspath(self.output_folder_path)

        if not os.path.exists(output_full_path):
            os.makedirs(output_full_path)
        else:
            output_file_paths: list = os.listdir(self.output_folder_path)

            for existing_output_file in output_file_paths:
                path = os.path.join(self.output_folder_path, existing_output_file)

                os.remove(path)

        out_file_path = os.path.join(output_full_path, "output.tex")

        out_file_path_rational_sum_all: str = out_file_path.replace(".tex", "_rational_sum_all.tex")

        list_rationals: list = []

        rational_sum_of_all_products: PolynomialSummationRational = PolynomialSummationRational()

        with open(out_file_path_rational_sum_all, "w") as fw:
            debug_write: DebugWrite = DebugWrite.get_instance(fw=fw)
            debug_write.write(ProcessFolder.file_prefix)

            dict_rationals: dict = {}

            debug_num_files: int = 0

            debug_files_counter: int = 0

            for path in input_file_paths:
                if 0 < debug_num_files <= debug_files_counter:
                    break

                debug_files_counter += 1

                if pattern:
                    search_result = re.search(pattern, path)

                    if search_result:
                        path = os.path.join(self.input_folder_path, path)
                        path = os.path.abspath(path)
                        print(path)
                        proc_file: ProcessFile = ProcessFile(path, output_directory=output_full_path)

                        proc_file.process_file(conversion_table=self.conversion_table,
                                               reverse_conversion_table=self.reverse_conversion_table,
                                               general_debug_writer=debug_write, list_rationals=dict_rationals,
                                               total_total_sum=rational_sum_of_all_products)

            cases: int = 0

            for key in dict_rationals:
                l: list = dict_rationals[key]

                cases += len(l)

            Element.reverse_conversion_table = self.reverse_conversion_table

            total = PolynomialSummationRational()

            for key in dict_rationals:
                l: list = dict_rationals[key]

                total0 = PolynomialSummationRational()

                for tup in l:
                    pol_sum_rational: PolynomialSummationRational = tup[0]
                _ = 0

            debug_write.write("\\tiny{")

            debug_write.write(f"{rational_sum_of_all_products}")

            debug_write.write("}")

            debug_write.write("\\end{document}")

        finished: bool = False

        index: int = 0

        take: int = 0

        while not finished:
            out_file_path_numerator_polynmomials: str = out_file_path.replace(".tex", f"_numerator_polynomials.tex")
            out_file_path_sum_numerator: str = out_file_path.replace(".tex", f"_sum_numerator.tex")

            if take > 0:
                out_file_path_sum_numerator = out_file_path.replace(".tex", f"{index}.tex")

            str_denominator: str = rational_sum_of_all_products.get_ltx_str_denominator()

            str0, finished = rational_sum_of_all_products.get_ltx_str_partial(index * take, take)

            index += 1

            with (open(out_file_path_sum_numerator, "w") as fw_sum_numerator,
                  open(out_file_path_numerator_polynmomials, "w") as fw_numerator_polynomials):
                fw_numerator_polynomials.write(ProcessFolder.file_prefix)
                fw_sum_numerator.write(ProcessFolder.file_prefix)

                fw_numerator_polynomials.write("\\tiny{")
                fw_sum_numerator.write("\\tiny{")

                total_total_sum0: PolynomialSummationRational = copy.deepcopy(rational_sum_of_all_products)

                sum1, list_pols0, dict_numerator = total_total_sum0.multiply()

                sum_numerator: Polynomial = Polynomial(monoms=[Monomial(coeff=Rational(0))])

                for key in dict_numerator:
                    list_monomials = dict_numerator[key]

                    sum_monomials: Polynomial = Polynomial(monoms=[Monomial(coeff=Rational(0))])

                    monomials_counter: int = 0

                    line_monomials_counter: int = 0

                    for monomial in list_monomials:
                        monomial_copy: Monomial = copy.deepcopy(monomial)

                        if line_monomials_counter == 0:
                            fw_numerator_polynomials.write("$")
                        else:
                            fw_numerator_polynomials.write(",")

                        fw_numerator_polynomials.write(f"{monomial_copy.get_ltx_str(print_sign=Monomial.Print_Sign_If_Minus)}")

                        monomials_counter += 1
                        line_monomials_counter += 1

                        line_break: bool = line_monomials_counter == 8
                        polynomials_printed: bool = monomials_counter == len(list_monomials)

                        if line_break or polynomials_printed:
                            if polynomials_printed:
                                fw_numerator_polynomials.write("\\\\\\\\")

                            fw_numerator_polynomials.write("$\n\n")
                            line_monomials_counter = 0

                        polynomial: Polynomial = Polynomial(monoms=[monomial_copy])
                        sum_monomials += polynomial

                    sum_numerator += sum_monomials

                fw_numerator_polynomials.write("}\\end{document}")
                fw_sum_numerator.write(f"${sum_numerator}$")
                fw_sum_numerator.write("}")
                fw_sum_numerator.write("\\end{document}")


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

    def process_file(self, conversion_table: dict, reverse_conversion_table: dict,
                     general_debug_writer: DebugWrite,
                     list_rationals: dict, total_total_sum: PolynomialSummationRational):
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
                                          reverse_conversion_table=reverse_conversion_table,
                                          general_debug_writer=general_debug_writer, list_rationals=list_rationals,
                                          total_total_sum=total_total_sum)

                for key in conversion_table.keys():
                    index: int = conversion_table[key]

                    s: str = f"x_{index}"

                    s = f"\\[{s}\\rightarrow{{p^{{{key[0]}}}t^{{{key[1]}}}}}\\]"

                    debug_write.write(s)

                debug_write.write("\\end{document}")

    def process_line(self, text: str, conversion_table: dict, reverse_conversion_table: dict,
                     general_debug_writer: DebugWrite,
                     list_rationals: dict, total_total_sum: PolynomialSummationRational):
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

            str_case_indices: str = ".".join([str(index) for index in self.case_indices])
            str_case_indices = f"Case {str_case_indices}"

            debug_write.write(f"\n{str_case_indices}\n")

            if general_debug_writer is not None:
                general_debug_writer.write(f"\n{str_case_indices}\n")

            for polynomial in self.polynomials:
                debug_write.write(f"\\[{polynomial}\\]", 1)

                self.substitution_counter += 1
                debug_write.write(f"Substitution no. {self.substitution_counter}")

                debug_write.write(f"{self.substitution}")

                converted_polynomial: Polynomial = self.substitution.substitude_polynomial(polynomial)

                debug_write.write(f"\\[{converted_polynomial}\\]", 1)

                converted_pt_product: ExponentialProduct = \
                    self.substitution.substitude_exponential_product(self.pt_product)

                series_product = SeriesProduct.from_exponential_product(converted_pt_product, conversion_table,
                                                                        reverse_conversion_table)

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

                sum0 = Polynomial(monoms=[Monomial(coeff=Rational(0))])

                for ser_prod in list_series:
                    ser_prod0 = copy.deepcopy(ser_prod)
                    ser_prod1 = copy.deepcopy(ser_prod0)

                    sum_product: PolynomialProductRational = ser_prod0.sum()

                    for pol in sum_product.denominator.list_polynomials:
                        if pol.power == Rational(4):
                            aaa = ser_prod1.sum()

                    sum_product0: PolynomialProductRational = copy.deepcopy(sum_product)

                    sum_product1: PolynomialProductRational = copy.deepcopy(sum_product0)

                    sum_product2: PolynomialProductRational = copy.deepcopy(sum_product1)

                    debug_write.write(f"\\[{ser_prod}={sum_product}\\]", 1)

                    debug_sums.append(copy.deepcopy(sum_product0))

                    total_sum.add_polynomial_rational(sum_product1)

                    total_total_sum.add_polynomial_rational(sum_product2)

                store_by_indices(list_rationals=list_rationals, total_sum=total_sum,
                            case_indices=self.case_indices)

                debug_write: DebugWrite = DebugWrite.get_instance()

                debug_write.write("\nTotal sum\n")

                #total_sum.multiply(sum0)

                if debug_write is not None:
                    # for sum_product in debug_sums:
                    #   str_to_print: str = f"\\[{sum_product}\\]"
                    #  debug_write.write(str_to_print)

                    str_to_print: str = f"{total_sum}"
                    debug_write.write(str_to_print)

                    if general_debug_writer is not None:
                        general_debug_writer.write(str_to_print)

                    total_sum0 = copy.deepcopy(total_sum)

                    sum_of_pols0, list0, dict_by_powers = total_sum0.multiply()

                    str_to_print: str = f"{total_sum}"
                    debug_write.write(str_to_print)

                    if general_debug_writer is not None:
                        general_debug_writer.write(str_to_print)

                    for pol0 in list0:
                        str_to_print = f"\\[{pol0}\\]"
                        debug_write.write(str_to_print)

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
