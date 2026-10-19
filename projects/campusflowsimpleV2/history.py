"""The event history (audit trail). Events are only ever added, never edited."""

from sla import to_time


def check_operator(name):
    """The operator label is just a name for tracking. It is not a login."""
    name = " ".join(str(name).split())
    if name == "":
        raise ValueError("Operator label must not be blank.")
    return name


def add_event(events, ticket_id, event_type, operator, when, before_status, after_status, details):
    """Add one event to the end of the list. 'when' is a datetime."""
    event = {
        "event_id": f"E{len(events) + 1:03d}",   # events are never deleted, so this is unique
        "ticket_id": ticket_id,
        "event_type": event_type,                # CREATE, ASSIGN, START, RESOLVE, REOPEN, ESCALATE
        "actor": check_operator(operator),
        "timestamp": when.isoformat(),
        "before_status": before_status,
        "after_status": after_status,
        "details": details,
    }
    events.append(event)
    return event


def sort_key(event):
    return (to_time(event["timestamp"]), int(event["event_id"][1:]))


def get_history(events, ticket_id):
    """Events of one ticket, oldest first (same time -> lower event_id first)."""
    mine = [e for e in events if e["ticket_id"] == str(ticket_id).strip().upper()]
    return sorted(mine, key=sort_key)


def show_event(e):
    before = e["before_status"] or "-"
    return (f"{e['event_id']}  {e['timestamp']}  {e['event_type']:<8}  "
            f"{before} -> {e['after_status']}  by {e['actor']}  {e['details']}")
