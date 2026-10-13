"""Input validation helpers."""
from typing import Optional


def parse_int(user_input: str) -> Optional[int]:
    """Return the integer value of `user_input`, or None if it isn't a
    plain non-negative ASCII integer (e.g. rejects '', '-3', '1.5', '²')."""
    text = user_input.strip()
    if text.isascii() and text.isdigit():
        return int(text)
    return None


def validate(user_input: str) -> bool:
    """True if `user_input` is a valid non-negative integer string."""
    return parse_int(user_input) is not None
