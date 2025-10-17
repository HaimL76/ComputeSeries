import os
import re


class InformationCollection:
    def __init__(self):
        self.dict_subst: dict[str, str] = {}
        self.dict_start_indices: dict[str, int] = {}
        self.section_counter: int = 0
        self.subsection_counter: int = 0
        self.item_counter: int = 0

def get_str_indices(information_collection: InformationCollection) -> tuple[str, str]:
    str_indices = f"{information_collection.section_counter}"
    str_indices_file: str = str_indices

    if information_collection.subsection_counter > 0:
        str_indices = f"{str_indices}.{information_collection.subsection_counter}"
        str_indices_file = str_indices

    if information_collection.item_counter > 0:
        str_indices = f"{str_indices}.{information_collection.item_counter}"

    return str_indices_file, str_indices


def finish_collecting_case_information(information_collection: InformationCollection, input_folder: str):
    if len(information_collection.dict_subst) == 4:
        str_indices_file, str_indices = get_str_indices(information_collection=information_collection)

        for key_subst in information_collection.dict_subst.keys():
            list_of_1_indices: list[str] = [key for key, value in information_collection.dict_start_indices.items() if value == 1]

            str_starting_index: str = ",".join(f"{str_index}" for str_index in list_of_1_indices)

            val_subst: str = information_collection.dict_subst[key_subst]

            print(f"{str_indices}: {key_subst}->{val_subst}, {str_starting_index}")

        information_collection.dict_subst.clear()
        information_collection.dict_start_indices.clear()


def parse_cases(file_path, input_folder: str):
    list_files: list[str] = os.listdir(input_folder)

    if isinstance(list_files, list) and len(list_files) > 0:
        list_error_files: list[str] = [os.path.join(input_folder, file_path) for file_path in list_files if file_path.endswith(".err.txt")]

        if isinstance(list_error_files, list) and len(list_error_files) > 0:
            for error_file in list_error_files:
                os.remove(error_file)

    dict_output: dict[str, (dict[int, str], dict[str, int], str)] = {}

    str_subs_pattern: str = r"(\$v_\d\\rightarrow{([\d]*[abcd][+-])*[\d]*[abcd]}\$)"
    str_starting_index_pattern: str = r"(([abcd],)*[abcd]\\geq\{[01]\})"

    information_collection: InformationCollection = InformationCollection()

    information_collection.section_counter = 0
    information_collection.subsection_counter = 0
    information_collection.item_counter = 0

    information_collection.dict_subst = {}
    information_collection.dict_start_indices = {}

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            if line.startswith("\\section{Case"):
                finish_collecting_case_information(information_collection=information_collection, input_folder=input_folder)

                information_collection.section_counter += 1

                information_collection.subsection_counter = 0  # Reset subsection counter for new section
                information_collection.item_counter = 0  # Reset item counter for new section

            if line.startswith("\\subsection{Sub"):
                finish_collecting_case_information(information_collection=information_collection, input_folder=input_folder)

                information_collection.subsection_counter += 1

                information_collection.item_counter = 0  # Reset item counter for new subsection

            if line.startswith("\\begin{enumerate}") or line.startswith("\\end{enumerate}"):
                finish_collecting_case_information(information_collection=information_collection, input_folder=input_folder)

                information_collection.item_counter = 0

            if line.startswith("\\item"):
                finish_collecting_case_information(information_collection=information_collection, input_folder=input_folder)
                information_collection.item_counter += 1

            occurrences: list[str] = re.findall(str_subs_pattern, line)

            if isinstance(occurrences, list) and len(occurrences) > 0:
                for occ in occurrences:
                    str_subs: str = occ[0]

                    match = re.search(r"(\$v_\d)", str_subs)

                    groups = match.groups()

                    if len(groups) > 0:
                        prefix: str = groups[0]

                        key: str = prefix[1:] # remove $ at the beginning

                        second_part: str = str_subs[len(prefix):-1]  # remove $ at the end

                        second_part = second_part[len("\\rightarrow"):]  # remove \\rightarrow

                        second_part = second_part[1:-1]  # remove { and }

                        #finish_collecting_case_information(information_collection=information_collection, input_folder=input_folder)

                        information_collection.dict_subst[key] = second_part

                        str_indices_file, str_indices = get_str_indices(information_collection=information_collection)

                        if str_indices_file not in dict_output:
                            dict_output[str_indices_file] = {}

                        inner_dict = dict_output[str_indices_file]

                        if str_indices not in inner_dict:
                            inner_dict[str_indices] = ({}, {}, str_indices_file)

                        tup: tuple[dict[str, str], dict[str, int]] = inner_dict[str_indices]

                        dict_subst: dict[str, str] = tup[0]

                        dict_subst[key] = second_part

            starting_indices: list[str] = re.findall(str_starting_index_pattern, line)

            if isinstance(starting_indices, list) and len(starting_indices) > 0:
                for tuple_start_index in starting_indices:
                    str_start_index: str = tuple_start_index[0]
                    match = re.search(r"(([abcd],)*[abcd])", str_start_index)

                    groups = match.groups()

                    str_starting_indices: str = groups[0]

                    str_index: str = str_start_index[len(str_starting_indices):]

                    str_index = str_index[len("\\geq"):]  # remove \\geq

                    str_index = str_index[1:-1]  # remove { and }

                    if isinstance(str_index, str) and str_index.isnumeric():
                        arr_indices = str_starting_indices.split(',')

                        for str_start_index in arr_indices:
                            information_collection.dict_start_indices[str_start_index] = int(str_index)

                            if str_indices_file not in dict_output:
                                dict_output[str_indices_file] = {}

                            inner_dict = dict_output[str_indices_file]

                            if str_indices not in inner_dict:
                                inner_dict[str_indices] = ({}, {}, str_indices_file)

                            tup: tuple[dict[str, str], dict[str, int]] = inner_dict[str_indices]

                            dict_start_indices: dict[str, int] = tup[1]

                            dict_start_indices[str_start_index] = int(str_index)

    check_input_files(input_folder=input_folder, dict_output=dict_output)

