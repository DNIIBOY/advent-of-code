import pyperclip
from time import perf_counter


def display_output(func) -> None:
    with open("input.txt", "r", encoding="utf-8") as f:
        value = f.read().strip()
    # value = "2333133121414131402"

    start = perf_counter()
    result = func(value)
    end = perf_counter()
    print(f"--- Got result in {end-start:.4f}s---")
    print(result)
    try:
        pyperclip.copy(result)
        print("--- Copied to clipboard ---")
    except FileNotFoundError:
        pass


def create_disk(disk_map: str) -> list:
    is_gap = False
    disk = []
    block_id = 0
    for num in disk_map:
        num = int(num)
        if is_gap:
            disk.extend(["."]*num)
        else:
            disk.extend([block_id]*num)
            block_id += 1
        is_gap = not is_gap
    return disk


def arrange_blocks(disk: list) -> str:
    i = 0
    j = len(disk)-1
    while i < j:
        if disk[i] != ".":
            i += 1
            continue
        if disk[j] == ".":
            j -= 1
            continue
        disk[i], disk[j] = disk[j], disk[i]
    return disk


def arrange_files(disk: list) -> str:
    i = len(disk) - 1
    start = i
    num = None

    while i > 0:
        if disk[i] != num and num is not None:
            length = i - start
            l = 0
            j = 0
            while j < i:
                if disk[j] == ".":
                    l += 1
                    j += 1
                else:
                    l = 0
                if l == length:
                    break
            disk[j-length:j] = disk[start:start+length]
        if disk[i] == ".":
            i -= 1
            continue
        num = disk[i]
        start = i
        i -= 1
    return disk


def checksum(disk: list) -> int:
    val = 0
    for i, char in enumerate(disk):
        if char == ".":
            return val
        val += i * char
    return val


def main(value: str) -> None:
    disk = create_disk(value)
    arranged = arrange_files(disk)
    return checksum(arranged)


if __name__ == "__main__":
    display_output(main)
