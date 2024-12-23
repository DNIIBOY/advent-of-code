import pyperclip
from time import perf_counter
from copy import deepcopy


def display_output(func) -> None:
    with open("input.txt", "r", encoding="utf-8") as f:
        values = f.read().splitlines()

    values = [
        "029A",
        "980A",
        "179A",
        "456A",
        "379A",
    ]

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


class Controller:
    key_locations: list[list[str | int | None]] = [[]]

    def __init__(self):
        self.keys = deepcopy(self.key_locations)
        self.position = self.get_position("A")

    def _key_options(self) -> list[int | str]:
        """
        Get the keys that can be pressed
        """
        return [key for row in self.keys for key in row if key is not None]

    def get_position(self, key: int | str) -> list[int, int]:
        """
        Get the position of the key
        """
        for i, row in enumerate(self.keys):
            for j, k in enumerate(row):
                if k == key:
                    return [i, j]

    def press(self, key: int | str) -> str:
        """
        Get the sequence of moves to press the key.
        """
        assert len(str(key)) == 1, "Invalid key length"
        assert key in self._key_options(), f"Invalid key: {key}, options:{self._key_options()}"
        result = ""
        target = self.get_position(key)
        while self.position != target:
            if self.position[0] < target[0]:
                result += "v"
                self.position[0] += 1
            elif self.position[0] > target[0]:
                result += "^"
                self.position[0] -= 1
            elif self.position[1] < target[1]:
                result += ">"
                self.position[1] += 1
            elif self.position[1] > target[1]:
                result += "<"
                self.position[1] -= 1

        return result

    def press_combination(self, combination: str) -> str:
        """
        Get the sequence of moves to press the combination
        """
        result = ""
        for key in combination:
            if key.isnumeric():
                key = int(key)
            result += self.press(key)
            result += "A"
        return result


class Numpad(Controller):
    key_locations = [
        [7, 8, 9],
        [4, 5, 6],
        [1, 2, 3],
        [None, 0, "A"]
    ]


class Directional(Controller):
    key_locations = [
        [None, "^", "A"],
        ["<", "v", ">"],
    ]


def get_personal_input(code: str) -> str:
    numpad = Numpad()
    directionals = [
        Directional(),
        Directional(),
    ]
    keys = numpad.press_combination(code)
    for d in directionals:
        keys = d.press_combination(keys)
    return keys


def main(values: list) -> None:
    # DOESN'T WORK, .press, doesn't optimise for nested key presses
    total = 0
    for value in values:
        keys = get_personal_input(value)
        print(keys)
        total += int(value[:-1]) * len(keys)
    return total


if __name__ == "__main__":
    display_output(main)
