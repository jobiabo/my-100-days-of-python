import json
import os
import tempfile
import unittest
from datetime import datetime, timezone

from actions import create_with_event
from storage import load_data, save_data

START = datetime(2026, 10, 14, 10, 0, tzinfo=timezone.utc)


class DataFileTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.folder.name, "tickets.json")

    def tearDown(self):
        self.folder.cleanup()

    def test_save_and_load_keeps_tickets_and_events(self):
        tickets, events = [], []
        create_with_event(tickets, events, "Printer", "Hardware", "low", 1, "ada", now=START)
        save_data(tickets, events, self.path)
        loaded_tickets, loaded_events = load_data(self.path)
        self.assertEqual(loaded_tickets, tickets)
        self.assertEqual(loaded_events, events)

    def test_new_ticket_id_continues_after_reload(self):
        tickets, events = [], []
        create_with_event(tickets, events, "One", "Other", "low", 1, "ada", now=START)
        save_data(tickets, events, self.path)
        tickets, events = load_data(self.path)
        second = create_with_event(tickets, events, "Two", "Other", "low", 1, "ada", now=START)
        self.assertEqual(second["id"], "T002")
        self.assertEqual(events[-1]["event_id"], "E002")

    def test_corrupt_file_is_rejected_and_not_overwritten(self):
        with open(self.path, "w") as f:
            f.write("{this is not json")
        with self.assertRaises(ValueError):
            load_data(self.path)
        with open(self.path) as f:
            self.assertEqual(f.read(), "{this is not json")

    def test_event_pointing_to_missing_ticket_is_rejected(self):
        tickets, events = [], []
        create_with_event(tickets, events, "Printer", "Hardware", "low", 1, "ada", now=START)
        save_data(tickets, events, self.path)
        with open(self.path) as f:
            data = json.load(f)
        data["events"][0]["ticket_id"] = "T999"
        with open(self.path, "w") as f:
            json.dump(data, f)
        with self.assertRaises(ValueError):
            load_data(self.path)

    def test_old_list_format_is_rejected(self):
        with open(self.path, "w") as f:
            json.dump([], f)
        with self.assertRaises(ValueError):
            load_data(self.path)

    def test_bad_data_is_never_saved(self):
        with self.assertRaises(ValueError):
            save_data([{"id": "T001"}], [], self.path)
        self.assertFalse(os.path.exists(self.path))


if __name__ == "__main__":
    unittest.main()
