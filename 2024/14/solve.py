import pyperclip
from time import perf_counter
import re


def display_output(func) -> None:
    with open("input.txt", "r", encoding="utf-8") as f:
        values = f.read().splitlines()

    # values = [
    #     "p=0,4 v=3,-3",
    #     "p=6,3 v=-1,-3",
    #     "p=10,3 v=-1,2",
    #     "p=2,0 v=2,-1",
    #     "p=0,0 v=1,3",
    #     "p=3,0 v=-2,-2",
    #     "p=7,6 v=-1,-3",
    #     "p=3,0 v=-1,-2",
    #     "p=9,3 v=2,3",
    #     "p=7,3 v=-1,2",
    #     "p=2,4 v=2,-3",
    #     "p=9,5 v=-3,-3",
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


class Robot:
    def __init__(self, position: tuple[int, int], velocity: tuple[int, int]) -> None:
        self.position = position
        self.velocity = velocity

    @classmethod
    def from_string(cls, string: str) -> "Robot":
        values = re.match(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", string)
        position = (int(values.group(1)), int(values.group(2)))
        velocity = (int(values.group(3)), int(values.group(4)))
        return cls(position, velocity)

    def move(self, room_size: tuple[int, int]) -> None:
        self.position = (
            (self.position[0] + self.velocity[0]) % room_size[0],
            (self.position[1] + self.velocity[1]) % room_size[1],
        )

    def __repr__(self) -> str:
        return f"Robot({self.position}, {self.velocity})"


def count_quadrants(robots: list[Robot], room_size: tuple[int, int]) -> int:
    quadrants = [0 for _ in range(4)]
    for robot in robots:
        if robot.position[0] < room_size[0] // 2:
            if robot.position[1] < room_size[1] // 2:
                quadrants[0] += 1
            elif robot.position[1] > room_size[1] // 2:
                quadrants[2] += 1
        elif robot.position[0] > room_size[0] // 2:
            if robot.position[1] < room_size[1] // 2:
                quadrants[1] += 1
            elif robot.position[1] > room_size[1] // 2:
                quadrants[3] += 1
    return quadrants


def display_room(robots: list[Robot], room_size: tuple[int, int]) -> None:
    room = [[0 for _ in range(room_size[0])] for _ in range(room_size[1])]
    for robot in robots:
        room[robot.position[1]][robot.position[0]] += 1
    for row in room:
        for cell in row:
            if cell == 0:
                print(".", end="")
            else:
                print(cell, end="")
        print()


def main(values: list) -> None:
    # room_size = (11, 7)
    room_size = (101, 103)
    robots = [Robot.from_string(value) for value in values]
    for _ in range(100):
        for robot in robots:
            robot.move(room_size)

    quadrants = count_quadrants(robots, room_size)
    product = quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]
    return product


def easter_egg(values: list) -> None:
    from time import sleep
    room_size = (101, 103)
    robots = [Robot.from_string(value) for value in values]
    i = 0
    while True:
        i += 1
        for robot in robots:
            robot.move(room_size)
        display_room(robots, room_size)
        print(f"Cycles: {i}: ")
        sleep(0.1)


if __name__ == "__main__":
    display_output(main)
    # display_output(easter_egg)
