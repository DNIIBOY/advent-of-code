import pyperclip
import re
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


max_cubes = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

count_color_regex = re.compile(r"(\d+) (\w+)")
game_id_regex = re.compile(r"Game (\d+):")


def is_legal_round(round_content: str) -> bool:
    cubes = round_content.split(", ")
    for cube in cubes:
        count, color = count_color_regex.match(cube).groups()
        if int(count) > max_cubes[color]:
            return False
    return True


def is_legal_game(game: str) -> bool:
    game = game.split(":")[1].strip()
    rounds = game.split("; ")
    for round_content in rounds:
        if not is_legal_round(round_content):
            return False
    return True


def get_game_id(game: str) -> int:
    return int(game_id_regex.match(game).group(1))


def main(games: list) -> None:
    result = 0
    for game in games:
        if is_legal_game(game):
            result += get_game_id(game)
    return result


if __name__ == "__main__":
    display_output(main)
