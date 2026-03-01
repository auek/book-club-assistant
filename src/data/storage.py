import os
import shutil
import json
from datetime import datetime, timedelta
from typing import List, Optional
from src.data.models import Book

def save_reading_log(markdown_content: str, output_file: str = "reading_log.md") -> None:
    """Writes the generated markdown to the reading log file, with a timestamped backup."""
    if os.path.exists(output_file):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{output_file}.{timestamp}.bak"
        shutil.copy2(output_file, backup_file)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_content)

def read_file_content(file_path: str) -> str:
    """Reads content from a file, returns empty string if not found."""
    if not os.path.exists(file_path):
        return ""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

PENDING_CONFIRM_FILE = "pending_confirmations.json"
CONFIRMATION_TIMEOUT_MINUTES = 5

def _load_pending_confirmations() -> dict:
    """Load pending confirmations from file."""
    if not os.path.exists(PENDING_CONFIRM_FILE):
        return {}
    try:
        with open(PENDING_CONFIRM_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def _save_pending_confirmations(data: dict) -> None:
    """Save pending confirmations to file."""
    with open(PENDING_CONFIRM_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def save_pending_confirmation(chat_id: int, data: dict) -> None:
    """Save a pending confirmation for a chat_id."""
    data["timestamp"] = datetime.now().isoformat()
    confirmations = _load_pending_confirmations()
    confirmations[str(chat_id)] = data
    _save_pending_confirmations(confirmations)

def get_pending_confirmation(chat_id: int) -> Optional[dict]:
    """Get pending confirmation if valid (not expired), else None."""
    confirmations = _load_pending_confirmations()
    data = confirmations.get(str(chat_id))
    
    if not data:
        return None
    
    # Check timestamp
    timestamp = datetime.fromisoformat(data["timestamp"])
    if datetime.now() - timestamp > timedelta(minutes=CONFIRMATION_TIMEOUT_MINUTES):
        # Expired - clear it
        clear_pending_confirmation(chat_id)
        return None
    
    return data

def clear_pending_confirmation(chat_id: int) -> None:
    """Remove pending confirmation for a chat_id."""
    confirmations = _load_pending_confirmations()
    confirmations.pop(str(chat_id), None)
    _save_pending_confirmations(confirmations)
