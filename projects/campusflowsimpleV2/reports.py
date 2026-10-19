"""Read-only views of the tickets. Nothing here changes any data."""

from actions import already_escalated
from config import PRIORITIES
from sla import is_overdue, now_utc, to_time


def sla_sort_key(ticket, now):
    overdue_first = 0 if is_overdue(ticket, now) else 1       # 0 sorts before 1
    return (overdue_first, to_time(ticket["due_at"]), int(ticket["id"][1:]))


def sla_queue(tickets, now=None):
    """Unresolved tickets: overdue first, then earliest due_at, then ticket number."""
    if now is None:
        now = now_utc()
    pending = [t for t in tickets if t["status"] != "resolved"]
    return sorted(pending, key=lambda t: sla_sort_key(t, now))


def sla_metrics(tickets, events, now=None):
    if now is None:
        now = now_utc()
    result = {"open": 0, "in_progress": 0, "resolved": 0,
              "overdue": 0, "escalated": 0,
              "by_priority": {p: 0 for p in PRIORITIES}}
    for t in tickets:                      # each ticket is looked at once
        result[t["status"]] += 1
        result["by_priority"][t["priority"]] += 1
        if t["status"] != "resolved":
            if is_overdue(t, now):
                result["overdue"] += 1
            if already_escalated(events, t):
                result["escalated"] += 1
    return result
