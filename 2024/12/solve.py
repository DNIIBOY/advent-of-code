import pyperclip
from time import perf_counter


def display_output(func) -> None:
    with open("input.txt", "r", encoding="utf-8") as f:
        values = f.read().splitlines()

    # values = [
    #     "RRRRIICCFF",
    #     "RRRRIICCCF",
    #     "VVRRRCCFFF",
    #     "VVRCCCJFFF",
    #     "VVVVCJJCFE",
    #     "VVIVCCJJEE",
    #     "VVIIICJJEE",
    #     "MIIIIIJJEE",
    #     "MIIISIJEEE",
    #     "MMMISSJEEE",
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


def main(values: list) -> None:
    visited = set()

    def dfs(i, j, target):
        if i < 0 or j < 0 or i >= len(values) or j >= len(values[0]) or (i, j) in visited:
            return 0
        if (i, j) in visited:
            return 0
        if values[i][j] != target:
            return 0

        visited.add((i, j))
        options = ((i+1, j), (i-1, j), (i, j+1), (i, j-1))

        total = 0
        for option in options:
            try:
                assert option[0] >= 0 and option[1] >= 0
                if values[option[0]][option[1]] != target:
                    total += 1
            except (IndexError, AssertionError):
                total += 1
            total += dfs(*option, target)
        return total

    total_price = 0
    for i, row in enumerate(values):
        for j, cell in enumerate(row):
            if (i, j) in visited:
                continue
            count = len(visited)
            price = dfs(i, j, cell)
            diff = len(visited) - count
            total_price += price * diff
    return total_price


if __name__ == "__main__":
    display_output(main)
