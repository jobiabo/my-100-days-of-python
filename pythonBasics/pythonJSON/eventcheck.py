import os
import json

FILENAME = "eventstest.json"
def main():
    if not os.path.exists(FILENAME) or os.path.getsize == 0:
        return {}
    try:
        with open(FILENAME, "r", encoding="utf=8") as file:
            datajson = json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"{FILENAME} has an error ({e})")

    print(len(datajson))

main()