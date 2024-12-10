import pyperclip
from time import perf_counter
from collections import defaultdict


def display_output(func) -> None:
    with open("input.txt", "r", encoding="utf-8") as f:
        values = f.read().splitlines()
    # values = [
    #     "47|53",
    #     "97|13",
    #     "97|61",
    #     "97|47",
    #     "75|29",
    #     "61|13",
    #     "75|53",
    #     "29|13",
    #     "97|29",
    #     "53|29",
    #     "61|53",
    #     "97|53",
    #     "61|29",
    #     "47|13",
    #     "75|47",
    #     "97|75",
    #     "47|61",
    #     "75|61",
    #     "47|29",
    #     "75|13",
    #     "53|13",
    #     "",
    #     "75,47,61,53,29",
    #     "97,61,53,29,13",
    #     "75,29,13",
    #     "75,97,47,61,53",
    #     "61,13,29",
    #     "97,13,75,29,47",
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


def parse(values: list) -> tuple[list[tuple[int, int]], list[list[int]]]:
    rules = []
    updates = []
    for i, value in enumerate(values):
        if value == "":
            break
        a, b = value.split("|")
        rules.append((int(a), int(b)))

    for value in values[i+1:]:
        updates.append(list(map(int, value.split(","))))

    return rules, updates


def create_maps(rules: list[tuple[int, int]]) -> tuple[dict[int, list[int]], ...]:
    before_map = defaultdict(set)
    after_map = defaultdict(set)
    for before, after in rules:
        before_map[after].add(before)
        after_map[before].add(after)
    return before_map, after_map


def verify(
    update: list[int],
    before_map: dict[int, list[int]],
    after_map: dict[int, list[int]],
) -> bool:
    for i, value in enumerate(update):
        if any(v not in before_map[value] for v in update[:i]):
            return False
        if any(v not in after_map[value] for v in update[i+1:]):
            return False
    return True



def main(values: list) -> None:
    rules, updates = parse(values)
    before_map, after_map = create_maps(rules)
    correct = []
    for update in updates:
        if verify(update, before_map, after_map):
            correct.append(update)

    total = 0
    for update in correct:
        center = update[len(update)//2]
        total += center
    return total


if __name__ == "__main__":
    display_output(main)
