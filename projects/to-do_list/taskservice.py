from databank import load_databank
from clock import time_stamp
import json

def create_id():
    
    databank = load_databank()
    if len(databank) == 0:
        max_id = 0
        return f"T{max_id+1:03d}"
    else:
        lastIindex = len(databank)-1
        lastitem = databank[lastIindex]
        lastid = int(lastitem["ID"][1:])
        return f"T{lastid+1:03d}"



def create_task(title):
    from config import CONTENTS
    taskdata = CONTENTS.copy()

    taskdata["ID"] = create_id()
    taskdata["TITLE"] = title
    taskdata["CREATED_AT"] = time_stamp()
    taskdata["STATUS"] = "just created"
    

    with open("taskstore.json", "w") as file:
        json.dump(taskdata, file, indent=4)
    print("Tasks created successfully")

def view_all_tasks():
    databank = load_databank()

    print("=" * 100)
    print(
        f"{'TICKET_ID':<15}"
        f"{'TITLE':<25}"
        f"{'CREATED_AT':<22}"
        f"{'STATUS':<15}"
        f"{'COMPLETED_AT':<20}"
    )
    print("=" * 100)
    if not load_databank():
        print("no task created yet")
    for x in databank:
        print(
            f"{x['ID']:<15}"
            f"{x['TITLE']:<25}"
            f"{x['CREATED_AT']:<22}"
            f"{x['STATUS']:<15}"
            f"{x['COMPLETED_AT'] or 'N/A':<20}"
        )

    print("=" * 100)





