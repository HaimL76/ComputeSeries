import copy
import os
import random
import re
from idlelib.replace import replace

from debug_write import DebugWrite
from element import Element
from exponential import ExponentialProduct
from monomial import Monomial
from polynomial import Polynomial, PolynomialProduct
from polynomial_rational import PolynomialSummationRational, PolynomialProductRational, PolynomialRational
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

    def __init__(self, input_path: str, output_path: str = None, debug: bool = False):
        self.print_debug: bool = debug
        self.conversion_table: dict = {}
        self.reverse_conversion_table: dict = {}

        self.input_folder_path: str = input_path

        self.output_folder_path: str = output_path

        if not self.output_folder_path:
            self.output_folder_path = self.input_folder_path

    def write_sage_program(self, dict_series_sums: dict,
                           out_file_path_sage_series_sums: str):
        num_series_products: int = 0

        for key in dict_series_sums.keys():
            val_dict = dict_series_sums[key]

            if isinstance(val_dict, list):
                length: int = len(val_dict)

                num_series_products += length

        dict_random_numbers: dict[int, int] = {}

        num_random_numbers: int = 10

        series_product_counter: int = 0

        while False:# len(dict_random_numbers) < num_random_numbers:
            random_number = int(random.random() * num_series_products)

            dict_random_numbers[random_number] = 0

        out_file_path_sage_series_sums_debug: str = out_file_path_sage_series_sums.replace(".txt", "_debug.txt")

        list_debug_data: list[str] = []

        with open(out_file_path_sage_series_sums, "w") as fw_sage_series_sums:
            #fw_sage_series_sums.write("# Define the polynomial ring\n")
            #fw_sage_series_sums.write("R.<p,t> = PolynomialRing(QQ)\n")
            #fw_sage_series_sums.write("F = R.fraction_field()\n")
            #fw_sage_series_sums.write("psi = F.hom([1/p, 1/t], F)\n")
            fw_sage_series_sums.write("var(\"p,t,a,b,c,d\")\n")
            fw_sage_series_sums.write("f = QQ.zero()\n")

            for str_case_indices in dict_series_sums.keys():
                if str_case_indices != "Case 4.2.2":
                    _ = 0#continue
                tup_val: tuple = dict_series_sums[str_case_indices]
                list_series_sums: list = tup_val[-1]
                original_polynomial: Polynomial = tup_val[0]
                converted_polynomial: Polynomial = tup_val[1]
                substitution: VariableSubstitution = tup_val[2]

                original_number_of_monomials: int = len(original_polynomial.monomials)
                converted_number_of_monomials: int = len(converted_polynomial.monomials)

                str_original_polynomial: str = original_polynomial.get_sage_str()
                str_converted_polynomial: str = converted_polynomial.get_sage_str()
                str_substitution: str = substitution.get_sage_str()

                comments: list[str] = []

                sharps: str = "##########"

                prefix: str = f"{sharps} [{str_case_indices}]"

                #comments.append(f"{prefix} {str_original_polynomial}")
                #comments.append(f"{prefix} {str_substitution}")
                #comments.append(f"{prefix} {str_converted_polynomial}")

                str_comments: str = "\n".join(comments)

                counter: int = 0

                str_debug: str = ""

                str_case_indices0: str = str_case_indices.replace("Case", "")
                str_case_indices0 = str_case_indices0.replace(".", "_")
                str_case_indices0 = str_case_indices0.strip()

                var_h: str = f"h_{str_case_indices0}"

                fw_sage_series_sums.write(f"{var_h} = QQ.zero()\n")

                for tup in list_series_sums:
                    dict_series_product: dict = tup[2]

                    monomial: Monomial = converted_polynomial.monomials[counter]

                    str_monomial: str = monomial.get_sage_str()

                    counter += 1

                    ##fw_sage_series_sums.write(f"{str_comments}\n")

                    ##fw_sage_series_sums.write(f"{prefix} [monomial {counter}/{converted_number_of_monomials}] {str_monomial}\n")# monomial {counter}/{converted_number_of_monomials}\n")

                    var_g: str = f"g_{str_case_indices0}__{counter}"

                    str_print: str = f"{var_g} = QQ.one()\n"

                    str_debug += str_print

                    fw_sage_series_sums.write(str_print)

                    product: SeriesProduct = tup[1]

                    is_minus: bool = product.is_minus

                    if is_minus:
                        str_print = f"{var_g} *= -1\n"

                        str_debug += str_print

                        fw_sage_series_sums.write(str_print)

                    coefficient = product.coefficient

                    if coefficient != Rational(1):
                        is_integer: bool = coefficient.denominator == 1

                        str_coefficient: str = coefficient.get_sage_str()

                        if not is_integer:
                            str_coefficient = f"({str_coefficient})"

                        str_print = f"{var_g} *= {str_coefficient}\n"

                        str_debug += str_print

                        fw_sage_series_sums.write(str_print)

                    if len(product.const_coefficients) > 0:
                        for key in product.const_coefficients.keys():
                            val: Element = product.const_coefficients[key]

                            if isinstance(val, Element):
                                for i in range(val.power):
                                    str_print = f"{var_g} *= (1-(p^(-1)))\n"

                                    str_debug += str_print

                                    fw_sage_series_sums.write(str_print)

                    for power in dict_series_product.keys():
                        start_index, rational, str_sage = dict_series_product[power]

                        str_print = f"{var_g} *= {str_sage} # {power}>={start_index}\n"

                        str_debug += str_print

                        fw_sage_series_sums.write(str_print)

                        if len(list_series_sums) > 1:
                            counter: int = tup[0]

                            str_full_case_indices: str = f"{str_case_indices}, product {counter}"

                    fw_sage_series_sums.write(f"print(f\"{var_g}={{{var_g}}} #### {str_case_indices}, [monomial {counter}/{converted_number_of_monomials}={str_monomial}]\")\n")

                    #fw_sage_series_sums.write("sf=psi(g)/g\n")
                    #fw_sage_series_sums.write(f"print(f\"sf(g[{counter}])={{sf}}\")\n")

                    fw_sage_series_sums.write(f"{var_h} += {var_g}\n")

                    if series_product_counter in dict_random_numbers:
                        list_debug_data.append(str_debug)

                fw_sage_series_sums.write(f"print(f\"{var_h}={{{var_h}}} #### {str_case_indices} [converted polynomial={str_converted_polynomial}]\")\n")

                fw_sage_series_sums.write(f"f += {var_h}\n")

            if self.print_debug:
                fw_sage_series_sums.write("print(\"########## Final Output ##########\")\n")

            #fw_sage_series_sums.write("print(f)\n")

        if isinstance(list_debug_data, list) and len(list_debug_data) > 0:
            with open(out_file_path_sage_series_sums_debug, "w") as fw_sage_series_sums_debug:
                for debug_data in list_debug_data:
                    fw_sage_series_sums_debug.write(f"{debug_data}\n")

    def write_sage_program_backup(self, dict_series_sums: dict,
                                  out_file_path_sage_series_sums: str):
        num_series_products: int = 0

        for key in dict_series_sums.keys():
            val_dict = dict_series_sums[key]

            if isinstance(val_dict, list):
                length: int = len(val_dict)

                num_series_products += length

        dict_random_numbers: dict[int, int] = {}

        num_random_numbers: int = 10

        series_product_counter: int = 0

        while len(dict_random_numbers) < num_random_numbers:
            random_number = int(random.random() * num_series_products)

            dict_random_numbers[random_number] = 0

        out_file_path_sage_series_sums_debug: str = out_file_path_sage_series_sums.replace(".txt", "_debug.txt")

        list_debug_data: list[str] = []

        with open(out_file_path_sage_series_sums, "w") as fw_sage_series_sums:
            fw_sage_series_sums.write("# Define the polynomial ring\n")
            fw_sage_series_sums.write("R.<p,t> = PolynomialRing(QQ)\n")
            fw_sage_series_sums.write("f = QQ.zero()\n")

            for str_case_indices in dict_series_sums.keys():
                list_series_sums: list[tuple[bool, SeriesProduct, dict[str, tuple[int, PolynomialRational, str]]]] = \
                dict_series_sums[
                    str_case_indices]

                fw_sage_series_sums.write(f"########## {str_case_indices}\n")

                fw_sage_series_sums.write("h = QQ.zero()\n")

                counter: int = 0

                str_debug: str = ""

                for tup in list_series_sums:
                    dict_series_product: dict[str, tuple[int, PolynomialRational, str]] = tup[2]

                    counter += 1

                    fw_sage_series_sums.write(f"##### {counter}\n")

                    str_print: str = "g = QQ.one()\n"

                    str_debug += str_print

                    fw_sage_series_sums.write(str_print)

                    product: SeriesProduct = tup[1]

                    is_minus: bool = product.is_minus

                    if is_minus:
                        str_print = "g *= -1\n"

                        str_debug += str_print

                        fw_sage_series_sums.write(str_print)

                    coefficient = product.coefficient

                    str_coefficient: str = coefficient.get_sage_str()

                    str_print = f"g *= ({str_coefficient})\n"

                    str_debug += str_print

                    fw_sage_series_sums.write(str_print)

                    if len(product.const_coefficients) > 0:
                        for key in product.const_coefficients.keys():
                            val: Element = product.const_coefficients[key]

                            if isinstance(val, Element):
                                for i in range(val.power):
                                    str_print = f"g *= (1-(p^(-1)))\n"

                                    str_debug += str_print

                                    fw_sage_series_sums.write(str_print)

                    for power in dict_series_product.keys():
                        start_index, rational = dict_series_product[power]

                        str_print = f"g *= {rational.get_sage_str()} # {power}>={start_index}\n"

                        str_debug += str_print

                        fw_sage_series_sums.write(str_print)

                        if len(list_series_sums) > 1:
                            counter: int = tup[0]

                            str_full_case_indices: str = f"{str_case_indices}, product {counter}"

                    if self.print_debug:
                        fw_sage_series_sums.write(f"print(f\"g={{g}} #### {str_full_case_indices}\")\n")

                    fw_sage_series_sums.write("h += g\n")

                    if series_product_counter in dict_random_numbers:
                        list_debug_data.append(str_debug)

                if self.print_debug:
                    fw_sage_series_sums.write(f"print(f\"h={{h}} #### {str_case_indices}\")\n")

                fw_sage_series_sums.write("f += h\n")

            if self.print_debug:
                fw_sage_series_sums.write("print(\"########## Final Output ##########\")\n")

            fw_sage_series_sums.write("print(f)\n")

        if isinstance(list_debug_data, list) and len(list_debug_data) > 0:
            with open(out_file_path_sage_series_sums_debug, "w") as fw_sage_series_sums_debug:
                for debug_data in list_debug_data:
                    fw_sage_series_sums_debug.write(f"{debug_data}\n")

    @staticmethod
    def write_case_sage_rationals(list_file_sage_rationals: list,
                                  out_file_path_sage_rationals: str,
                                  ):
        with open(out_file_path_sage_rationals, "w") as fw_file_sage:
            fw_file_sage.write("# Define the polynomial ring\n")
            fw_file_sage.write("R.<p,t> = PolynomialRing(QQ)\n")
            fw_file_sage.write("f = QQ.zero()\n")

            for sum_product in list_file_sage_rationals:
                sum_product_sage: str = sum_product.get_sage_str(with_plus_sign=False,
                                                                 with_minus_sign=False)

                sign: str = "-" if sum_product.is_minus else "+"

                fw_file_sage.write(f"f{sign}={sum_product_sage}\n")

            fw_file_sage.write("print(f)\n")

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

        rational_sum_of_all_products: PolynomialSummationRational = PolynomialSummationRational()

        list_denominators: list = []

        out_file_path_sage = os.path.join(output_full_path, "output_sage.txt")

        dict_sage_rationals: dict[str, list[PolynomialProductRational]] = {}

        dict_series_sums: dict[
            str, list[tuple[bool, SeriesProduct, dict[str, tuple[int, PolynomialRational, str]]]]] = {}

        dict_polynomials_data: dict = {}

        with (open(out_file_path_rational_sum_all, "w") as fw,
              open(out_file_path_sage, "w") as fw_sage):
            debug_write: DebugWrite = DebugWrite.get_instance(fw=fw)
            debug_write.write(ProcessFolder.file_prefix)

            dict_rationals: dict = {}

            debug_num_files: int = 0

            debug_files_counter: int = 0

            for path in input_file_paths:
                if 0 < debug_num_files <= debug_files_counter:
                    break

                out_file_path_sage_rationals: str = path.replace(".txt", "_sage_rationals.txt")

                debug_files_counter += 1

                if pattern:
                    search_result = re.search(pattern, path)

                    if search_result:
                        path = os.path.join(self.input_folder_path, path)
                        path = os.path.abspath(path)
                        print(path)
                        proc_file: ProcessFile = ProcessFile(path, output_directory=output_full_path)

                        list_file_sage_rationals: [PolynomialProductRational] = []

                        proc_file.process_file(conversion_table=self.conversion_table,
                                               reverse_conversion_table=self.reverse_conversion_table,
                                               general_debug_writer=debug_write, list_rationals=dict_rationals,
                                               total_sum=rational_sum_of_all_products,
                                               list_denominators=list_denominators,
                                               dict_sage_rationals=dict_sage_rationals,
                                               dict_series_sums=dict_series_sums,
                                               dict_polynomials_data=dict_polynomials_data)

                        out_file_path_sage_rationals = os.path.join(proc_file.output_directory_path,
                                                                    out_file_path_sage_rationals)

                        if not os.path.exists(proc_file.output_directory_path):
                            os.makedirs(proc_file.output_directory_path)

                        ProcessFolder.write_case_sage_rationals(list_file_sage_rationals,
                                                                out_file_path_sage_rationals)

            out_file_path_sage_polynomials: str = os.path.join(output_full_path, "output_sage_polynomials.txt")

            with open(out_file_path_sage_polynomials, "w") as fw_sage_polynomials:
                fw_sage_polynomials.write("var(\"v1,v2,v3,v4,a,b,c,d,p\")\n")
                for polynomial in dict_polynomials_data.keys():
                    list_: list = dict_polynomials_data[polynomial]

                    for tup in list_:
                        s: str = polynomial.get_sage_str()
                        print(s)
                        fw_sage_polynomials.write(f"f={s}\n")
                        substitution: dict[str, Polynomial] = tup[0].substitution

                        for symb in substitution.keys():
                            polynomial: Polynomial = substitution[symb]

                            symb = symb.replace("_", "")

                            str_polynomial: str = polynomial.get_sage_str()

                            fw_sage_polynomials.write(f"{symb}={str_polynomial}\n")

                        fw_sage_polynomials.write(f"print(f)\n")

            out_file_path_sage_series_sums: str = os.path.join(output_full_path, "output_sage_series_sums.txt")

            list_rational_polynomials: list = []

            for denominator in list_denominators:
                denominator_copy = copy.deepcopy(denominator)

                numerator: Polynomial = Polynomial(monoms=[Monomial(coeff=Rational(1))])

                rational_polynomial: PolynomialRational = PolynomialRational(numer=numerator, denom=denominator_copy)

                list_rational_polynomials.append(rational_polynomial)

            cases: int = 0

            for key in dict_rationals:
                l: list = dict_rationals[key]

                cases += len(l)

            Element.reverse_conversion_table = self.reverse_conversion_table

            debug_write.write("\\tiny{")

            debug_write.write(f"{rational_sum_of_all_products}")

            debug_write.write("}")

            debug_write.write("\\end{document}")

        with open(out_file_path_sage, "w") as fw_sage:
            fw_sage.write("# Define the polynomial ring\n")
            fw_sage.write("R.<p,t> = PolynomialRing(QQ)\n")
            fw_sage.write("f = QQ.zero()\n")

            str_case_indices: str = ""

            for key in dict_sage_rationals.keys():
                list_sum_products: list[PolynomialProductRational] = dict_sage_rationals[key]

                if isinstance(list_sum_products, list) and len(list_sum_products) > 0:
                    fw_sage.write(f"#{key}\n")

                    for sum_product in list_sum_products:
                        sum_product_sage: str = sum_product.get_sage_str(with_plus_sign=False,
                                                                         with_minus_sign=False)

                        sign: str = "-" if sum_product.is_minus else "+"

                        fw_sage.write(f"f{sign}={sum_product_sage}\n")

            fw_sage.write("print(f)\n")

        finished: bool = False

        index: int = 0

        take: int = 0

        self.write_sage_program(dict_series_sums=dict_series_sums,
                                out_file_path_sage_series_sums=out_file_path_sage_series_sums)

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

                total_sum_copy: PolynomialSummationRational = copy.deepcopy(rational_sum_of_all_products)

                sum_all, list_all_polynomials, dict_by_powers = total_sum_copy.multiply()

                sum_numerator: Polynomial = Polynomial(monoms=[Monomial(coeff=Rational(0))])

                for key in dict_by_powers:
                    list_monomials = dict_by_powers[key]

                    sum_monomials: Polynomial = Polynomial(monoms=[Monomial(coeff=Rational(0))])

                    monomials_counter: int = 0

                    line_monomials_counter: int = 0

                    for monomial in list_monomials:
                        monomial_copy: Monomial = copy.deepcopy(monomial)

                        if line_monomials_counter == 0:
                            fw_numerator_polynomials.write("$")
                        else:
                            fw_numerator_polynomials.write(",")

                        fw_numerator_polynomials.write(
                            f"{monomial_copy.get_ltx_str(print_sign=Monomial.Print_Sign_If_Minus)}")

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
                     list_rationals: dict, total_sum: PolynomialSummationRational,
                     list_denominators: list,
                     list_sage_rationals=None,
                     dict_sage_rationals: dict[str, list[PolynomialProductRational]] = None,
                     dict_series_sums: dict[
                         str, list[tuple[bool, SeriesProduct, dict[str, tuple[int, PolynomialRational, str]]]]] = None,
                     dict_polynomials_data: dict = None):
        if list_sage_rationals is None:
            list_sage_rationals = []
        with open(self.file_path, 'r') as file:
            file_name: str = os.path.basename(self.file_path)

            out_file_path_ltx: str = file_name.replace(".txt", ".tex")

            if not os.path.exists(self.output_directory_path):
                os.makedirs(self.output_directory_path)

            out_file_path_ltx = os.path.join(self.output_directory_path, out_file_path_ltx)

            out_file_path_sage = out_file_path_ltx.replace(".tex", "_sage.txt")

            with open(out_file_path_ltx, "w") as fw_ltx, open(out_file_path_sage, "w") as fw_sage:
                debug_write_ltx: DebugWrite = DebugWrite.get_instance(fw=fw_ltx)
                debug_write_sage: DebugWrite = DebugWrite.get_instance(fw=fw_sage)
                debug_write_ltx.write(r"""
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
                                          general_debug_writer=general_debug_writer,
                                          list_rationals=list_rationals,
                                          total_sum=total_sum,
                                          list_denominators=list_denominators,
                                          debug_write_ltx=debug_write_ltx,
                                          debug_write_sage=debug_write_sage,
                                          dict_sage_rationals=dict_sage_rationals,
                                          dict_series_sums=dict_series_sums,
                                          dict_polynomials_data=dict_polynomials_data)

                for key in conversion_table.keys():
                    index: int = conversion_table[key]

                    s: str = f"x_{index}"

                    s = f"\\[{s}\\rightarrow{{p^{{{key[0]}}}t^{{{key[1]}}}}}\\]"

                    debug_write_ltx.write(s)

                debug_write_ltx.write("\\end{document}")

    def process_line(self, text: str, conversion_table: dict,
                     reverse_conversion_table: dict,
                     general_debug_writer: DebugWrite,
                     list_rationals: dict,
                     total_sum: PolynomialSummationRational,
                     list_denominators: list,
                     debug_write_ltx: DebugWrite,
                     debug_write_sage: DebugWrite,
                     dict_sage_rationals: dict[str, list[PolynomialProductRational]] = None,
                     dict_series_sums: dict[
                         str, tuple[bool, list[dict[str, tuple[str, PolynomialRational, str]]]]] = None,
                     dict_polynomials_data: dict = None):
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

        prefix = "substitution: "

        if text.startswith(prefix):
            text = text[len(prefix):]

            if text:
                text = text.strip()

            if text:
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

            str_to_print: str = f"\r\n{str_case_indices}\r\n"

            debug_write_ltx.write(str_to_print)
            debug_write_ltx.write(str_to_print)

            if general_debug_writer is not None:
                general_debug_writer.write(f"\n{str_case_indices}\n")

            for polynomial in self.polynomials:
                if polynomial not in dict_polynomials_data:
                    dict_polynomials_data[polynomial] = []

                list_ = dict_polynomials_data[polynomial]

                polynomial_data: tuple = self.substitution, self.start_index

                list_.append(polynomial_data)

                debug_write_ltx.write(f"\\[{polynomial.get_ltx_str()}\\]\r\n", 1)

                debug_write_sage.write(f"{polynomial.get_sage_str()}\r\n", 1)

                self.substitution_counter += 1

                str_to_print = f"Substitution no. {self.substitution_counter}\r\n"

                debug_write_ltx.write(str_to_print)
                debug_write_sage.write(str_to_print)

                debug_write_ltx.write(f"\\[{self.substitution.get_ltx_str()}\\]")

                debug_write_sage.write(f"{self.substitution.get_sage_str()}\r\n")

                converted_polynomial: Polynomial = self.substitution.substitude_polynomial(polynomial)

                debug_write_ltx.write(f"\\[{converted_polynomial.get_ltx_str()}\\]\r\n", 1)

                debug_write_sage.write(f"{converted_polynomial.get_sage_str()}\r\n", 1)

                converted_pt_product: ExponentialProduct = self.substitution.substitude_exponential_product(
                    self.pt_product)

                series_product = SeriesProduct.from_exponential_product(converted_pt_product,
                                                                        conversion_table,
                                                                        reverse_conversion_table)

                if isinstance(series_product, SeriesProduct) and isinstance(self.start_index, dict) and len(
                        self.start_index) > 0:
                    for key in self.start_index.keys():
                        if key:
                            val: int = self.start_index[key]

                            if isinstance(val, int):
                                series_product.add_start_index(key, val)

                list_series_products: list[SeriesProduct] = series_product.multiply_by_polynomial(converted_polynomial)

                sum_item: PolynomialSummationRational = PolynomialSummationRational()

                str_to_print = "All series and their sums\r\n"

                debug_write_ltx.write(str_to_print)
                debug_write_sage.write(str_to_print)

                counter: int = 0

                for ser_prod in list_series_products:
                    counter += 1
                    ser_prod_copy = copy.deepcopy(ser_prod)

                    sum_product: PolynomialProductRational = ser_prod_copy.sum(dict_series_sums=dict_series_sums,
                                                                               str_case_indices=str_case_indices,
                                                                               counter=counter, original_polynomial=polynomial,
                                                                               converted_polynomial=converted_polynomial,
                                                                               substitution=self.substitution)

                    numerator: PolynomialProduct = sum_product.numerator

                    str_to_print = f"\\[{ser_prod.get_ltx_str()}={sum_product.get_ltx_str()}\\]"

                    debug_write_ltx.write("\r\nBefore Conversion\r\n", 1)

                    debug_write_ltx.write(str_to_print, 1)

                    sum_product_sage: str = sum_product.get_sage_str()

                    str_to_print = f"\\[{ser_prod.get_ltx_str()}\\]={sum_product_sage}"

                    debug_write_sage.write("\r\nBefore Conversion\r\n", 1)

                    debug_write_sage.write(str_to_print, 1)

                    numerator.convert_constant_coefficients()

                    str_to_print = f"\\[{ser_prod}={sum_product}\\]"

                    debug_write_ltx.write("\r\nAfter Conversion\r\n", 1)

                    debug_write_ltx.write(str_to_print, 1)

                    sum_product_sage = sum_product.get_sage_str()

                    str_to_print = f"\\[{ser_prod.get_ltx_str()}\\]={sum_product_sage}"

                    debug_write_sage.write("\r\nAfter Conversion\r\n", 1)

                    debug_write_sage.write(str_to_print, 1)

                    if isinstance(dict_sage_rationals, dict):
                        if str_case_indices not in dict_sage_rationals:
                            dict_sage_rationals[str_case_indices] = []

                        list_sage_rationals: list[PolynomialProductRational] = dict_sage_rationals[str_case_indices]

                        if isinstance(list_sage_rationals, list):
                            list_sage_rationals.append(sum_product)

                    sum_product_copy: PolynomialProductRational = copy.deepcopy(sum_product)
                    sum_product_copy_2: PolynomialProductRational = copy.deepcopy(sum_product)

                    if debug_write_ltx is not None:
                        sum_item.add_polynomial_rational(sum_product_copy)

                    total_sum.add_polynomial_rational(sum_product_copy_2)

                str_to_print = "\r\nItem Sum\r\n"

                debug_write_ltx.write(str_to_print)
                debug_write_sage.write(str_to_print)

                denominator0 = copy.deepcopy(sum_item.denominator)

                list_denominators.append(denominator0)

                if debug_write_ltx is not None:
                    str_to_print = f"{sum_item.get_ltx_str()}"
                    debug_write_ltx.write(str_to_print)

                    str_to_print = f"{sum_item.get_sage_str()}"
                    debug_write_sage.write(str_to_print)

                    if general_debug_writer is not None:
                        general_debug_writer.write(str_to_print)

                    sum_item_copy = copy.deepcopy(sum_item)

                    sum_polynomials, list_polynomials, dict_monomials_by_powers = sum_item_copy.multiply()

                    if general_debug_writer is not None:
                        general_debug_writer.write(str_to_print)

                    str_to_print = "Polynomial sums\r\n"

                    debug_write_ltx.write(str_to_print)
                    debug_write_sage.write(str_to_print)

                    index: int = 0

                    for tup in list_polynomials:
                        index += 1
                        str_to_print = f"Polynomial {index}\r\n\r\n\\[{tup[0]}=\\]\\[={tup[1]}\\]"
                        debug_write_ltx.write(str_to_print)

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
                                    _ = 0  # debug

                            indices[ind] = pol.power

        list_indices: list[int] = sorted(indices.keys())

        list0: list[str] = [""] * len(list_indices)

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
