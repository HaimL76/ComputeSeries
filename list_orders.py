import re


def list_orders(file_path: str) -> list[int]:
    orders: list[int] = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()

            line = line.replace("{", "").replace("}", "")

            line = re.sub(r'\\overset[abcde]', '', line)

            if line:
                line = line.strip()

            arr: list[str] = re.split(r'\\geq|>', line)

            arr = [s.strip() for s in arr if s.startswith("v_")]

            if isinstance(arr, list) and len(arr) > 3:
                print(line)
    return orders