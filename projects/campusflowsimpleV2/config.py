"""Shared constants for CampusFlow."""

DATA_FILE = "tickets.json"

CATEGORIES = ["Network", "Hardware", "Software", "Other"]
URGENCIES = ["low", "medium", "high"]
PRIORITIES = ["critical", "high", "medium", "low"]   # queue order
STATUSES = ["open", "in_progress", "resolved"]
FIELDS = ["id", "title", "category", "urgency", "affected_users",
          "priority", "status", "assigned_to"]

# Allowed workflow moves: current status -> the one status it may move to.
NEXT_STATUS = {"open": "in_progress", "in_progress": "resolved", "resolved": "open"}

# ---------- CampusFlow Pro additions ----------
SCHEMA_VERSION = 2

# Minutes allowed before a ticket is due, by priority.
SLA_MINUTES = {"critical": 60, "high": 240, "medium": 1440, "low": 2880}

# Folder where Knowledge Lab results are saved.
LAB_FOLDER = "lab_sessions"
