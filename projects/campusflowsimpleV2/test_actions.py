import unittest
from datetime import datetime, timedelta, timezone

from actions import (assign_with_event, change_status_with_event,
                     create_with_event, escalate_overdue)
from history import get_history
from ticket_service import find_duplicates

START = datetime(2026, 10, 14, 10, 0, tzinfo=timezone.utc)


def minutes_later(n):
    return START + timedelta(minutes=n)


def new_ticket(tickets, events, title="Wi-Fi down", urgency="low", users=1, **extra):
    return create_with_event(tickets, events, title, "Network", urgency, users,
                             "ada", now=START, **extra)


class EventTests(unittest.TestCase):
    def test_full_life_of_a_ticket_makes_five_events(self):
        tickets, events = [], []
        new_ticket(tickets, events)
        assign_with_event(tickets, events, "T001", "Bob", "ada", minutes_later(1))
        change_status_with_event(tickets, events, "T001", "in_progress", "bob", minutes_later(2))
        change_status_with_event(tickets, events, "T001", "resolved", "bob", minutes_later(3))
        change_status_with_event(tickets, events, "T001", "open", "ada", minutes_later(4))
        shown = [(e["event_id"], e["event_type"], e["before_status"], e["after_status"])
                 for e in get_history(events, "T001")]
        self.assertEqual(shown, [("E001", "CREATE", None, "open"),
                                 ("E002", "ASSIGN", "open", "open"),
                                 ("E003", "START", "open", "in_progress"),
                                 ("E004", "RESOLVE", "in_progress", "resolved"),
                                 ("E005", "REOPEN", "resolved", "open")])

    def test_rejected_actions_change_nothing(self):
        tickets, events = [], []
        new_ticket(tickets, events)
        tickets_before = [dict(t) for t in tickets]
        events_before = [dict(e) for e in events]
        bad_calls = [
            lambda: change_status_with_event(tickets, events, "T001", "in_progress", "ada"),  # unassigned
            lambda: change_status_with_event(tickets, events, "T001", "resolved", "ada"),     # skips a step
            lambda: assign_with_event(tickets, events, "T999", "Bob", "ada"),                 # no such ticket
            lambda: assign_with_event(tickets, events, "T001", "Bob", "   "),                 # blank operator
        ]
        for call in bad_calls:
            with self.assertRaises(ValueError):
                call()
        self.assertEqual(tickets, tickets_before)
        self.assertEqual(events, events_before)

    def test_reopen_starts_a_new_sla_cycle(self):
        tickets, events = [], []
        new_ticket(tickets, events, urgency="high", users=10)      # critical: 60 minutes
        ticket = tickets[0]
        assign_with_event(tickets, events, "T001", "Bob", "ada", minutes_later(10))
        change_status_with_event(tickets, events, "T001", "in_progress", "bob", minutes_later(20))
        change_status_with_event(tickets, events, "T001", "resolved", "bob", minutes_later(30))
        events_before = [dict(e) for e in events]
        change_status_with_event(tickets, events, "T001", "open", "ada", minutes_later(500))
        self.assertEqual(ticket["created_at"], START.isoformat())             # unchanged
        self.assertEqual(ticket["due_at"], minutes_later(560).isoformat())    # new cycle
        self.assertEqual(ticket["escalation_cycle"], 1)
        self.assertEqual(events[:len(events_before)], events_before)          # old events intact

    def test_reopened_ticket_can_be_escalated_again(self):
        tickets, events = [], []
        new_ticket(tickets, events, urgency="high", users=10)
        escalate_overdue(tickets, events, minutes_later(61), "ada")
        assign_with_event(tickets, events, "T001", "Bob", "ada", minutes_later(62))
        change_status_with_event(tickets, events, "T001", "in_progress", "bob", minutes_later(63))
        change_status_with_event(tickets, events, "T001", "resolved", "bob", minutes_later(64))
        change_status_with_event(tickets, events, "T001", "open", "ada", minutes_later(100))
        self.assertEqual(escalate_overdue(tickets, events, minutes_later(161), "ada"), (1, 0))


class DuplicateTests(unittest.TestCase):
    def test_messy_title_matches_and_is_held_back(self):
        tickets, events = [], []
        new_ticket(tickets, events, title=" Wi-Fi   Down ")
        self.assertEqual(find_duplicates(tickets, "network", "wi-fi down"), ["T001"])
        self.assertIsNone(new_ticket(tickets, events, title="wi-fi down"))
        self.assertEqual((len(tickets), len(events)), (1, 1))      # nothing was created

    def test_confirming_creates_the_second_ticket(self):
        tickets, events = [], []
        new_ticket(tickets, events, title=" Wi-Fi   Down ")
        second = new_ticket(tickets, events, title="wi-fi down", allow_duplicate=True)
        self.assertEqual(second["id"], "T002")
        self.assertEqual(len(events), 2)

    def test_resolved_or_other_category_is_not_a_duplicate(self):
        tickets, events = [], []
        new_ticket(tickets, events)
        self.assertEqual(find_duplicates(tickets, "Hardware", "Wi-Fi down"), [])
        tickets[0]["status"] = "resolved"
        self.assertEqual(find_duplicates(tickets, "Network", "Wi-Fi down"), [])


if __name__ == "__main__":
    unittest.main()
