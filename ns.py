symbols: list[str] = ['a', 'b', 'c']

def main():
    n: int = 5

    global lefts

    lefts = [0] * (n - 1)

    left: int = 1

    for i in range(n - 1):
        lefts[i] = left

        left += (n - i - 1)

    create_n(n=n)

def get_left(r: int, i: int):
    index: int = r - 1

    left_offset: int = lefts[index]

    return left_offset - 1 + i

def create_n(n: int):
    d: int =  int(n * (n - 1) / 2)

    left: int = n - 1

    for r in range(2, n - 1):
        create_n_r(n=n, d=d, left=left, r=r)

        left += (n - r)

def create_n_r(n: int, d: int, left: int, r: int):
    symbol_index: int = r - 2

    symbol: str = symbols[symbol_index]

    for k in range(n - r + 1):
        create_n_r_k(n=n, d=d, left=left, r=r, k=k, symbol=symbol)

def get_image(r: int, k: int, i: int):
    if i == k:
        return [(None, i, i + 1), ("a", k, k + r)]
    
    elif i == (k + r):
        return [(None, i, i + 1), ("-a", k + 1, k + 1 + r)]
    
    else:
        return [(None, i, i + 1)]

def create_n_r_k(n: int, d: int, left: int, r: int, k: int, symbol: str):
    for i in range(1, n):
        elements: list[tuple] = get_image(r, k, i)

        if isinstance(elements, list):
            for element in elements:
                if isinstance(element, tuple) and len(element) == 3:
                    symbol: str = element[0]
                    idx_i: int = element[1]
                    idx_j: int = element[2]

                    diff: int = idx_j - idx_i

                    left: int = get_left(diff, idx_i)

                    if symbol:
                        print(f"N_{r}_{k}[idx({i}),idx({left})]={symbol}")#{symbol}_{{{k}{k}}}")




    return
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