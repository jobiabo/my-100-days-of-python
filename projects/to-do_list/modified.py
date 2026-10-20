from databank import load_databank
from clock import time_stamp


def mark_complete():
    current_id = input("Enter task ID to mark as complete: ").upper()
    data_bank = load_databank()

    for x in data_bank:
        if current_id == x['ID']:
            if x['STATUS'] == "just created" or x['STATUS'] == "incompleted":
                x["STATUS"] = "completed" 
                x['COMPLETED_AT'] = time_stamp()
                print(
                f"{x['ID']:<15}"
                f"{x['TITLE']:<25}"
                f"{x['CREATED_AT']:<22}"
                f"{x['STATUS']:<15}"
                f"{x['COMPLETED_AT'] or 'N/A':<20}"
            )
            
                from databank import save_databank
                save_databank(data_bank)
                print(f" Ticket ID {x["ID"]} has been marked {x["STATUS"]} successfully")        
                return
            elif x['STATUS'] == "completed":
                print(f"Task already completed as at {x["COMPLETED_AT"]}")
                return
    else:
        print("Task ID mismatch")

def mark_incomplete():
    current_id = input("Enter task ID to mark as complete: ").upper()
    data_bank = load_databank()

    for x in data_bank:
            if current_id == x['ID']:
                if x['STATUS'] == "incompleted":
                    print(f"TASK {x['ID']} is still active as incomplete as at {x['CREATED_AT']}")
                    return
                elif x['STATUS'] == "just created" or x['STATUS'] == "completed":
                    x['STATUS'] = "incompleted"
                    x['CREATED_AT'] = time_stamp()
                    x['COMPLETED_AT'] = ""
                    print(
                    f"{x['ID']:<15}"
                    f"{x['TITLE']:<25}"
                    f"{x['CREATED_AT']:<22}"
                    f"{x['STATUS']:<15}"
                    f"{x['COMPLETED_AT'] or 'N/A':<20}"
                    
                    ) 
                    from databank import save_databank
                    save_databank(data_bank)
                    print(f" Ticket ID {x["ID"]} has been marked {x["STATUS"]} successfully")        
                    return
    else:
        print("Task ID mismatch")
