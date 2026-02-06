import os
import json

def read_log_file(filepath):
    """Reads the raw log file."""
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Error: Log file not found."

def read_ticket_data(filepath):
    """Reads the JSON incident ticket."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": "Ticket file not found."}

def read_runbook(filepath):
    """Reads the markdown runbook."""
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Error: Runbook not found."