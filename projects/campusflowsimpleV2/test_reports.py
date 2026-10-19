import unittest
from datetime import datetime, timedelta, timezone

from actions import create_with_event, escalate_overdue
from reports import sla_metrics, sla_queue

START = datetime(2026, 10, 14, 10, 0, tzinfo=timezone.utc)


def minutes_later(n):
    return START + timedelta(minutes=n)


def add(tickets, events, title, urgency, users, created=START):
    create_with_event(tickets, events, title, "Network", urgency, users, "ada", now=created)


def ids(tickets):
    return [t["id"] for t in tickets]


class QueueTests(unittest.TestCase):
    def setUp(self):
        self.tickets, self.events = [], []
        add(self.tickets, self.events, "a", "low", 1)                 # T001 due +2880
        add(self.tickets, self.events, "b", "high", 10)               # T002 due +60
        add(self.tickets, self.events, "c", "medium", 1)              # T003 due +1440
        add(self.tickets, self.events, "d", "low", 1, START - timedelta(minutes=2000))  # T004 due +880
        add(self.tickets, self.events, "e", "high", 10)               # T005 due +60

    def test_overdue_first_then_due_time_then_id(self):
        # At +61 minutes T002 and T005 are overdue (tie -> lower ID first).
        self.assertEqual(ids(sla_queue(self.tickets, minutes_later(61))),
                         ["T002", "T005", "T004", "T003", "T001"])

    def test_when_nothing_is_overdue_sort_by_due_time(self):
        self.assertEqual(ids(sla_queue(self.tickets, minutes_later(30))),
                         ["T002", "T005", "T004", "T003", "T001"])

    def test_overdue_comes_before_an_earlier_due_ticket(self):
        tickets, events = [], []
        add(tickets, events, "x", "low", 1, START - timedelta(minutes=2900))   # overdue
        add(tickets, events, "y", "high", 10)                                   # not overdue
        self.assertEqual(ids(sla_queue(tickets, minutes_later(10))), ["T001", "T002"])

    def test_resolved_tickets_are_left_out(self):
        self.tickets[1]["status"] = "resolved"
        self.assertNotIn("T002", ids(sla_queue(self.tickets, minutes_later(61))))


class MetricsTests(unittest.TestCase):
    def test_numbers_and_no_double_counting(self):
        tickets, events = [], []
        add(tickets, events, "a", "high", 10)        # T001 critical, will be overdue
        add(tickets, events, "b", "low", 1)          # T002 low, on time
        add(tickets, events, "c", "high", 10)        # T003 critical, resolved
        tickets[2]["status"] = "resolved"
        escalate_overdue(tickets, events, minutes_later(61), "ada")
        escalate_overdue(tickets, events, minutes_later(62), "ada")   # again: still 1
        m = sla_metrics(tickets, events, minutes_later(62))
        self.assertEqual((m["open"], m["in_progress"], m["resolved"]), (2, 0, 1))
        self.assertEqual((m["overdue"], m["escalated"]), (1, 1))
        self.assertEqual(m["by_priority"], {"critical": 2, "high": 0, "medium": 0, "low": 1})

    def test_reports_do_not_change_data(self):
        tickets, events = [], []
        add(tickets, events, "a", "high", 10)
        before = ([dict(t) for t in tickets], [dict(e) for e in events])
        sla_queue(tickets, minutes_later(99))
        sla_metrics(tickets, events, minutes_later(99))
        self.assertEqual((tickets, events), before)


if __name__ == "__main__":
    unittest.main()