def add_error_line(dict_errors: dict[str, list[str]], file_path: str, line: str):
    if file_path not in dict_errors:
        dict_errors[file_path] = []

    dict_errors[file_path].append(line)

def check_input_files(input_folder: str, dict_output: dict[str,dict[str, (dict[str, str], dict[str, int])]]):
    dict_input: dict[str, (dict[int, str], dict[str, int], str)] = {}

    list_files = os.listdir(input_folder)

    if isinstance(list_files, list) and len(list_files) > 0:
        for file_path in list_files:
            str_indices_file: str = file_path.replace(".txt", "")

            file_path = os.path.join(input_folder, file_path)
            with open(file_path, 'r') as file:
                str_indices_in_file: str = ""
                dict_error_lines: dict[str, list[str]] = {}

                pattern_indices: str = "^=+\\s*(\\d+\\.)*\\d+\\s*=+$"

                for num, line in enumerate(file):
                    line = line.strip()
                    if re.search(pattern=pattern_indices, string=line):
                        str_indices_in_file = line.replace("=", "").strip()

                    if "substitution:" in line:
                        subst = line.replace("substitution:", "").strip()

                        arr: list[str] = subst.split("=")

                        if isinstance(arr, list) and len(arr) == 2:
                            key_subst: str = arr[0].strip()
                            val_subst: str = arr[1].strip()

                        if str_indices_file not in dict_input:
                            dict_input[str_indices_file] = {}

                        inner_dict = dict_input[str_indices_file]

                        if str_indices_in_file not in inner_dict:
                            inner_dict[str_indices_in_file] = ({}, {}, str_indices_file)

                        tup: tuple[dict[str, str], dict[str, int]] = inner_dict[str_indices_in_file]

                        dict_subst: dict[str, str] = tup[0]

                        dict_subst[key_subst] = val_subst

                    if "indices:" in line:
                        str_ind = line.replace("indices:", "").strip()

                        arr: list[str] = str_ind.split(",")

                        if isinstance(arr, list) and len(arr) > 0:
                            for ind in arr:
                                ind = ind.strip()

                                if ind:
                                    if str_indices_file not in dict_input:
                                        dict_input[str_indices_file] = {}

                                    inner_dict = dict_input[str_indices_file]

                                    if str_indices_in_file not in inner_dict:
                                        inner_dict[str_indices_in_file] = ({}, {}, str_indices_file)

                                    tup: tuple[dict[str, str], dict[str, int]] = inner_dict[str_indices_in_file]

                                    dict_starting_indices: dict[str, int] = tup[1]

                                    dict_starting_indices[ind] = 1

    compare_dictionaries(dict_input, dict_output, dict_error_lines)
    compare_dictionaries(dict_output, dict_input, dict_error_lines)

    if len(dict_error_lines) > 0:
        for key in dict_error_lines.keys():
            list_error_lines: list[str] = dict_error_lines[key]

            if isinstance(list_error_lines, list) and len(list_error_lines) > 0:
                error_file_path = os.path.join(input_folder, f"{key}.err.txt")
                with open(error_file_path, 'w') as ef:
                    for error in list_error_lines:
                        ef.write(f"{error}\r\n")

