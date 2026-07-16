symbols: list[str] = ['a', 'b', 'c']

def main():
    n: int = 5

    global lefts
    global list_symbols

    lefts = [0] * (n - 1)

    list_symbols = []

    left: int = 1

    for i in range(n - 1):
        lefts[i] = left

        left += (n - i - 1)

    list_strs, list_auts = create_n(n=n)

    if isinstance(list_strs, list) and len(list_strs) > 0:
        with open("ns_sage.txt", "w") as f:
            f.write("def idx(i: int):\n")
            f.write("\treturn i - 1\n\n")

            if isinstance(list_symbols, list) and len(list_symbols) > 0:
                str_symbols = ",".join(list_symbols)

                f.write(f"{str_symbols} = var(\"{str_symbols}\")\n\n")

            if isinstance(list_strs, list) and len(list_strs) > 0:
                for s in list_strs:
                    if s:
                        f.write(f"{s}\n")

            if isinstance(list_auts, list) and len(list_auts) > 0:
                for aut in list_auts:
                    f.write(f"print(f\"{aut}=\\n{{{aut}}}\")\n")

def get_left(r: int, i: int):
    index: int = r - 1

    left_offset: int = lefts[index]

    return left_offset - 1 + i

def create_n(n: int):
    list_strs: list[str] = []
    list_auts: list[str] = []

    d: int =  int(n * (n - 1) / 2)

    left: int = n - 1

    for r in range(2, n ):
        list_strs0, list_auts0 = create_n_r(n=n, d=d, left=left, r=r)

        if isinstance(list_strs0, list) and len(list_strs0) > 0:
            list_strs += list_strs0

        if isinstance(list_auts0, list) and len(list_auts0) > 0:
            list_auts += list_auts0

        left += (n - r)

    return list_strs, list_auts

def create_n_r(n: int, d: int, left: int, r: int):
    list_strs: list[str] = []
    list_auts: list[str] = []

    symbol_index: int = r - 2

    symbol: str = symbols[symbol_index]

    aut: str = None

    for k in range(n - r + 1):
        aut, list_strs0 = create_n_r_k(n=n, d=d, left=left, r=r, k=k, l=0, symbol=symbol)

        if isinstance(list_strs0, list) and len(list_strs0) > 0:
            list_strs += list_strs0
            
            if aut:
                list_auts.append(aut)

    if (r == (n - 2)):
        aut, list_strs1 = create_n_r_k(n=n, d=d, left=left, r=r, k=1, l=2, symbol=symbol)

        if aut:
            list_auts.append(aut)

        if isinstance(list_strs1, list) and len(list_strs1) > 0:
            list_strs += list_strs1

        aut, list_strs2 = create_n_r_k(n=n, d=d, left=left, r=r, k=(n - 1), l=1, symbol=symbol)

        if aut:
            list_auts.append(aut)

        if isinstance(list_strs2, list) and len(list_strs2) > 0:
            list_strs += list_strs2

    return list_strs, list_auts

def multiply_images(image_left: list[tuple], image_right: list[tuple]):
    elements: list[tuple] = []

    for element_left in image_left:
        for element_right in image_right:
            i_left = element_left[0]
            i_right = element_right[0]

            j_left = element_left[1]
            j_right = element_right[1]

            symb_left: str = None
            symb_right: str = None

            is_minus_left: bool = False
            is_minus_right: bool = False

            if len(element_left) > 2:
                symb_left = element_left[2]

                if len(element_left) > 3:
                    is_minus_left = element_left[3]

            if len(element_right) > 2:
                symb_right = element_right[2]

                if len(element_right) > 3:
                    is_minus_right = element_right[3]

            is_minus: bool = is_minus_left != is_minus_right

            symb: str = symb_left or symb_right

            if symb_left and symb_right:
                symb = "*".join([symb_left, symb_right])

            element: tuple = None

            if j_left == i_right:
                element = (i_left, j_right, symb, is_minus)

            if i_left == j_right:
                element = (i_right, j_left, symb, not is_minus)

            if isinstance(element, tuple):
                elements.append(element)

    return elements

