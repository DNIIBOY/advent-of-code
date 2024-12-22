import pyperclip
from time import perf_counter


def display_output(func) -> None:
    with open("input.txt", "r", encoding="utf-8") as f:
        values = f.read().splitlines()

    # values = [
    #     "MMMSXXMASM",
    #     "MSAMXMSMSA",
    #     "AMXSXMAAMM",
    #     "MSAMASMSMX",
    #     "XMASAMXAMM",
    #     "XXAMMXXAMA",
    #     "SMSMSASXSS",
    #     "SAXAMASAAA",
    #     "MAMMMXMMMM",
    #     "MXMXAXMASX",
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


def count_occurrences(grid, word):
    def check_direction(x, y, dx, dy):
        for i in range(len(word)):
            nx, ny = x + i * dx, y + i * dy
            if nx < 0 or ny < 0 or nx >= len(grid) or ny >= len(grid[0]):
                return False
            if grid[nx][ny] != word[i]:
                return False
        return True

    rows, cols = len(grid), len(grid[0])
    count = 0

    directions = [
        (0, 1),   # Right
        (1, 0),   # Down
        (1, 1),   # Down-right
        (1, -1),  # Down-left
        (0, -1),  # Left
        (-1, 0),  # Up
        (-1, -1),  # Up-left
        (-1, 1)   # Up-right
    ]

    for x in range(rows):
        for y in range(cols):
            for dx, dy in directions:
                if check_direction(x, y, dx, dy):
                    count += 1

    return count


def main(values: list) -> None:
    word = "XMAS"
    total = count_occurrences(values, word)
    return total


if __name__ == "__main__":
    display_output(main)
