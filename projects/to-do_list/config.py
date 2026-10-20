FILEPATH = "taskstore.json"

CONTENTS = {
    "ID": "",
    "TITLE": "",
    "CREATED_AT": "",
    "STATUS": "",
    "COMPLETED_AT": "",
}

def heading():
    MENU = """1. VIEW ALL TASKS\n2. ADD TASK\n3. SHOW INCOMPLETED TASKS\n4. SHOW COMPLETED TASKS\n5. MARK TASK AS COMPLETED\n6. MARK TASK AS INCOMPLETED"""

    print("="*100)
    print(" "* 40 ,"CLI TASK MANAGER")
    print("="*100)
    print("Please select with a corresponding option(1-4):")
    print(MENU)



