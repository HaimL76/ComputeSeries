import re


def parse_cases(file_path):
    str_subs_pattern: str = r"(\$v_\d\\rightarrow{([\d]*[abcd][+-])*[\d]*[abcd]}\$)"
    str_starting_index_pattern: str = r"(([abcd],)*[abcd]\\geq\{[01]\})"

    section_counter: int = 0
    subsection_counter: int = 0
    item_counter: int = 0

    dict_subs: dict[int, str] = {}
    dict_start_indices: dict[str, int] = {}

    cases = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            if line.startswith("\\section{Case"):
                section_counter += 1

                subsection_counter = 0  # Reset subsection counter for new section
                item_counter = 0  # Reset item counter for new section

            if line.startswith("\\subsection{Sub"):
                subsection_counter += 1

                item_counter = 0  # Reset item counter for new subsection

            if line.startswith("\\begin{enumerate}"):
                item_counter = 0  # Reset item counter at the beginning of an enumerate environment

            if line.startswith("\\end{enumerate}"):
                item_counter = 0  # Reset item counter at the end of an enumerate environment

            if line.startswith("\\item"):
                item_counter += 1

            occurrences: list[str] = re.findall(str_subs_pattern, line)

            if isinstance(occurrences, list) and len(occurrences) > 0:
                if len(dict_subs) == 4:
                    for key in dict_subs.keys():
                        list_of_1_indices: list[str] = [key for key, value in dict_start_indices.items() if value == 1]

                        str_starting_index: str = ",".join(f"{str_index}" for str_index in list_of_1_indices)

                        print(f"{str_indices}: {dict_subs[key]}, {str_starting_index}")

                    dict_subs.clear()
                    dict_start_indices.clear()

                for occ in occurrences:
                    str_subs: str = occ[0]

                    match = re.search(r"(\$v_\d)", str_subs)

                    groups = match.groups()

                    if len(groups) > 0:
                        prefix: str = groups[0]

                        second_part: str = str_subs[len(prefix):-1]  # remove $ at the end

                        second_part = second_part[len("\\rightarrow"):]  # remove \\rightarrow

                        second_part = second_part[1:-1]  # remove { and }

                        arr = prefix.split("_")

                        if isinstance(arr, list) and len(arr) == 2:
                            str_index: str = arr[1]

                            if isinstance(str_index, str) and str_index.isnumeric():
                                index: int = int(str_index)

                                dict_subs[index] = str_subs

                                if len(dict_subs) == 4:
                                    str_indices = f"{section_counter}"

                                    if subsection_counter > 0:
                                        str_indices = f"{str_indices}.{section_counter}"

                                    if item_counter > 0:
                                        str_indices = f"{str_indices}.{item_counter}"

            starting_indices: list[str] = re.findall(str_starting_index_pattern, line)

            if isinstance(starting_indices, list) and len(starting_indices) > 0:
                for tuple_start_index in starting_indices:
                    str_start_index: str = tuple_start_index[0]
                    match = re.search(r"(([abcd],)*[abcd])", str_start_index)

                    groups = match.groups()

                    str_starting_indices: str = groups[0]

                    str_index: str = str_start_index[len(str_starting_indices):]

                    str_index = str_index[len("\\geq"):] # remove \\geq

                    str_index = str_index[1:-1] # remove { and }

                    if isinstance(str_index, str) and str_index.isnumeric():
                        arr_indices = str_starting_indices.split(',')

                        for start_index in arr_indices:
                            dict_start_indices[start_index] = int(str_index)


                # print(f"{section_counter}.{subsection_counter}.{item_counter}, {line}")
