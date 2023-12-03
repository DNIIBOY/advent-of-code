import requests
import time

session = ""

headers = {
    "Cookie": f"session={session}"
}


def get_url(prompt: bool = True) -> str:
    """
    Get the url for the input for the day
    :param prompt: Whether to prompt the user for the day
    :return: The url for the input
    """
    day = time.strftime("%d")
    year = time.strftime("%Y")
    if prompt:
        day = input("Day: ")
        year = input("Year: ")
    return f"https://adventofcode.com/{year}/day/{day}/input"


r = requests.get(get_url(prompt=False), headers=headers, timeout=1)
print(r)
