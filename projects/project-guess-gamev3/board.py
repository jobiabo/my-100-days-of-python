"""Core game loop."""
from config import MAX_GUESSES, MAX_INVALID_INPUTS
from userinput_validate import parse_int


def guess(secret: int, upper: int,
          max_guesses: int = MAX_GUESSES,
          max_invalid: int = MAX_INVALID_INPUTS,
          input_fn=input) -> bool:
    """Run one game round. Returns True if the player wins.

    Invalid inputs (non-integers or values outside 1..upper) are tracked
    separately from valid guesses; exhausting either budget loses the game.
    `input_fn` is injectable to make the loop testable.
    """
    guesses_used = 0
    invalid_used = 0

    while guesses_used < max_guesses:
        raw = input_fn("Enter your guess here: ")
        value = parse_int(raw)

        if value is None or not 1 <= value <= upper:
            invalid_used += 1
            remaining = max_invalid - invalid_used
            print(f"Invalid input: enter a whole number from 1 to {upper}.")
            if remaining <= 0:
                print(f"You gave {invalid_used} invalid inputs. You failed.")
                print(f"Computer won! The secret number was {secret}.")
                return False
            print(f"{remaining} invalid input trial(s) remaining.")
            continue

        guesses_used += 1

        if value == secret:
            print(f"Yay, you got the number {secret}! You won!")
            return True

        hint = "high" if value > secret else "low"
        remaining = max_guesses - guesses_used
        print(f"Not the number: {value} is too {hint}.")
        print(f"You have used {guesses_used} trial(s): {remaining} remaining.")

    print("You failed.")
    print(f"Computer won! The secret number was {secret}.")
    return False
