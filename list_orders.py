import re


def list_orders(file_path: str) -> list[tuple[list[int], list[bool]]]:
    list_orders: list[
        tuple[tuple[list[int], list[bool]],str]
        ] = []

    with open(file_path, "r") as f:
        for line in f:
            line0: str = str(line)

            line = line.strip()

            if re.search(r'\(.*\)$', line):
                continue

            if line.startswith(r"\item"):
                continue

            line = line.replace("{", "").replace("}", "").replace(r"\item", "").replace(r"$", "")

            line = re.sub(r'\\overset[abcde]', '', line)

            if line:
                line = line.strip()

            arr: list[str] = re.split(r'\\geq|>', line)

            arr = [s.strip() for s in arr if s.startswith("v_")]

            if isinstance(arr, list) and len(arr) > 3:
                index: int = 0

                list_vars: list[list[int]] = []
                list_rels: list[bool] = []

                while line:
                    if re.search(r'^v_[1234]', line):
                        list_index: list[int] = []

                        str_var: str = line[0:3]

                        str_num: str = str_var[2]

                        if str_num and str_num.isnumeric:
                            list_index.append(int(str_num))

                        line = line[3:]

                        if line[0] == "+":
                            line = line[1:]
                            str_var: str = line[0:3]

                            str_num: str = str_var[2]

                            if str_num and str_num.isnumeric:
                                list_index.append(int(str_num))
                            
                            line = line[3:]

                        if len(list_index) > 0:
                            list_vars.append(list_index)
                    elif line.startswith(">"):
                        line = line[1:]
                        list_rels.append(True)
                    elif line.startswith(r"\geq"):
                        line = line[len(r"\geq"):]
                        list_rels.append(False)
                    else:
                        line = line[1:]

                order: tuple[list[int], list[bool]] = list_vars, list_rels
                
                found: bool = False
                index: int = 0

                while not found and index < len(list_orders):
                    existing_order = list_orders[index][0]

                    inner_index: int = 0
                    different: bool = False

                    while not different and inner_index < len(order[0]):
                        list_vars = sorted(order[0][inner_index])
                        existing_list_vars = sorted(existing_order[0][inner_index])

                        if len(list_vars) != len(existing_list_vars):
                            different = True

                        list_vars_index: int = 0

                        while not different and list_vars_index < len(list_vars):
                            if list_vars[list_vars_index] != existing_list_vars[list_vars_index]:
                                different = True

                            list_vars_index += 1

                        if not different and inner_index < len(order[1]):
                            rel = order[1][inner_index]
                            existing_rel = existing_order[1][inner_index]
                            if rel != existing_rel:
                                different = True

                        inner_index += 1

                    if not different:
                        found = True

                    index += 1

                if not found:
                    list_orders.append((order, line0))

                #str_order: str = print_order(order)

                #print(str_order)

        for i in range(len(list_orders)):
            order = list_orders[i][0]
            line0 = list_orders[i][1]

            str_order: str = print_order(order)

            print(f"Order {i+1}: {str_order}, {line0}")
    return list_orders

def print_order(order: tuple[list[int], list[bool]]):
    list_vars, list_rels = order

    list_strs: list[str] = []

    for i in range(len(list_vars)):
        list_index = list_vars[i]
        str_vars: str = "+".join([f"v_{index}" for index in list_index])

        list_strs.append(str_vars)

        list_strs.append(">" if list_rels[i] else ">=")

    return " ".join(list_strs)

def find_vector(orders: list[
    tuple[tuple[list[int], list[bool]], str]
    ], vector: list[int]) -> bool:
    list_orders: list[tuple[list[int], list[bool]]] = []
    
    for order in orders:
        if check_vector(order[0], vector):
            list_orders.append(order[0])

    return list_orders

def check_vector(order: tuple[list[int], list[bool]], vector: list[int]) -> bool:
    list_vars, list_rels = order

    index: int = 1

    var_index: int = list_vars[len(list_vars) - index][0]

    var_value: int = vector[var_index - 1]

    dict_var_values: dict[int, int] = {}

    dict_var_values[var_index] = var_value

    rel_of_two_vars: bool = False

    while index <= (len(list_vars) - 1):
        rel = list_rels[len(list_rels) - index - 1]

        #rel0 = rel or rel_of_two_vars

        rel_of_two_vars = False

        list_var_indices: list[int] = list_vars[len(list_vars) - index - 1]

        var_value_next: int = 0

        if len(list_var_indices) > 1:
            var_value_next = dict_var_values[list_var_indices[0]] + dict_var_values[list_var_indices[1]]

            if var_value_next < var_value:
                return False
            
            if var_value_next == var_value and rel:
                return False
        else:
            var_index_next: int = list_var_indices[0]

            var_value_next: int = vector[var_index_next - 1]

            dict_var_values[var_index_next] = var_value_next

            if var_value_next < var_value:
                return False

            if var_value_next == var_value and rel:
                return False
        
        var_value = var_value_next
            
        index += 1

    return True