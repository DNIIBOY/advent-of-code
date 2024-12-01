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


def find_number_indexes(table: list[str]) -> list[tuple[int, int]]:
    """
    Find the indexes of the numbers in the table.
    Only includes the index of the first digit of each number.
    :param table: The table to search.
    :return: A list of tuples containing the indexes of the numbers.
    """
    for i, row in enumerate(table):
        for j, char in enumerate(row):
            if char.isdigit() and not table[i][j-1].isdigit():
                yield i, j


def is_symbol(char: str) -> bool:
    """
    Check if a character is a symbol.
    Symbols are defined as any character that is not a digit or a period.
    :param char: The character to check.
    :return: True if the character is a symbol, False otherwise.
    """
    if char == ".":
        return False
    if char.isdigit():
        return False
    return True


def has_adjacent_symbol(table: list[str], row: int, col: int) -> bool:
    """
    Check if a number has a symbol adjacent to it.
    :param table: The table to search.
    :param row: The row of the number.
    :param col: The column of the number.
    :return: True if the number has a symbol adjacent to it, False otherwise.
    """
    char = table[row][col]
    while char.isdigit() and col < len(table[row]) - 1:
        for i in range(row-1, row+2):
            if i > len(table) - 1:
                continue
            for j in range(col-1, col+2):
                if j < len(table[i]) - 1 and is_symbol(table[i][j]):
                    return True
        col += 1
        char = table[row][col]
    return False


def get_number(table: list[str], row: int, col: int) -> int:
    """
    Get the number at the given index.
    :param table: The table to search.
    :param row: The row of the number.
    :param col: The column of the number.
    :return: The number at the given index.
    """
    char = table[row][col]
    number = ""
    while char.isdigit() and col < len(table[row]) - 1:
        number += char
        col += 1
        char = table[row][col]
    return int(number)


def main(values: list) -> int:
    result = 0
    for row, col in find_number_indexes(values):
        if has_adjacent_symbol(values, row, col):
            result += get_number(values, row, col)
    return result


if __name__ == "__main__":
    display_output(main)
