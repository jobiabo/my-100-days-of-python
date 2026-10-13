"""Entry point for the Python guess game."""
import random
import sys

from board import guess
from config import MAX_RANGE, MIN_RANGE
from menu import menupage
from rangeint import inrangenumber


def main() -> int:
    menupage()
    print(f"Range should be between {MIN_RANGE} and {MAX_RANGE}.")
    upper = inrangenumber(input("Please enter end range: "))
    if upper is None:
        print("Invalid range. Restart session.")
        return 1

    secret = random.randint(1, upper)
    print(f"I'm thinking of a number between 1 and {upper}.")
    guess(secret, upper)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (KeyboardInterrupt, EOFError):
        print("\nGame cancelled.")
        sys.exit(130)
