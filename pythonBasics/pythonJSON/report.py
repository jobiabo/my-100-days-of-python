import json

def report():
    # Breakdown by status
    open_tickets = 0
    in_progress_ticket = 0
    closed_tickets = 0
    with open("ticketstore.json", "r") as file:
        tickets = json.load(file)
        print("Total Tickets Logged:",len(tickets))
        # print(tickets)

        
        for ticketDetails in tickets:
            
            
            if  ticketDetails["id"] == "open":
                open_tickets=+1

        # Breakdown by priority
        low_priority = 0
        medium_priority = 0
        high_priority = 0

report()