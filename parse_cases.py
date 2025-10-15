def parse_cases(file_path):
    cases = []
    with open(file_path, 'r') as file:
        section_counter: int = 0
        subsection_counter: int = 0
        item_counter: int = 0
        for line in file:
            line = line.strip()

            if line.startswith("\\section{Case"):
                section_counter += 1

                subsection_counter = 0 # Reset subsection counter for new section
                item_counter = 0 # Reset item counter for new section

            if line.startswith("\\subsection{Sub"):
                subsection_counter += 1

                item_counter = 0 # Reset item counter for new subsection

            if line.startswith("\\end{enumerate}"):
                item_counter = 0 # Reset item counter at the end of an enumerate environment

            if line.startswith("\\item"):
                item_counter += 1

                print(f"{section_counter}.{subsection_counter}.{item_counter}")

