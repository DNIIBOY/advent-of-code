import pyperclip
from time import perf_counter
import re


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


def solve_line(line: str) -> int:
    pattern = re.compile(r"mul\((\d{,3})\,(\d{,3})\)")
    matches = pattern.findall(line)
    total = 0
    for match in matches:
        total += int(match[0]) * int(match[1])
    return total


def solve_line2(line: str) -> int:
    pattern = re.compile(r"mul\((\d{,3})\,(\d{,3})\)|(don't\(\)|do\(\))")
    matches = pattern.findall(line)
    total = 0
    enabled = True
    for match in matches:
        print(match)
        if match[2] == "don't()":
            enabled = False
            print(enabled)
        elif match[2] == "do()":
            enabled = True
            print(enabled)
        if match[0] and match[1] and enabled:
            total += int(match[0]) * int(match[1])
    return total


def main(lines: list) -> None:
    total = 0
    for line in lines:
        total += solve_line(line)
    return total


def main2(lines: list) -> None:
    return solve_line2("".join(lines))


if __name__ == "__main__":
    display_output(main2)
