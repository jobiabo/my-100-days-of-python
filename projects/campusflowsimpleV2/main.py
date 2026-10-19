"""CampusFlow Pro - a text-based IT help desk ticket tracker.

Run with:  python helpdesk.py
Priority is worked out with plain Python rules (no AI involved).
"""

from actions import (assign_with_event, change_status_with_event,
                     create_with_event, escalate_overdue)
from config import CATEGORIES, DATA_FILE, URGENCIES
from history import check_operator, get_history, show_event
from knowledge_lab import run_quiz
from reports import sla_metrics, sla_queue
from sla import is_overdue, now_utc, to_time
from storage import load_data, save_data
from ticket_service import find_duplicates, find_ticket, report, work_queue
from validation import clean_choice, clean_title, clean_users

MENU = """
===== CampusFlow Pro Help Desk =====
1.  Create ticket
2.  Assign ticket
3.  Start / resolve / reopen
4.  Original Open Work Queue
5.  SLA Attention Queue
6.  Ticket history
7.  Check and escalate overdue
8.  Reports
9.  Save / load
10. Engineering Knowledge Lab
11. List all tickets
12. View one ticket
0.  Exit"""


# ---------- Asking the user ----------
# Each function asks again until the answer is valid.

def ask_title():
    while True:
        try:
            return clean_title(input("Title: "))
        except ValueError as error:
            print("  Error:", error)


def ask_category():
    while True:
        try:
            return clean_choice(input(f"Category ({'/'.join(CATEGORIES)}): "), CATEGORIES, "category")
        except ValueError as error:
            print("  Error:", error)


def ask_urgency():
    while True:
        try:
            return clean_choice(input(f"Urgency ({'/'.join(URGENCIES)}): "), URGENCIES, "urgency")
        except ValueError as error:
            print("  Error:", error)


def ask_users():
    while True:
        try:
            return clean_users(input("Affected users: "))
        except ValueError as error:
            print("  Error:", error)


def ask_operator():
    while True:
        try:
            return check_operator(input("Operator label (a name for the history, not a login): "))
        except ValueError as error:
            print("  Error:", error)


def ask_time():
    """Blank = use the current time. Or type a time like 2026-10-14T10:00:00+00:00."""
    while True:
        text = input("Time to check (Enter = now, or e.g. 2026-10-14T10:00:00+00:00): ")
        if text.strip() == "":
            return now_utc()
        try:
            return to_time(text)
        except ValueError as error:
            print("  Error:", error)


# ---------- Showing things ----------

def show_tickets(tickets):
    if not tickets:
        print("No tickets to show.")
        return
    print(f"{'ID':<6}{'Title':<28}{'Category':<10}{'Urgency':<8}{'Users':>5}  "
          f"{'Priority':<9}{'Status':<12}Assigned to")
    for t in tickets:
        assigned = t["assigned_to"] or "-"
        print(f"{t['id']:<6}{t['title'][:26]:<28}{t['category']:<10}{t['urgency']:<8}"
              f"{t['affected_users']:>5}  {t['priority']:<9}{t['status']:<12}{assigned}")


def show_sla_queue(tickets, now):
    queue = sla_queue(tickets, now)
    if not queue:
        print("No unresolved tickets.")
        return
    print(f"{'ID':<6}{'Priority':<10}{'Status':<13}{'Due (UTC)':<34}State")
    for t in queue:
        state = "** OVERDUE **" if is_overdue(t, now) else "on time"
        print(f"{t['id']:<6}{t['priority']:<10}{t['status']:<13}{t['due_at']:<34}{state}")


# ---------- One function per menu option ----------

def create_menu(tickets, events, operator):
    title = ask_title()
    category = ask_category()
    urgency = ask_urgency()
    users = ask_users()

    ticket = create_with_event(tickets, events, title, category, urgency, users, operator)
    if ticket is None:                               # duplicates were found
        ids = find_duplicates(tickets, category, title)
        print("Warning: unresolved ticket(s) with the same title and category:", ", ".join(ids))
        answer = input("Create it anyway? (yes/no): ").strip().lower()
        if answer != "yes":
            print("Cancelled. No ticket or event was created.")
            return False
        ticket = create_with_event(tickets, events, title, category, urgency, users,
                                   operator, allow_duplicate=True)
    print(f"Created {ticket['id']} with priority '{ticket['priority']}', due {ticket['due_at']}.")
    return True


