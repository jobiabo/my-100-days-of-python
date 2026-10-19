"""Saving and loading tickets as JSON."""

import json
import os

from config import DATA_FILE, FIELDS


def save_tickets(tickets, path=DATA_FILE):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tickets, f, indent=2)


def load_tickets(path=DATA_FILE):
    if not os.path.exists(path):
        return []                      # no file yet: fresh start
    try:
        with open(path, encoding="utf-8") as f:
            tickets = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"'{path}' is not valid JSON ({e}). The file was not "
                         "changed; fix or move it, then restart.")
    if not isinstance(tickets, list) or not all(
            isinstance(t, dict) and t.keys() >= set(FIELDS) for t in tickets):
        raise ValueError(f"'{path}' does not contain valid ticket data. "
                         "The file was not changed.")
    return tickets


# ---------- Version 2 file: tickets + events together ----------

from config import SCHEMA_VERSION, STATUSES, PRIORITIES
from sla import to_time

TICKET_KEYS = FIELDS + ["created_at", "updated_at", "due_at", "escalation_cycle"]
EVENT_KEYS = ["event_id", "ticket_id", "event_type", "actor", "timestamp",
              "before_status", "after_status", "details"]


def check_data(data):
    """Raise ValueError if the loaded data is wrong. Does not change anything."""
    if not isinstance(data, dict) or data.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("File is not in the version 2 format (schema_version 2).")
    tickets = data.get("tickets")
    events = data.get("events")
    if not isinstance(tickets, list) or not isinstance(events, list):
        raise ValueError("'tickets' and 'events' must both be lists.")

    ticket_ids = []
    for t in tickets:
        if not isinstance(t, dict) or not set(TICKET_KEYS) <= set(t):
            raise ValueError("A ticket is missing required fields.")
        if t["status"] not in STATUSES or t["priority"] not in PRIORITIES:
            raise ValueError(f"Ticket {t['id']} has a wrong status or priority.")
        if t["id"] in ticket_ids:
            raise ValueError(f"Ticket ID {t['id']} appears twice.")
        ticket_ids.append(t["id"])
        for key in ("created_at", "updated_at", "due_at"):
            to_time(t[key])                      # raises ValueError if bad

    event_ids = []
    for e in events:
        if not isinstance(e, dict) or not set(EVENT_KEYS) <= set(e):
            raise ValueError("An event is missing required fields.")
        if e["event_id"] in event_ids:
            raise ValueError(f"Event ID {e['event_id']} appears twice.")
        event_ids.append(e["event_id"])
        if e["ticket_id"] not in ticket_ids:
            raise ValueError(f"Event {e['event_id']} points to an unknown ticket.")
        to_time(e["timestamp"])
    return tickets, events


def save_data(tickets, events, path=DATA_FILE):
    """Write to a temporary file first, then swap it in. If writing fails,
    the old file is still safe."""
    data = {"schema_version": SCHEMA_VERSION, "tickets": tickets, "events": events}
    check_data(data)                             # never save bad data
    temp_path = path + ".tmp"
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(temp_path, path)


def load_data(path=DATA_FILE):
    """Returns (tickets, events). A missing file means a fresh start."""
    if not os.path.exists(path):
        return [], []
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"'{path}' is not valid JSON ({e}). The file was not changed.")
    return check_data(data)
