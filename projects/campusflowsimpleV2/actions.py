"""Ticket actions that also write to the event history.

Every action follows the same three steps:
  1. check the input and run the ORIGINAL ticket function (it raises an error
     BEFORE changing anything if the action is not allowed)
  2. update the timestamps
  3. add the event
If step 1 fails, steps 2 and 3 never run, so a rejected action leaves the
tickets and the events exactly as they were.
"""

from history import add_event, check_operator
from sla import is_overdue, make_due_at, now_utc, to_text
from ticket_service import (assign_ticket, change_status, create_ticket,
                            find_duplicates, find_ticket)

# Moving INTO a status -> name of the event
EVENT_FOR_STATUS = {"in_progress": "START", "resolved": "RESOLVE", "open": "REOPEN"}


def create_with_event(tickets, events, title, category, urgency, users, operator,
                      now=None, allow_duplicate=False):
    """Returns the new ticket, or None if duplicates exist and were not allowed."""
    operator = check_operator(operator)
    if now is None:
        now = now_utc()
    if not allow_duplicate and find_duplicates(tickets, category, title):
        return None
    ticket = create_ticket(tickets, title, category, urgency, users, now)
    add_event(events, ticket["id"], "CREATE", operator, now, None, "open",
              f"Created with priority {ticket['priority']}")
    return ticket


def assign_with_event(tickets, events, ticket_id, name, operator, now=None):
    operator = check_operator(operator)
    if now is None:
        now = now_utc()
    ticket = find_ticket(tickets, ticket_id)
    status = ticket["status"]
    assign_ticket(tickets, ticket_id, name)        # raises if not allowed
    ticket["updated_at"] = to_text(now)
    add_event(events, ticket["id"], "ASSIGN", operator, now, status, status,
              f"Assigned to {ticket['assigned_to']}")
    return ticket


def change_status_with_event(tickets, events, ticket_id, new_status, operator, now=None):
    operator = check_operator(operator)
    if now is None:
        now = now_utc()
    ticket = find_ticket(tickets, ticket_id)
    old_status = ticket["status"]
    change_status(tickets, ticket_id, new_status)  # raises if not allowed
    ticket["updated_at"] = to_text(now)
    details = f"{old_status} -> {new_status}"
    if new_status == "open":                       # reopened: start a NEW SLA cycle
        ticket["due_at"] = make_due_at(ticket["priority"], now)
        ticket["escalation_cycle"] += 1
        details += f" (new SLA cycle {ticket['escalation_cycle']})"
    add_event(events, ticket["id"], EVENT_FOR_STATUS[new_status], operator, now,
              old_status, new_status, details)
    return ticket


# ---------- Escalation ----------

def escalation_text(cycle):
    """The details text of an ESCALATE event. Also used to find earlier ones."""
    return f"Overdue in SLA cycle {cycle}"


def already_escalated(events, ticket):
    for e in events:
        if (e["ticket_id"] == ticket["id"] and e["event_type"] == "ESCALATE"
                and e["details"] == escalation_text(ticket["escalation_cycle"])):
            return True
    return False


def escalate_overdue(tickets, events, now=None, operator="system"):
    """One ESCALATE event per overdue ticket per SLA cycle.
    Returns (newly escalated, already escalated)."""
    operator = check_operator(operator)
    if now is None:
        now = now_utc()
    newly = 0
    already = 0
    for ticket in tickets:
        if not is_overdue(ticket, now):
            continue
        if already_escalated(events, ticket):
            already += 1
        else:
            add_event(events, ticket["id"], "ESCALATE", operator, now,
                      ticket["status"], ticket["status"],
                      escalation_text(ticket["escalation_cycle"]))
            newly += 1
    return newly, already
