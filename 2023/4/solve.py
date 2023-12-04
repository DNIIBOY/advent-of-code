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


def winning_numbers_count(card: str) -> int:
    """
    Get number of winning numbers for a card
    """
    card = card.split(":")[1].strip()  # Remove card name
    winning, numbers = card.split("|")
    winning = [number.strip() for number in winning.split()]
    numbers = numbers.split()
    count = 0
    for number in numbers:
        number = number.strip()
        if number in winning:
            count += 1
    return count


def get_points(winning_number_count: int) -> int:
    """
    Get points for a card.
    1 winning = 1 point.
    2 winning = 2 points.
    3 winning = 4 points.
    etc.
    """
    if winning_number_count == 0:
        return 0
    return 2 ** (winning_number_count - 1)


def main(cards: list) -> None:
    total = 0
    for card in cards:
        total += get_points(winning_numbers_count(card))
    return total


if __name__ == "__main__":
    display_output(main)
