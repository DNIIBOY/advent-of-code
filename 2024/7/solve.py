import pyperclip
from time import perf_counter


def display_output(func) -> None:
    with open("input.txt", "r", encoding="utf-8") as f:
        values = f.read().splitlines()
    # values = [
    #     "190: 10 19",
    #     "3267: 81 40 27",
    #     "83: 17 5",
    #     "156: 15 6",
    #     "7290: 6 8 6 15",
    #     "161011: 16 10 13",
    #     "192: 17 8 14",
    #     "21037: 9 7 18 13",
    #     "292: 11 6 16 20",
    # ]

    start = perf_counter()
    result = func(values)
    end = perf_counter()
    print(f"--- Got result in {end-start:.2f}s---")
    print(result)
    try:
        pyperclip.copy(result)
        print("--- Copied to clipboard ---")
    except FileNotFoundError:
        pass


def parse(equation: str) -> tuple[int, list[int]]:
    equation = equation.split(":")
    return int(equation[0]), list(map(int, equation[1].split()))


def options(vals: list) -> list:
    if len(vals) == 1:
        return vals
    val = vals[-1]
    vals = vals[:-1]
    new = options(vals)
    out = [val + i for i in new] + [val * i for i in new]
    return out


def options2(vals: list) -> list:
    if len(vals) == 1:
        return vals
    val = vals[-1]
    vals = vals[:-1]
    new = options2(vals)
    out = [val + i for i in new] + [val * i for i in new] + [int(str(i) + str(val)) for i in new]
    return out


def main(values: list) -> None:
    total = 0
    for value in values:
        solution, equation = parse(value)
        if solution in options2(equation):
            total += solution
    return total


if __name__ == "__main__":
    display_output(main)
