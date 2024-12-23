import pyperclip
from time import perf_counter


def display_output(func) -> None:
    with open("input.txt", "r", encoding="utf-8") as f:
        values = f.read().splitlines()

    # values = [
    #     "5,4",
    #     "4,2",
    #     "4,5",
    #     "3,0",
    #     "2,1",
    #     "6,3",
    #     "2,4",
    #     "1,5",
    #     "0,6",
    #     "3,3",
    #     "2,6",
    #     "5,1",
    #     "1,2",
    #     "5,5",
    #     "2,5",
    #     "6,5",
    #     "1,4",
    #     "0,4",
    #     "6,4",
    #     "1,1",
    #     "6,1",
    #     "1,0",
    #     "0,5",
    #     "1,6",
    #     "2,0",
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


def print_graph(graph: list, visited: list = None) -> None:
    if visited is None:
        visited = [[False] * len(graph) for _ in range(len(graph))]
    size = len(graph)
    for i in range(size):
        for j in range(size):
            if visited[j][i]:
                print("O", end="")
            else:
                print("." if graph[j][i] else "#", end="")
        print()


def parse(values: list[str]) -> list[tuple[int, int]]:
    return [tuple(map(int, value.split(","))) for value in values]


def corrupt_graph(graph: list, values: list) -> None:
    for x, y in values:
        graph[x][y] = False


def shortest_path(graph: list) -> int:
    """
    Find the shortest path from the top-left corner to the bottom-right corner,
    moving only up, down, left, and right.
    Uses breadth-first search.
    :param graph: a 2D list of booleans, True means the cell is open, False means it's blocked
    :return: the length of the shortest path
    """
    size = len(graph)
    visited = [[False] * size for _ in range(size)]
    visited[0][0] = True
    queue = [(0, 0, 0)]
    while queue:
        x, y, steps = queue.pop(0)
        if x == size - 1 and y == size - 1:
            return steps
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < size and 0 <= new_y < size and graph[new_x][new_y] and not visited[new_x][new_y]:
                visited[new_x][new_y] = True
                queue.append((new_x, new_y, steps + 1))


def main(values: list, corrupted_count: int = 12) -> None:
    # size = 7
    size = 71
    graph = [[True] * size for _ in range(size)]
    values = parse(values)
    corrupt_graph(graph, values[:corrupted_count])
    return shortest_path(graph)


def part_2(values: list) -> int:
    corrupted_count = 1024
    while main(values, corrupted_count) is not None:
        corrupted_count += 1
    return values[corrupted_count - 1]


if __name__ == "__main__":
    display_output(part_2)
