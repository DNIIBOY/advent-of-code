import pyperclip
from time import perf_counter
from enum import Enum


def display_output(func) -> None:
    with open("input.txt", "r", encoding="utf-8") as f:
        values = f.read().splitlines()
    # values = [
    #     "....#.....",
    #     ".........#",
    #     "..........",
    #     "..#.......",
    #     ".......#..",
    #     "..........",
    #     ".#..^.....",
    #     "........#.",
    #     "#.........",
    #     "......#...",
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


class Direction(Enum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"


def get_start(values: list[str]) -> tuple[int, int, Direction]:
    for y, row in enumerate(values):
        for x, cell in enumerate(row):
            if cell in Direction:
                return x, y, Direction(cell)


def move(x: int, y: int, direction: Direction) -> tuple[int, int]:
    if direction == Direction.UP:
        return x, y - 1
    if direction == Direction.DOWN:
        return x, y + 1
    if direction == Direction.LEFT:
        return x - 1, y
    if direction == Direction.RIGHT:
        return x + 1, y


def turn(x: int, y: int, direction: Direction, values: list) -> Direction:
    check_x, check_y = move(x, y, direction)
    if not in_bounds(check_x, check_y, values):
        return direction
    if values[check_y][check_x] == "#":
        if direction == Direction.UP:
            return Direction.RIGHT
        if direction == Direction.RIGHT:
            return Direction.DOWN
        if direction == Direction.DOWN:
            return Direction.LEFT
        if direction == Direction.LEFT:
            return Direction.UP
    return direction


def in_bounds(x: int, y: int, values: list[str]) -> bool:
    return 0 <= y < len(values) and 0 <= x < len(values[0])


def mark(values: list, x, y) -> None:
    values[y] = values[y][:x] + "X" + values[y][x + 1:]


def display(values: list) -> None:
    for row in values:
        print(row)
    print()


def count(values: list) -> int:
    return sum(row.count("X") for row in values)


def main(values: list[str]) -> None:
    x, y, direction = get_start(values)
    while in_bounds(x, y, values):
        mark(values, x, y)
        direction = turn(x, y, direction, values)
        x, y = move(x, y, direction)
    display(values)
    return count(values)


if __name__ == "__main__":
    display_output(main)
