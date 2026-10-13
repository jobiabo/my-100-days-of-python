"""Validation of the game's upper range."""
from typing import Optional

from config import MAX_RANGE, MIN_RANGE
from userinput_validate import parse_int


def inrangenumber(raw: str, minimum: int = MIN_RANGE,
                  maximum: int = MAX_RANGE) -> Optional[int]:
    """Return the range as an int if valid and within [minimum, maximum],
    otherwise print a helpful message and return None."""
    value = parse_int(raw)
    if value is None:
        print("Please enter a valid whole number.")
        return None
    if not minimum <= value <= maximum:
        print(f"Range must be between {minimum} and {maximum}.")
        return None
    return value
