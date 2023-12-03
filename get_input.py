import os
import requests
import time

SESSION_FILE = ".session"


def get_url(prompt: bool = True) -> str:
    """
    Get the url for the input for the day
    :param prompt: Whether to prompt the user for the day
    :return: The url for the input
    """
    day = int(time.strftime("%d"))
    year = int(time.strftime("%Y"))
    if prompt:
        day = input("Day: ")
        year = input("Year: ")
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
    response = requests.get(get_url(prompt=False), headers=headers, timeout=1)
    if response.status_code != 200:
        print("Invalid session cookie.")
        return False
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        f.write(session)
    return True


def main():
    headers = {
        "Cookie": f"session={get_session()}"
    }


if __name__ == "__main__":
    main()
