import os
from typing import List
from src.data.models import Book

def save_reading_log(markdown_content: str, output_file: str = "reading_log.md") -> None:
    """Writes the generated markdown to the reading log file."""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_content)

def read_file_content(file_path: str) -> str:
    """Reads content from a file, returns empty string if not found."""
    if not os.path.exists(file_path):
        return ""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
