import unittest
from datetime import datetime, timedelta, timezone

from actions import escalate_overdue
from sla import is_overdue, make_due_at, to_time
from ticket_service import create_ticket

START = datetime(2026, 10, 14, 10, 0, tzinfo=timezone.utc)   # a fixed clock


def minutes_later(n):
    return START + timedelta(minutes=n)


def critical_ticket():
    tickets = []
    create_ticket(tickets, "Server down", "Network", "high", 20, START)
    return tickets


class SlaTests(unittest.TestCase):
    def test_due_time_for_each_priority(self):
        expected = {"critical": 60, "high": 240, "medium": 1440, "low": 2880}
        for priority, minutes in expected.items():
            self.assertEqual(to_time(make_due_at(priority, START)),
                             START + timedelta(minutes=minutes))

    def test_critical_at_exactly_60_minutes_is_not_overdue(self):
        ticket = critical_ticket()[0]
        self.assertFalse(is_overdue(ticket, minutes_later(60)))

    def test_critical_at_61_minutes_is_overdue(self):
        ticket = critical_ticket()[0]
        self.assertTrue(is_overdue(ticket, minutes_later(61)))

    def test_resolved_ticket_is_never_overdue(self):
        ticket = critical_ticket()[0]
        ticket["status"] = "resolved"
        self.assertFalse(is_overdue(ticket, minutes_later(500)))

    def test_escalation_only_once_per_cycle(self):
        tickets, events = critical_ticket(), []
        self.assertEqual(escalate_overdue(tickets, events, minutes_later(61), "ada"), (1, 0))
        self.assertEqual(escalate_overdue(tickets, events, minutes_later(61), "ada"), (0, 1))
        self.assertEqual(escalate_overdue(tickets, events, minutes_later(90), "ada"), (0, 1))
        self.assertEqual(len(events), 1)

    def test_escalation_does_not_change_the_ticket(self):
        tickets, events = critical_ticket(), []
        before = dict(tickets[0])
        escalate_overdue(tickets, events, minutes_later(61), "ada")
        self.assertEqual(tickets[0], before)

    def test_ticket_not_yet_overdue_is_not_escalated(self):
        tickets, events = critical_ticket(), []
        self.assertEqual(escalate_overdue(tickets, events, minutes_later(60), "ada"), (0, 0))
        self.assertEqual(events, [])


if __name__ == "__main__":
    unittest.main()
