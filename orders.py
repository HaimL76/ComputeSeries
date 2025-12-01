import re
from functools import cmp_to_key

from stack import Stack


def convert_order_to_str(order: list[str]):
    str0: str = ""  # .join([str(obj) for obj in stack])

    for obj in order:
        str_element: str = str(obj)

        if isinstance(obj, int):
            str_element: str = f"v_{obj}"

        if str_element == r"\geq":
            str_element = ">="

        if str0:
            str0 = f"{str0} "

        str0 = f"{str0}{str_element}"

    return str0


def convert_line_to_str(line: list[str]):
    str1: str = ""

    for element in line:
        str_element: str = element

        if str_element == r"\geq":
            str_element = ">="

        if str1:
            str1 = f"{str1} "

        str1 = f"{str1}{str_element}"

    return str1


def build_order(symbols: list[str], index: int, stack: Stack, list_strs: list[(list, list)],
                list_original: list[str]):
    if index >= len(symbols):
        tup: tuple = list(stack), list_original

        list_strs.append(tup)
    else:
        symbol: str = symbols[index]

        arr: list[str] = symbol.split("_")

        if isinstance(arr, list) and len(arr) == 2 and arr[1].isnumeric():
            var_index: int = int(arr[1])

            stack.push(var_index)
            build_order(symbols, index + 1, stack=stack, list_strs=list_strs,
                        list_original=list_original)
            _ = stack.pop()

        elif symbol == r"\geq" and index < len(symbols) - 2:
            stack.push(">")
            build_order(symbols, index + 1, stack=stack, list_strs=list_strs,
                        list_original=list_original)
            _ = stack.pop()

            stack.push("=")
            build_order(symbols, index + 1, stack=stack, list_strs=list_strs,
                        list_original=list_original)
            _ = stack.pop()

        else:
            stack.push(symbol)
            build_order(symbols, index + 1, stack=stack, list_strs=list_strs,
                        list_original=list_original)
            _ = stack.pop()


def check_covering():
    list_strs: list[str] = []

    check_all_orders(0, Stack(), lisr_strs=list_strs)

    counter: int = 0

    for str0 in list_strs:
        print(f"order[{counter}]: {str0}")
        counter += 1
    #return
    dict_order: dict = {}

    regex_overset: str = r"\\overset\{[a-z]\}"
    regex_var: str = r"v_\d"
    regex_var_start: str = rf"^{regex_var}"

    regex_geq: str = r"\\geq"
    regex_geq_start: str = rf"^{regex_geq}"

    arr_order: list[list[tuple]] = []

    list_strs: list[(str, str)] = []

    list_symbols: list[list[str]] = []

    with open(".\\input\\cases.tex") as fr:
        for line in fr:
            line0: str = line
            list_vars: list = []

            while len(line) > 0:
                offset: int = 1

                finds = re.findall(regex_var_start, line)

                if isinstance(finds, list) and len(finds) > 0:
                    str_var: str = finds[0]

                    offset = len(str_var)

                    list_vars.append(str_var)
                else:
                    str0: str = line[:1]

                    if str0 in [">", "<", "+", "0"]:
                        list_vars.append(str0)
                    else:
                        finds = re.findall(regex_geq_start, line)

                        if isinstance(finds, list) and len(finds) > 0:
                            str_geq: str = finds[0]

                            offset = len(str_geq)

                            list_vars.append(str_geq)

                line: str = line[offset:]

            list_vars0: list[str] = []

            list_vars_original: list[str] = list_vars

            for index in range(len(list_vars)):
                prev_symbol: str = ""
                next_symbol: str = ""
                curr_symbol: str = list_vars[index]

                if index > 0:
                    prev_symbol = list_vars[index - 1]

                if index < (len(list_vars) - 1):
                    next_symbol = list_vars[index + 1]

                sum_of_vars: bool = "+" in [prev_symbol, curr_symbol, next_symbol]

                if not sum_of_vars:
                    list_vars0.append(curr_symbol)

            list_vars0 = list_vars

            cleaned_doubles: bool = False

            while not cleaned_doubles:
                list_vars = list_vars0
                list_vars0 = []

                doubles_counter: int = 0

                for index in range(len(list_vars)):
                    prev_symbol: str = ""
                    curr_symbol: str = list_vars[index]

                    if index > 0:
                        prev_symbol = list_vars[index - 1]

                    double_found: bool = curr_symbol == prev_symbol

                    if double_found:
                        doubles_counter += 1

                    if not double_found:
                        list_vars0.append(curr_symbol)

                if doubles_counter < 1:
                    cleaned_doubles = True

            list_vars = list_vars0
            list_vars0 = []

            for index in range(len(list_vars)):
                prev_symbol: str = ""
                next_symbol: str = ""
                curr_symbol: str = list_vars[index]

                if index > 0:
                    prev_symbol = list_vars[index - 1]

                if index < len(list_vars) - 1:
                    next_symbol = list_vars[index + 1]

                remove: bool = curr_symbol in [">", r"\geq"] and ">" in [prev_symbol, next_symbol]

                if not remove:
                    list_vars0.append(curr_symbol)

            #if len(list_vars0) > 0 and list_vars0[0] in [">", r"\geq"]:
             #   list_vars0 = list_vars0[1:]

            #if len(list_vars0) > 1 and list_vars0[-1] == "0" and list_vars0[-2]:
             #   list_vars0 = list_vars0[:-2]

            if "overset" in line0:
                build_order(list_vars0, 0, stack=Stack(), list_strs=list_strs,
                            list_original=list_vars_original)
                list_symbols.append(list_vars0)

    if isinstance(list_strs, list) and len(list_strs) > 0:
        list_strs.sort(key=cmp_to_key(lambda list1, list2: compare_lists(list1, list2)))

    dict_orders: dict[str, list[str]] = {}

    for tup in list_strs:
        str0: str = convert_order_to_str(tup[0])
        str1: str = convert_line_to_str(tup[1])

        if str1 not in dict_orders.keys():
            dict_orders[str1] = []

        list_orders: list[str] = dict_orders[str1]

        list_orders.append(str0)

    with open(".\\saved_output\\orders.txt", "w") as fw:
        counter: int = 0

        for key in dict_orders.keys():
            counter += 1
            fw.write(f"original[{counter}]: {key}\n")

            list_orders: list[str] = dict_orders[key]

            counter0: int = 0

            for val in list_orders:
                counter0 += 1

                fw.write(f"\torder[{counter}][{counter0}]: {val}\n")

            fw.write(f"========================================\n")

        #for tup in list_strs:
         #   str0: str = convert_order_to_str(tup[0])
          #  str1: str = convert_line_to_str(tup[1])
           # fw.write(f"order[{counter}]: {str0}, original: {str1}\n")
            #counter += 1


