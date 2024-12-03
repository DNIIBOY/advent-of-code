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


def eval_report(report: list) -> int | None:
    start = report[0]
    if report[1] > start:
        dir = "inc"
    else:
        dir = "dec"

    for i, num in enumerate(report):
        if i == 0:
            continue
        prev = report[i-1]

        if abs(num - prev) > 3:
            return i-1

        if dir == "inc":
            if num <= prev:
                return i - 1
        else:
            if num >= prev:
                return i-1

    return None


def main(reports: list) -> None:
    safe_count = 0
    for report in reports:
        report = list(map(int, report.split()))

        fail = eval_report(report)
        if not fail:
            safe_count += 1

    return safe_count


def main2(reports: list) -> None:
    safe_count = 0
    for report in reports:
        report = list(map(int, report.split()))

        fail = eval_report(report)
        if fail:
            report.pop(fail)
            fail = eval_report(report)
            if not fail:
                safe_count += 1
        else:
            safe_count += 1

    return safe_count


if __name__ == "__main__":
    display_output(main2)