def print_element(element: tuple):
    s: str = ""

    i: int = element[0]
    j: int = element[1]

    symb: str = None

    is_minus: bool = False

    if len(element) > 2:
        symb = element[2]

        if len(element) > 3:
            is_minus = element[3]

    if symb:
        s = symb

    s += f"e{i}{j}"

    return is_minus, s

def print_image(elements: list[tuple]):
    s: str = None

    for element in elements:
        is_minus, s0 = print_element(element=element)

        if s0:
            if isinstance(s, str):
                sign: str = "-" if is_minus else "+"

                s = f"{s} {sign} {s0}"
            else:
                s = s0

    return s

def get_image(n: int, r: int, k: int, i: int, j: int, l: int, symbol: str):
    diff: int = j - i

    if diff > 1:
        image_left = get_image(n=n, r=r, k=k, i=i, j=j - 1, l=l, symbol=symbol)
        image_right = get_image(n=n, r=r, k=k, i=j - 1, j=j, l=l, symbol=symbol)

        return multiply_images(image_left=image_left, image_right=image_right)

    symb: str = symbol

    if symb:
        i1: int = k
        j1: int = k

        if k == 0:
            i1 = r
            j1 = 1

        symb0: str = f"{symb}{i1}{j1}"

        if symb0 and symb0 not in list_symbols:
            list_symbols.append(symb0)

    list_images: list[tuple] = None

    list_images = [(i, i + 1)]

    if l == 0:
        if r == (n - 1):
            symb2: str = f"{symb}{i}"
            list_images.append((1, 1 + r, symb2))

            if symb2 and symb2 not in list_symbols:
                list_symbols.append(symb2)
        else:
            if i == k:
                list_images.append((k, k + r, symb0))
    
            elif i == (k + r):
                list_images.append((k + 1, k + 1 + r, symb0, True))
    else:
        if i == k:
            symb1: str = f"{symb}{k}{l}"
            list_images.append((l, l + r, symb1))

            if symb1 and symb1 not in list_symbols:
                list_symbols.append(symb1)

    return list_images
    
def get_image_string(aut: str, elements: list[tuple], r: int, k: int, i: int, j: int):
    if isinstance(elements, list):
        for element in elements:
            if isinstance(element, tuple) and len(element) > 1:
                symb: str = None

                idx_i: int = element[0]
                idx_j: int = element[1]

                if len(element) > 2:
                    symb = element[2]

                    if symb and len(element) > 3:
                        is_minus: bool = element[3]

                        if is_minus:
                            symb = f"-{symb}"

                diff: int = idx_j - idx_i

                left: int = get_left(diff, idx_i)

                diff = j - i

                top = get_left(diff, i)

                if symb:
                    return f"{aut}[idx({top}),idx({left})]={symb}"

def create_n_r_k(n: int, d: int, left: int, r: int, k: int, l: int, symbol: str):
    aut: str = f"N_{r}"

    if r < (n - 1):
        aut = f"{aut}_{k}"
    else:
        if k == 0:
            return None, None

    if l > 0:
        aut = f"N_{r}"

        for l0 in range(l):
            aut = f"{aut}p"

    s: str = f"{aut}=matrix(SR, {d}, {d}, 1)"

    list_strs: list[str] = [s]
    
    for r0 in range(1, n):
        for i in range(1, n - r0 + 1):
            elements: list[tuple] = get_image(n=n, r=r, k=k, i=i, j=(i + r0), l=l, symbol=symbol)

            if isinstance(elements, list):
                s0: str = print_image(elements)

                if s0:
                    print(f"{aut}(e{i}{i+r0}) = {s0}")

                s: str = get_image_string(aut=aut, elements=elements, r=r, k=k, i=i, j=(i + r0))

                if s:
                    list_strs.append(s)

    return aut, list_strs

main()