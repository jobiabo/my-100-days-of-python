import json

def list_and_view():
    with open("ticketstore.json", "r") as file:
        student = json.load(file)
        
    print("===================================")
    print("ID    Ticket Title")
    print("===================================")


    for x in student:
        
        print(x["id"], x["title"])
    print("===================================")
    print("please enter specific ticket ID to view more details")        
    print("===================================")

