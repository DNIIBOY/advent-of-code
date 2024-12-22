import pyperclip
from time import perf_counter
from collections import defaultdict


def display_output(func) -> None:
    with open("input.txt", "r", encoding="utf-8") as f:
        values = f.read().splitlines()

    # values = [
    #     "............",
    #     "........0...",
    #     ".....0......",
    #     ".......0....",
    #     "....0.......",
    #     "......A.....",
    #     "............",
    #     "............",
    #     "........A...",
    #     ".........A..",
    #     "............",
    #     "............",
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


def get_antinodes(i: int, j: int, antennas: list[tuple[int, int]], rows: int, cols: int) -> set[tuple[int, int]]:
    antinodes = set()
    for y, x in antennas:
        if y == i and x == j:
            continue
        diff_x = x - j
        diff_y = y - i

        a_x = j - diff_x
        if a_x < 0 or a_x >= cols:
            continue
        a_y = i - diff_y
        if a_y < 0 or a_y >= rows:
            continue

        antinodes.add((a_y, a_x))
    return antinodes


def main(values: list) -> None:
    antennas: dict[str, list[tuple[int, int]]] = defaultdict(list)
    antinodes: set[tuple[int, int]] = set()
    rows = len(values)
    cols = len(values[0])

    for i, row in enumerate(values):
        for j, val in enumerate(row):
            if val == ".":
                continue
            antennas[val].append((i, j))
    for freq in antennas:
        for location in antennas[freq]:
            antinodes |= get_antinodes(location[0], location[1], antennas[freq], rows, cols)
    for node in antinodes:
        values[node[0]] = values[node[0]][:node[1]] + "#" + values[node[0]][node[1]+1:]
    # print("\n".join(values))
    return len(antinodes)


if __name__ == "__main__":
    display_output(main)
