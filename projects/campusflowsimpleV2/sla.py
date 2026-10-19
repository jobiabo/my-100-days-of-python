"""Time rules for tickets: due dates and overdue checks.

All times are in UTC and stored as text, e.g. "2026-10-14T10:00:00+00:00".
Functions that need the current time take an optional 'now' value. If you
leave it out they use the real clock. Tests pass a fixed 'now' so they do
not have to wait.
"""

from datetime import datetime, timedelta, timezone

from config import SLA_MINUTES


def now_utc():
    return datetime.now(timezone.utc)


def to_text(moment):
    """datetime -> text."""
    return moment.isoformat()


def to_time(text):
    """text -> datetime. The text must include a timezone like +00:00."""
    try:
        moment = datetime.fromisoformat(str(text).strip())
    except ValueError:
        raise ValueError(f"'{text}' is not a valid time. Example: 2026-10-14T10:00:00+00:00")
    if moment.tzinfo is None:
        raise ValueError(f"'{text}' has no timezone. Example: 2026-10-14T10:00:00+00:00")
    return moment


def make_due_at(priority, start_time):
    """Due time = start of the SLA cycle + minutes allowed for the priority."""
    return to_text(start_time + timedelta(minutes=SLA_MINUTES[priority]))


def is_overdue(ticket, now=None):
    """Overdue only if NOW is strictly later than due_at and not resolved."""
    if now is None:
        now = now_utc()
    if ticket["status"] == "resolved":
        return False
    return now > to_time(ticket["due_at"])
