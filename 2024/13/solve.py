import pyperclip
from time import perf_counter
import re


def display_output(func) -> None:
    with open("input.txt", "r", encoding="utf-8") as f:
        values = f.read().splitlines()
    # values = [
    #     "Button A: X+94, Y+34",
    #     "Button B: X+22, Y+67",
    #     "Prize: X=8400, Y=5400",
    #     "",
    #     "Button A: X+26, Y+66",
    #     "Button B: X+67, Y+21",
    #     "Prize: X=12748, Y=12176",
    #     "",
    #     "Button A: X+17, Y+86",
    #     "Button B: X+84, Y+37",
    #     "Prize: X=7870, Y=6450",
    #     "",
    #     "Button A: X+69, Y+23",
    #     "Button B: X+27, Y+71",
    #     "Prize: X=18641, Y=10279",
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


def parse(lines: list[str]) -> list[dict[str, tuple[int, int]]]:
    games = []
    for i in range(0, len(lines), 4):
        game = {}
        match = re.search(r"X\+(\d+), Y\+(\d+)", lines[i])
        game["a"] = (int(match.group(1)), int(match.group(2)))
        match = re.search(r"X\+(\d+), Y\+(\d+)", lines[i + 1])
        game["b"] = (int(match.group(1)), int(match.group(2)))
        match = re.search(r"X=(\d+), Y=(\d+)", lines[i + 2])
        game["prize"] = (int(match.group(1)), int(match.group(2)))
        games.append(game)
    return games


def can_reach(position: tuple[int, int], button: tuple[int, int], prize: tuple[int, int]) -> bool:
    """
    Check if it is possible to reach the prize from the current position using the button
    :param position: current position
    :param button: X and Y moves of the button
    :param prize: position of the prize
    """
    target = (prize[0] - position[0], prize[1] - position[1])
    if target[0] < 0 or target[1] < 0:
        return False
    return target[0] % button[0] == 0 and target[1] % button[1] == 0 and (target[0] // button[0]) == (target[1] // button[1])


def get_lowest_cost(game: dict[str, tuple[int, int]]) -> int:
    a = game["a"]
    b = game["b"]
    prize = game["prize"]
    a_pos = [0, 0]
    a_presses = 0
    while not can_reach(a_pos, b, prize) and a_presses <= 100:
        a_pos[0] += a[0]
        a_pos[1] += a[1]
        a_presses += 1

    if a_presses >= 100:
        return 0
    b_presses = (prize[0] - a_pos[0]) // b[0]
    assert b_presses == (prize[1] - a_pos[1]) // b[1]
    return a_presses * 3 + b_presses


def main(values: list) -> None:
    games = parse(values)
    total_cost = 0
    for game in games:
        total_cost += get_lowest_cost(game)
    return total_cost


if __name__ == "__main__":
    display_output(main)