def compare_lists(tup1: tuple[list, list], tup2: tuple[list, list]):
    list1: list = tup1[0]
    list2: list = tup2[0]

    index: int = 0

    comp: int = 0

    while comp == 0 and index < len(list1) and index < len(list2):
        obj1 = list1[index]
        obj2 = list2[index]

        index += 1

        if obj1 != obj2:
            if isinstance(obj1, int) and isinstance(obj2, int):
                comp = obj1 - obj2
            else:
                comp = 1 if obj2 == ">" else -1

    return comp


def push_operator(index: int, stack: Stack):
    if list_collected(stack):
        return

    for str0 in [">", "="]:
        stack.push(str0)
        check_all_orders(index=index + 1, stack=stack)
        _ = stack.pop()


def check_all_orders_backup(index: int, stack: Stack):
    if list_collected(stack):
        return

    for i in range(4):
        var_index: int = i + 1

        if var_index not in stack:
            stack.push(var_index)
            push_operator(index, stack=stack)
            _ = stack.pop()


def check_all_orders(index: int, stack: Stack, lisr_strs: list[str]):
    list_operators: list[str] = list(stack)

    if isinstance(list_operators, list) and len(list_operators) >= 3:
        str0: str = ""

        index: int = 0

        len_list_operators = len(list_operators)

        var_index: int = 0

        for i in range(len_list_operators):
            var_index = i + 1

            str_op: str = list_operators[i]

            str0 = f"{str0}v_{var_index}{str_op}"

        var_index = len_list_operators + 1

        str0 = f"{str0}v_{var_index}"

        lisr_strs.append(str0)

        return

    for op in [">", "<", "="]:
        stack.push(op)
        check_all_orders(index=index, stack=stack, lisr_strs=lisr_strs)
        _ = stack.pop()


def list_collected(stack: Stack):
    is_collected: bool = False

    count: int = 0

    for i in range(4):
        var_index: int = i + 1

        if var_index in stack:
            count += 1

    if count >= 4:
        str0: str = ",".join([str(element) for element in stack])

        print(str0)

        is_collected = True

    return is_collected
