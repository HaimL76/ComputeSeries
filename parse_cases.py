import re


def parse_cases(file_path):
    str_subs_pattern: str = r"(\$v_\d\\rightarrow{([\d]*[abcd][+-])*[\d]*[abcd]}\$)"

    section_counter: int = 0
    subsection_counter: int = 0
    item_counter: int = 0

    dict_subs: dict[int, str] = {}

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

            if line.startswith("\\end{enumerate}"):
                item_counter = 0  # Reset item counter at the end of an enumerate environment

            if line.startswith("\\item"):
                item_counter += 1

            occurrences: list[str] = re.findall(str_subs_pattern, line)  # , "gm"):

            if isinstance(occurrences, list) and len(occurrences) > 0:
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

                # print(f"{section_counter}.{subsection_counter}.{item_counter}, {line}")
