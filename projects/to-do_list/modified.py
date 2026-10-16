from databank import load_databank
from clock import time_stamp

def mark_complete():
    current_id = input("Enter task ID to mark as complete: ")
    databank = load_databank()
    for x in databank:
        if current_id == x["ID"]:
            x["STATUS"] = "completed" 
            x['COMPLETED_AT'] = time_stamp()
            print(
            f"{x['ID']:<15}"
            f"{x['TITLE']:<25}"
            f"{x['CREATED_AT']:<22}"
            f"{x['STATUS']:<15}"
            f"{x['COMPLETED_AT'] or 'N/A':<20}"
        )
        else:
            print("Task ID mismatch")
            return

