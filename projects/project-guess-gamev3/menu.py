"""Menu / banner display."""
from config import MAX_GUESSES, MAX_INVALID_INPUTS


def menupage() -> None:
    lines = [
        f"You have {MAX_INVALID_INPUTS} invalid input trials",
        f"You have {MAX_GUESSES} valid guess attempts",
    ]
    width = max(len(line) for line in lines) + 4
    print("====== Python Guess Game ======")
    print("-" * width)
    for line in lines:
        print(f"| {line.ljust(width - 4)} |")
    print("-" * width)
