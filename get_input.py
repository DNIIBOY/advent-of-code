from rich import pretty
from rich.console import Console
from rich.prompt import IntPrompt
import shutil
import os
import requests
import time

SESSION_FILE = ".session"
console = Console()
pretty.install()


def get_date(prompt: bool = True) -> tuple[int, int]:
    """
    Get the data to use.
    :param prompt: Whether to prompt the user for the date.
    :return: The date as a tuple of (year, day)
    """
    day = int(time.strftime("%d"))
    year = int(time.strftime("%Y"))
    if prompt:
        day = IntPrompt.ask("Day: ", default=day)
        year = IntPrompt.ask("Year: ", default=year)
    return year, day


def get_url(year: int, day: int) -> str:
    """
    Get the url for the input for the day
    :param prompt: Whether to prompt the user for the day
    :return: The url for the input
    """
    return f"https://adventofcode.com/{year}/day/{day}/input"


def get_session() -> str:
    """
    Get the session cookie from the user or from the file.
    :return: The cookies as str
    """
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            session = f.read()
    else:
        session = ""

    if test_session(session):
        return session

    session = input("Session: ")
    if not test_session(session):
        return get_session()


def test_session(session: str) -> bool:
    """
    Test the session cookie.
    If the cookie is valid, it is saved to the file.
    :param session: The session cookie
    :return: Whether the session cookie is valid
    """
    headers = {
        "Cookie": f"session={session}"
    }
    response = requests.get("https://adventofcode.com/auth/login", headers=headers, timeout=1, allow_redirects=False)
    if response.status_code != 303:
        print("Invalid session cookie.")
        return False
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        f.write(session)
    return True


def create_dir(year: int, day: int) -> None:
    """
    Create the directory for the day.
    :param year: The year of the day
    :param day: The day
    """
    path = f"{year}/{day}"
    if not os.path.exists(path):
        os.makedirs(path)
    # Copy template.py to the directory
    shutil.copy("template.py", f"{path}/solve.py")


def get_input(year: int, day: int) -> str:
    """
    Get the input for the day.
    :param year: The year of the day
    :param day: The day
    :return: The input
    """
    headers = {
        "Cookie": f"session={get_session()}"
    }
    response = requests.get(get_url(year, day), headers=headers, timeout=5)
    return response.text


def save_input(year: int, day: int, input_value: str) -> None:
    """
    Save the input to a file.
    :param year: The year of the day
    :param day: The day
    :param input_value: The input
    """
    with open(f"{year}/{day}/input.txt", "w", encoding="utf-8") as f:
        f.write(input_value)


def main():
    year, day = get_date()
    create_dir(year, day)
    input_value = get_input(year, day)
    save_input(year, day, input_value)


if __name__ == "__main__":
    main()
