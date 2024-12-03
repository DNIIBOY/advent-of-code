import pyperclip
from time import perf_counter
from collections import defaultdict


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


def get_counts(values: list) -> dict:
    counts = defaultdict(int)
    for value in values:
        counts[value] += 1
    return counts


def get_min(values: dict) -> str:
    vals = []
    for k, v in values.items():
        if v > 0:
            vals.append(int(k))
    return min(vals)


def main(values: list) -> None:
    left = []
    right = []
    for value in values:
        l, r = value.split("   ")
        left.append(l)
        right.append(r)
    left_counts = get_counts(left)
    right_counts = get_counts(right)

    total_diff = 0
    while any(left_counts.values()) and any(right_counts.values()):
        min_left = get_min(left_counts)
        min_right = get_min(right_counts)
        left_counts[str(min_left)] -= 1
        right_counts[str(min_right)] -= 1
        diff = abs(int(min_left) - int(min_right))
        total_diff += diff

    return total_diff


def main2(values: list) -> None:
    left = []
    right = []
    for value in values:
        l, r = value.split("   ")
        left.append(l)
        right.append(r)
    right_counts = get_counts(right)

    total_sim = 0
    for value in left:
        total_sim += int(value) * right_counts[value]

    return total_sim


if __name__ == "__main__":
    display_output(main2)
