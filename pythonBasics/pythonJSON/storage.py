import json

def list_and_view():
    with open("ticketstore.json", "r") as file:
        student = json.load(file)
        
    
    for x in student:
        print(x["id"], )