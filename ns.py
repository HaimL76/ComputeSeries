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

    list_strs: list[str] = create_n(n=n)

    if isinstance(list_strs, list) and len(list_strs) > 0:
        with open("ns_sage.txt", "w") as f:
            f.write("def idx(i: int):\n")
            f.write("\treturn i - 1\n\n")

            if isinstance(list_symbols, list) and len(list_symbols) > 0:
                str_symbols = ",".join(list_symbols)

                f.write(f"{str_symbols} = var(\"{str_symbols}\")\n\n")

            for s in list_strs:
                if s:
                    f.write(f"{s}\n")

            for r in range(2, n - 1):
                for k in range(n - r + 1):
                    f.write(f"print(N_{r}_{k})\n")

def get_left(r: int, i: int):
    index: int = r - 1

    left_offset: int = lefts[index]

    return left_offset - 1 + i

def create_n(n: int):
    list_strs: list[str] = []

    d: int =  int(n * (n - 1) / 2)

    left: int = n - 1

    for r in range(2, n - 1):
        list_strs0: list[str] = create_n_r(n=n, d=d, left=left, r=r)

        if isinstance(list_strs0, list) and len(list_strs0) > 0:
            list_strs += list_strs0

        left += (n - r)

    return list_strs

def create_n_r(n: int, d: int, left: int, r: int):
    list_strs: list[str] = []
    ##print(f"create_n_r, n: {n}, r: {r}")
    symbol_index: int = r - 2

    symbol: str = symbols[symbol_index]

    for k in range(n - r + 1):
        list_strs0: list[str] = create_n_r_k(n=n, d=d, left=left, r=r, k=k, symbol=symbol)

        if isinstance(list_strs0, list) and len(list_strs0) > 0:
            list_strs += list_strs0

    return list_strs

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

            if len(element_left) > 2:
                symb_left = element_left[2]

            if len(element_right) > 2:
                symb_right = element_right[2]

            symb: str = symb_left or symb_right

            if symb_left and symb_right:
                symb = "*".join([symb_left, symb_right])

            element: tuple = None

            if j_left == i_right:
                element = (i_left, j_right, symb)

            if i_left == j_right:
                element = (i_right, j_left, symb)

            if isinstance(element, tuple):
                elements.append(element)

    return elements


def get_image(r: int, k: int, i: int, j: int, symbol: str):
    diff: int = j - i

    if diff > 1:
        image_left = get_image(r=r, k=k, i=i, j=j - 1, symbol=symbol)
        image_right = get_image(r=r, k=k, i=j - 1, j=j, symbol=symbol)

        return multiply_images(image_left=image_left, image_right=image_right)

    symb: str = symbol

    if symb:
        i1: int = k
        j1: int = k

        if k == 0:
            i1 = r
            j1 = 1

        symb = f"{symb}{i1}{j1}"

        if symb and symb not in list_symbols:
            list_symbols.append(symb)

    if i == k:
        return [(i, i + 1), (k, k + r, symb)]
    
    elif i == (k + r):
        return [(i, i + 1), (k + 1, k + 1 + r, symb, True)]
    
    else:
        return [(i, i + 1)]
    
def print_image(elements: list[tuple], r: int, k: int, i: int):
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

                if symb:
                    return f"N_{r}_{k}[idx({i}),idx({left})]={symb}"

def create_n_r_k(n: int, d: int, left: int, r: int, k: int, symbol: str):
    s: str = f"N_{r}_{k}=matrix(SR, {d}, {d}, 1)"

    list_strs: list[str] = [s]
    ##    print(f"\tcreate_n_r_k, n: {n}, r: {r}, k: {k}")
    
    for r0 in range(1, 3):
        for i in range(1, n - r0):
        #print(f"\tcreate_n_r_k, n: {n}, r: {r}, k: {k}, i: {i}")

            elements: list[tuple] = get_image(r, k, i, i + r0, symbol=symbol)

            if isinstance(elements, list):
                s: str = print_image(elements=elements, r=r, k=k, i=i)

                if s:
                    list_strs.append(s)

    return list_strs

    print(f"N_{r}_{k}=matrix(SR, {d}, {d}, 1)")

    top: int = 1
    size_vertical: int = n - 1

    for i in range(n - 1):
        bottom: int = top + size_vertical - 1

        if k < bottom:
            print(f"N_{r}_{k}[idx({k}),idx({left+k})]={symbol}_{{{k}{k}}}")

        if (k + r) < bottom:
            print(f"N_{r}_{k}[idx({k+r}),idx({left+k+1})]=-{symbol}_{{{k}{k}}}")

main()