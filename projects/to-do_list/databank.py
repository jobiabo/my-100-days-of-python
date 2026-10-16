import json
import os

def load_databank():
    file_path = "taskstore.json"  # Replace with your actual file path
    
    # 1. Check if file doesn't exist or is completely empty
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return {}  # Or [] depending on your structure

    with open(file_path, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            # 2. Fallback if the file contains invalid JSON text
            return {}  # Or []
