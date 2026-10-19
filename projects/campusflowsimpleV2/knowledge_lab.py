"""Engineering Knowledge Lab: 10 questions, auto-scored, with explanations.
This file never reads or changes ticket data."""

import json
import os

from config import LAB_FOLDER
from sla import now_utc

LETTERS = ["A", "B", "C", "D"]
PEOPLE = ["A", "B"]
MUST_EXPLAIN = ["Q1", "Q5", "Q10"]      # explanations required here, optional elsewhere
MIN_LENGTH = 10                          # shortest allowed explanation

QUESTIONS = [
    {"id": "Q1", "topic": "SLA boundaries", "answer": "B",
     "text": "A critical ticket is created at 10:00 UTC. At 11:00 UTC, is it overdue?",
     "options": ["Yes", "No, only strictly after 11:00", "Only if assigned", "Only if reopened"],
     "ask": "Explain the difference between 'due' and 'overdue'.",
     "why": "Due at 11:00 is the deadline. Overdue means strictly later than the deadline."},
    {"id": "Q2", "topic": "Priority rules", "answer": "B",
     "text": "urgency=low and affected_users=10. What priority?",
     "options": ["Critical", "High", "Medium", "Low"],
     "ask": "Explain which rule applies first.",
     "why": "Critical needs high urgency AND 10+ users. 'High urgency OR 10+ users' matches next: high."},
    {"id": "Q3", "topic": "Rejected actions", "answer": "C",
     "text": "An unassigned open ticket moves directly to in_progress. What should happen?",
     "options": ["Transition succeeds", "Status changes but history stays",
                 "Reject without changing ticket or events", "Delete the ticket"],
     "ask": "Explain the invariant.",
     "why": "A rejected action must leave the ticket and the events unchanged."},
    {"id": "Q4", "topic": "SLA cycles and reopening", "answer": "B",
     "text": "A resolved high-priority ticket is reopened. Which SLA behavior is correct?",
     "options": ["Keep old due_at always", "Start a fresh SLA cycle while preserving created_at",
                 "Reset created_at to today's date", "Delete previous events"],
     "ask": "Explain why.",
     "why": "Reopening starts a new cycle (new due_at). created_at and old events stay."},
    {"id": "Q5", "topic": "Escalation happens once", "answer": "C",
     "text": "An overdue ticket is checked three times within one SLA cycle. How many new ESCALATE events?",
     "options": ["Three", "Two", "One", "Zero"],
     "ask": "Explain idempotency.",
     "why": "Repeating the check must not repeat the result: one escalation per cycle."},
    {"id": "Q6", "topic": "Safe JSON loading", "answer": "D",
     "text": "The saved file has invalid JSON. What is the safest action?",
     "options": ["Replace data with empty list", "Use eval()",
                 "Ignore and keep running with partial data",
                 "Reject load and preserve existing valid state"],
     "ask": "Explain your choice.",
     "why": "Check the file first and only replace your data if it is good. Never use eval()."},
    {"id": "Q7", "topic": "Code review", "answer": "B",
     "text": "A PR changes SLA calculations but adds no boundary tests. What should a reviewer do?",
     "options": ["Approve because it runs locally", "Request focused tests and explanation",
                 "Merge and test next week", "Ask AI to approve automatically"],
     "ask": "Explain your reasoning.",
     "why": "Boundary bugs hide at exact limits. A reviewer asks for proof."},
    {"id": "Q8", "topic": "Checking AI advice", "answer": "C",
     "text": "An assistant says 'use eval() to parse stored JSON'. What should you do?",
     "options": ["Copy it", "Disable tests", "Reject and use JSON parsing with validation",
                 "Share the whole file publicly"],
     "ask": "Explain how you verified.",
     "why": "eval() runs any code in the file. json.load plus checks is safe."},
    {"id": "Q9", "topic": "Duplicate warnings", "answer": "B",
     "text": "Titles ' Wi-Fi   Down ' and 'wi-fi down' share a category, both unresolved. What should the CLI do?",
     "options": ["Silently delete original", "Warn and require confirmation",
                 "Silently block forever", "Ignore normalization"],
     "ask": "Explain the trade-off.",
     "why": "Repeat reports can be real, so warn and let the user decide."},
    {"id": "Q10", "topic": "Audit history", "answer": "D",
     "text": "An invalid return/status operation is rejected. What should happen to event count?",
     "options": ["Increase by one", "Increase twice", "Reset to zero", "Stay unchanged"],
     "ask": "Explain the reason.",
     "why": "Events record changes that really happened. A rejected action changed nothing."},
]


# ---------- Small checking functions (easy to test) ----------

def is_valid_choice(text):
    """Only exactly A, B, C or D is accepted."""
    return text in LETTERS


def explanation_problem(question_id, text):
    """Returns a message if the explanation is not acceptable, otherwise ''."""
    text = " ".join(text.split())
    if text == "" and question_id not in MUST_EXPLAIN:
        return ""                                       # optional: skipping is fine
    if len(text) < MIN_LENGTH:
        return f"Please write at least {MIN_LENGTH} characters."
    return ""


def calculate_score(choices):
    """choices looks like {"Q1": "B", ...}. Returns (score, topics to revise)."""
    score = 0
    revise = []
    for q in QUESTIONS:
        if choices.get(q["id"]) == q["answer"]:
            score += 1
        else:
            revise.append(q["topic"])
    return score, revise


def build_record(person, choices, explanations, when):
    score, revise = calculate_score(choices)
    return {"participant": person, "timestamp": when.isoformat(), "choices": choices,
            "score": score, "revision_topics": revise, "explanations": explanations}


def save_record(record, folder=LAB_FOLDER):
    os.makedirs(folder, exist_ok=True)
    stamp = record["timestamp"][:19].replace(":", "").replace("-", "")
    path = os.path.join(folder, f"session_{record['participant']}_{stamp}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2)
    return path


# ---------- The interactive part ----------

def run_quiz(folder=LAB_FOLDER):
    print("\n===== Engineering Knowledge Lab =====")
    person = ""
    while person not in PEOPLE:
        person = input("Participant [A/B]: ")
    choices = {}
    explanations = {}

    for number, q in enumerate(QUESTIONS, start=1):
        print(f"\n{q['id']} ({number}/10) {q['text']}")
        for letter, option in zip(LETTERS, q["options"]):
            print(f"  {letter}) {option}")

        answer = input("Your answer [A/B/C/D]: ")
        while not is_valid_choice(answer):
            print("  Enter exactly A, B, C or D (capital letter).")
            answer = input("Your answer [A/B/C/D]: ")
        choices[q["id"]] = answer

        note = "required" if q["id"] in MUST_EXPLAIN else "optional, Enter to skip"
        text = input(f"{q['ask']} ({note}): ")
        problem = explanation_problem(q["id"], text)
        while problem != "":
            print("  " + problem)
            text = input(f"{q['ask']} ({note}): ")
            problem = explanation_problem(q["id"], text)
        if text.strip() != "":
            explanations[q["id"]] = " ".join(text.split())

    record = build_record(person, choices, explanations, now_utc())
    print(f"\nScore: {record['score']}/10")
    topics = ", ".join(record["revision_topics"]) or "none"
    print("Topics to revise:", topics)
    for q in QUESTIONS:
        given = choices[q["id"]]
        if given == q["answer"]:
            print(f"{q['id']}: you chose {given} - correct")
        else:
            print(f"{q['id']}: you chose {given} - wrong (correct is {q['answer']}). {q['why']}")
        if q["id"] in explanations:
            print("    Your explanation:", explanations[q["id"]])
    print("\nSaved to", save_record(record, folder))
