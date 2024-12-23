import pyperclip
from time import perf_counter


def display_output(func) -> None:
    with open("input.txt", "r", encoding="utf-8") as f:
        values = f.read().splitlines()

    # values = [
    #     "1",
    #     "10",
    #     "100",
    #     "2024"
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


def mix(secret: int, number: int) -> int:
    return secret ^ number


def prune(secret: int) -> int:
    return secret % 16777216


def get_next_secret(secret: int) -> int:
    new_secret = secret * 64
    new_secret = mix(new_secret, secret)
    new_secret = prune(new_secret)

    secret = new_secret
    new_secret = new_secret // 32
    new_secret = mix(new_secret, secret)
    new_secret = prune(new_secret)

    secret = new_secret
    new_secret = new_secret * 2048
    new_secret = mix(new_secret, secret)
    new_secret = prune(new_secret)

    return new_secret


def get_nth_secret(secret: int, n: int) -> int:
    for _ in range(n):
        secret = get_next_secret(secret)
    return secret


def main(values: list) -> None:
    seeds = list(map(int, values))
    return sum(get_nth_secret(seed, 2000) for seed in seeds)


if __name__ == "__main__":
    display_output(main)