def assign_menu(tickets, events, operator):
    ticket_id = input("Ticket ID: ")
    name = input("Assign to: ")
    ticket = assign_with_event(tickets, events, ticket_id, name, operator)
    print(f"{ticket['id']} assigned to {ticket['assigned_to']}.")


def status_menu(tickets, events, operator):
    ticket_id = input("Ticket ID: ")
    action = input("1 Start   2 Resolve   3 Reopen: ").strip()
    if action == "1":
        new_status = "in_progress"
    elif action == "2":
        new_status = "resolved"
    elif action == "3":
        new_status = "open"
    else:
        print("Invalid action. Enter 1, 2 or 3.")
        return False
    ticket = change_status_with_event(tickets, events, ticket_id, new_status, operator)
    print(f"{ticket['id']} is now {ticket['status']} (due {ticket['due_at']}).")
    return True


def history_menu(tickets, events):
    ticket = find_ticket(tickets, input("Ticket ID: "))
    history = get_history(events, ticket["id"])
    if not history:
        print("No history for", ticket["id"])
    for event in history:
        print(show_event(event))


def escalate_menu(tickets, events, operator):
    newly, already = escalate_overdue(tickets, events, ask_time(), operator)
    print(f"Newly escalated: {newly}. Already escalated: {already}.")


def reports_menu(tickets, events):
    now = ask_time()
    basic = report(tickets)
    m = sla_metrics(tickets, events, now)
    print("\nTotal tickets:", basic["total"])
    print(f"Open: {m['open']}   In progress: {m['in_progress']}   Resolved: {m['resolved']}")
    print(f"Overdue (unresolved): {m['overdue']}   Escalated in current cycle: {m['escalated']}")
    for priority, count in m["by_priority"].items():
        print(f"  {priority}: {count}")


def save_load_menu(tickets, events):
    action = input("1 Save now   2 Reload from file: ").strip()
    if action == "1":
        save_data(tickets, events, DATA_FILE)
        print("Saved.")
    elif action == "2":
        new_tickets, new_events = load_data(DATA_FILE)   # checked BEFORE we use it
        tickets[:] = new_tickets
        events[:] = new_events
        print(f"Loaded {len(tickets)} tickets and {len(events)} events.")
    else:
        print("Invalid action. Enter 1 or 2.")


def view_one_menu(tickets):
    t = find_ticket(tickets, input("Ticket ID: "))
    for field, value in t.items():
        print(f"  {field:<17}: {value if value is not None else '(unassigned)'}")


# ---------- Main loop ----------

def main():
    try:
        tickets, events = load_data(DATA_FILE)
    except ValueError as error:
        print("Error:", error)
        return                      # stop, so the file is never overwritten
    operator = ask_operator()

    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        changed = False             # did this option change any data?
        try:
            if choice == "0":
                print("Goodbye.")
                break
            elif choice == "1":
                changed = create_menu(tickets, events, operator)
            elif choice == "2":
                assign_menu(tickets, events, operator)
                changed = True
            elif choice == "3":
                changed = status_menu(tickets, events, operator)
            elif choice == "4":
                show_tickets(work_queue(tickets))
            elif choice == "5":
                show_sla_queue(tickets, ask_time())
            elif choice == "6":
                history_menu(tickets, events)
            elif choice == "7":
                escalate_menu(tickets, events, operator)
                changed = True
            elif choice == "8":
                reports_menu(tickets, events)
            elif choice == "9":
                save_load_menu(tickets, events)
            elif choice == "10":
                run_quiz()          # the quiz is never given the tickets
            elif choice == "11":
                show_tickets(tickets)
            elif choice == "12":
                view_one_menu(tickets)
            else:
                print("Invalid choice. Enter a number from the menu.")

            if changed:
                save_data(tickets, events, DATA_FILE)
        except ValueError as error:
            print("Error:", error)


if __name__ == "__main__":
    main()
