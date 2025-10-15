import re


class InformationCollection:
    def __init__(self):
        self.dict_subs: dict[int, str] = {}
        self.dict_start_indices: dict[str, int] = {}
        self.section_counter: int = 0
        self.subsection_counter: int = 0
        self.item_counter: int = 0


def finish_collecting_case_information(information_collection: InformationCollection):
    if len(information_collection.dict_subs) == 4:
        str_indices = f"{information_collection.section_counter}"

        if information_collection.subsection_counter > 0:
            str_indices = f"{str_indices}.{information_collection.subsection_counter}"

        if information_collection.item_counter > 0:
            str_indices = f"{str_indices}.{information_collection.item_counter}"

        for key_subst in information_collection.dict_subs.keys():
            list_of_1_indices: list[str] = [key for key, value in information_collection.dict_start_indices.items() if value == 1]

            str_starting_index: str = ",".join(f"{str_index}" for str_index in list_of_1_indices)

            val_subst: str = information_collection.dict_subs[key_subst]

            print(f"{str_indices}: v_{key_subst}->{val_subst}, {str_starting_index}")

        information_collection.dict_subs.clear()
        information_collection.dict_start_indices.clear()


def parse_cases(file_path):
    str_subs_pattern: str = r"(\$v_\d\\rightarrow{([\d]*[abcd][+-])*[\d]*[abcd]}\$)"
    str_starting_index_pattern: str = r"(([abcd],)*[abcd]\\geq\{[01]\})"

    information_collection: InformationCollection = InformationCollection()

    information_collection.section_counter = 0
    information_collection.subsection_counter = 0
    information_collection.item_counter = 0

    information_collection.dict_subs = {}
    information_collection.dict_start_indices = {}

    cases = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            if line.startswith("\\section{Case"):
                finish_collecting_case_information(information_collection=information_collection)

                information_collection.section_counter += 1

                information_collection.subsection_counter = 0  # Reset subsection counter for new section
                information_collection.item_counter = 0  # Reset item counter for new section

            if line.startswith("\\subsection{Sub"):
                finish_collecting_case_information(information_collection=information_collection)

                information_collection.subsection_counter += 1

                information_collection.item_counter = 0  # Reset item counter for new subsection

            if line.startswith("\\begin{enumerate}") or line.startswith("\\end{enumerate}"):
                finish_collecting_case_information(information_collection=information_collection)

                information_collection.item_counter = 0

            if line.startswith("\\item"):
                finish_collecting_case_information(information_collection=information_collection)
                information_collection.item_counter += 1

            occurrences: list[str] = re.findall(str_subs_pattern, line)

            if isinstance(occurrences, list) and len(occurrences) > 0:
                for occ in occurrences:
                    str_subs: str = occ[0]

                    match = re.search(r"(\$v_\d)", str_subs)

                    groups = match.groups()

                    if len(groups) > 0:
                        prefix: str = groups[0]

                        arr = prefix.split("_")

                        if isinstance(arr, list) and len(arr) == 2:
                            str_index: str = arr[1]

                            if isinstance(str_index, str) and str_index.isnumeric():
                                index: int = int(str_index)

                                second_part: str = str_subs[len(prefix):-1]  # remove $ at the end

                                second_part = second_part[len("\\rightarrow"):]  # remove \\rightarrow

                                second_part = second_part[1:-1]  # remove { and }

                                #finish_collecting_case_information(information_collection=information_collection)

                                information_collection.dict_subs[index] = second_part

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

                        for start_index in arr_indices:
                            information_collection.dict_start_indices[start_index] = int(str_index)

        #finish_collecting_case_information(information_collection=information_collection)
