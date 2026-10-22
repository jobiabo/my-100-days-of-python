import json
import os
from config import FILEPATH

def load_databank():
    #  actual file path
    
    # 1. Check if file doesn't exist or is completely empty
    if not os.path.exists(FILEPATH) or os.path.getsize(FILEPATH) == 0:
        return []

    with open(FILEPATH, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            # 2. Fallback if the file contains invalid JSON text
            return []


def save_databank(databank):
    with open(FILEPATH, "w") as file:
        json.dump(databank, file, indent=4)
