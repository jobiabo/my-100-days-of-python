from databank import load_databank, save_databank
from clock import time_stamp
import json
from config import FILEPATH


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

def is_duplicate(title):
    title = title.strip()
    databank = load_databank()

    for task in databank:
        if task["TITLE"] == title and task["STATUS"] in (
            "just created",
            "incompleted",
        ):
            return True
    return False

def create_task(title):
    from config import CONTENTS
    new_task = CONTENTS.copy()
    databank = load_databank()

    if is_duplicate(title):
        print(  f"Task match found with same title {title}\n" 
                f"would you love to continue creating a new task with {title}"
            )
        userchoice = input("yes or no: ").lower()
        if userchoice == "yes":
            new_task["ID"] = create_id()
            new_task["TITLE"] = title
            new_task["CREATED_AT"] = time_stamp()
            new_task["STATUS"] = "just created"
            
            databank.append(new_task)
            save_databank(databank)
            print("Task created successfully")

        else:
            return None
    if not is_duplicate(title):
        new_task["ID"] = create_id()
        new_task["TITLE"] = title
        new_task["CREATED_AT"] = time_stamp()
        new_task["STATUS"] = "just created"
        
        databank.append(new_task)
        save_databank(databank)
        print("Task created successfully")




def view_all_tasks():
    databank = load_databank()

    print("=" * 100)
    print(
        f"{'TASK_ID':<15}"
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

def show_completed():
    databank = load_databank()

    # Filter completed tasks
    completed_tasks = [
        task for task in databank
        if task["STATUS"] == "completed"
    ]

    if not completed_tasks:
        print("No completed tasks found.")
        return

    # Print headings once
    print("=" * 100)
    print(
        f"{'TASK_ID':<15}"
        f"{'TITLE':<25}"
        f"{'CREATED_AT':<22}"
        f"{'STATUS':<15}"
        f"{'COMPLETED_AT':<20}"
    )
    print("=" * 100)

    # Display completed tasks
    for task in completed_tasks:
        print(
            f"{task['ID']:<15}"
            f"{task['TITLE']:<25}"
            f"{task['CREATED_AT']:<22}"
            f"{task['STATUS']:<15}"
            f"{task.get('COMPLETED_AT', 'N/A'):<20}"
        )

    print("=" * 100)


def show_incompleted():
    databank = load_databank()

    # Filter tasks by status
    incomplete_tasks = [
        task for task in databank
        if task["STATUS"] in ("incompleted", "just created")
    ]

    # Handle the case where no matching tasks exist
    if not incomplete_tasks:
        print("No incomplete or newly created tasks found.")
        return

    # Print headings once
    print("=" * 100)
    print(
        f"{'TASK_ID':<15}"
        f"{'TITLE':<25}"
        f"{'CREATED_AT':<22}"
        f"{'STATUS':<15}"
        f"{'COMPLETED_AT':<20}"
    )
    print("=" * 100)

    # Print each matching task
    for task in incomplete_tasks:
        print(
            f"{task['ID']:<15}"
            f"{task['TITLE']:<25}"
            f"{task['CREATED_AT']:<22}"
            f"{task['STATUS']:<15}"
            f"{task.get('COMPLETED_AT', 'N/A'):<20}"
        )

    print("=" * 100)

            
    