def compare_dictionaries(dict_input: dict[str,dict[str, (dict[str, str], dict[str, int])]],
                         dict_output: dict[str, (dict[str, str], dict[str, int], str)],
                         dict_error_lines: dict[str, list[str]]):
    if len(dict_output) > 0:
        for str_indices_in_file in dict_output.keys():
            inner_dict_output = dict_output[str_indices_in_file]

            for str_indices in inner_dict_output.keys():
                tup_output: tuple[dict[str, str], dict[str, int], str] = inner_dict_output[str_indices]

                dict_subst_output: dict[str, str] = tup_output[0]

                str_indices_file: str = tup_output[2]

                for key_subst in dict_subst_output.keys():
                    val_subst_output: str = dict_subst_output[key_subst]

                    if str_indices_in_file not in dict_input:
                        add_error_line(dict_error_lines, str_indices_file, f"{str_indices} not found")
                    else:
                        inner_dict_input = dict_input[str_indices_in_file]

                        if str_indices not in inner_dict_input:
                            add_error_line(dict_error_lines, str_indices_file, f"{str_indices} not found in {str_indices}")
                        else:
                            tup_input: tuple[dict[str, str], dict[str, int]] = inner_dict_input[str_indices]

                            dict_subst_input: dict[str, str] = tup_input[0]

                            if key_subst not in dict_subst_input:
                                add_error_line(dict_error_lines, str_indices_file, f"{key_subst} not found in {str_indices}")
                            else:
                                val_from_dict_input: str = dict_subst_input[key_subst]

                                val_from_dict_input = val_from_dict_input.replace(".", "")
                                val_subst_output = val_subst_output.replace(".", "")

                                if val_from_dict_input != val_subst_output:
                                    add_error_line(dict_error_lines, str_indices_file, f"{key_subst} should be {val_subst_output} in {str_indices}")

                dict_starting_indices_output: dict[str, int] = tup_output[1]

                for ind in dict_starting_indices_output.keys():
                    int_index_output: int = dict_starting_indices_output[ind]

                    if str_indices_in_file not in dict_input:
                        add_error_line(dict_error_lines, str_indices_file, f"{str_indices_in_file} not found")
                    else:
                        inner_dict_input = dict_input[str_indices_in_file]

                        if str_indices not in inner_dict_input:
                            add_error_line(dict_error_lines, str_indices_file, f"{str_indices} not found in {str_indices}")
                        else:
                            tup: tuple[dict[str, str], dict[str, int]] = inner_dict_input[str_indices]

                            dict_starting_indices_input: dict[str, int] = tup[1]

                            if ind not in dict_starting_indices_input:
                                if int_index_output == 1:
                                    add_error_line(dict_error_lines, str_indices_file, f"{ind} not found in {str_indices}")
                            else:
                                int_index_input: int = dict_starting_indices_input[ind]

                                if int_index_output != int_index_input:
                                    add_error_line(dict_error_lines, str_indices_file, f"{ind} should be {int_index_output} in {str_indices})")

