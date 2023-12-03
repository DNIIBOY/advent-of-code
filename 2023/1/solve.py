import pyperclip
from time import perf_counter


def display_output(func) -> None:
    with open("input.txt", "r", encoding="utf-8") as f:
        values = f.read().splitlines()

    start = perf_counter()
    result = func(values)
    end = perf_counter()
    print(f"--- Got result in {end-start:.2f}s---")
    pyperclip.copy(result)
    print(result)
    print("--- Copied to clipboard ---")


def get_calibration_value(number: str) -> int:
    i = 0
    first = ""
    last = ""
    while i < len(number):
        if number[i].isdigit():
            first = number[i]
            break
        i += 1

    i = len(number) - 1
    while i >= 0:
        if number[i].isdigit():
            last = number[i]
            break
        i -= 1
    return int(first + last)


def main(values: list) -> None:
    result = 0
    for value in values:
        output = get_calibration_value(value)
        result += output
    return result


if __name__ == "__main__":
    display_output(main)
