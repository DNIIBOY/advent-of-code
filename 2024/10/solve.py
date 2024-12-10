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


def dfs(grid, i, j, target="0", sols: set = None):
    if sols is None:
        sols = set()
    if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]):
        return sols

    if target == "9" and grid[i][j] == "9":
        sols.add((i, j))
        return sols

    if grid[i][j] == target:
        target = str(int(target) + 1)
        sets = [
            dfs(grid, i+1, j, target),
            dfs(grid, i-1, j, target),
            dfs(grid, i, j+1, target),
            dfs(grid, i, j-1, target)
        ]
        return set(
            [item for sublist in sets for item in sublist]
        )
    return sols


def dfs2(grid, i, j, target="0"):
    if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]):
        return 0

    if target == "9" and grid[i][j] == "9":
        return 1

    if grid[i][j] == target:
        target = str(int(target) + 1)
        return sum([
            dfs2(grid, i+1, j, target),
            dfs2(grid, i-1, j, target),
            dfs2(grid, i, j+1, target),
            dfs2(grid, i, j-1, target)
        ])
    return 0


def main(values: list) -> None:
    score = 0
    for i in range(len(values)):
        for j in range(len(values[i])):
            if values[i][j] == "0":
                score += dfs2(values, i, j)
    return score


if __name__ == "__main__":
    display_output(main)
