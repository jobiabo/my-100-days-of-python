import json
import os
import tempfile
import unittest
from datetime import datetime, timezone

from actions import create_with_event
from knowledge_lab import (QUESTIONS, build_record, calculate_score,
                           explanation_problem, is_valid_choice, save_record)

NOW = datetime(2026, 10, 14, 10, 0, tzinfo=timezone.utc)
ALL_CORRECT = {q["id"]: q["answer"] for q in QUESTIONS}


class QuizTests(unittest.TestCase):
    def test_there_are_ten_questions(self):
        self.assertEqual(len(QUESTIONS), 10)

    def test_only_exact_a_b_c_d_is_valid(self):
        for good in ["A", "B", "C", "D"]:
            self.assertTrue(is_valid_choice(good))
        for bad in ["E", "", " ", "a", "AB", "1"]:
            self.assertFalse(is_valid_choice(bad), repr(bad))

    def test_scoring_and_revision_topics(self):
        self.assertEqual(calculate_score(ALL_CORRECT), (10, []))
        choices = dict(ALL_CORRECT, Q5="A", Q10="A")
        score, topics = calculate_score(choices)
        self.assertEqual(score, 8)
        self.assertEqual(topics, ["Escalation happens once", "Audit history"])
        self.assertEqual(calculate_score({})[0], 0)

    def test_required_explanations(self):
        self.assertNotEqual(explanation_problem("Q1", ""), "")        # required
        self.assertNotEqual(explanation_problem("Q1", "too short"), "")
        self.assertEqual(explanation_problem("Q2", ""), "")           # optional
        self.assertEqual(explanation_problem("Q1", "Overdue means strictly later."), "")

    def test_session_file_has_everything_mentors_need(self):
        explanations = {"Q1": "Due is the deadline.", "Q5": "Once per cycle.", "Q10": "Nothing changed."}
        record = build_record("B", ALL_CORRECT, explanations, NOW)
        with tempfile.TemporaryDirectory() as folder:
            path = save_record(record, folder)
            with open(path) as f:
                saved = json.load(f)
        self.assertEqual(saved["participant"], "B")
        self.assertEqual(saved["timestamp"], NOW.isoformat())
        self.assertEqual(saved["score"], 10)
        self.assertEqual(saved["choices"], ALL_CORRECT)
        self.assertEqual(saved["explanations"], explanations)

    def test_quiz_does_not_touch_tickets(self):
        tickets, events = [], []
        create_with_event(tickets, events, "Printer", "Hardware", "low", 1, "ada", now=NOW)
        before = json.dumps([tickets, events])
        record = build_record("A", ALL_CORRECT, {}, NOW)
        with tempfile.TemporaryDirectory() as folder:
            save_record(record, folder)
        self.assertEqual(json.dumps([tickets, events]), before)


if __name__ == "__main__":
    unittest.main()
