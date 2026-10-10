import json

def list_and_view():
    with open("ticketstore.json", "r") as file:
        student = json.load(file)
        return student["id"]