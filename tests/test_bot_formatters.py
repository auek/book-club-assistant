import pytest
from src.bot.middleware.formatters import format_progress_for_telegram

def test_format_progress_empty():
    """Test formatting when progress is empty."""
    assert "Inga böcker" in format_progress_for_telegram("")

def test_format_progress_content():
    """Test formatting with actual content."""
    content = "# Current\n- Book A"
    formatted = format_progress_for_telegram(content)
    assert "<b>Current</b>" in formatted
    assert "• Book A" in formatted

def test_format_progress_bar():
    """Test the visual progress bar logic."""
    content = "Progress: 45%"
    formatted = format_progress_for_telegram(content)
    assert "<code>[████░░░░░░] 45%</code>" in formatted

def test_format_books_limit():
    """Test that book formatting respects the limit and handles tables."""
    from src.bot.middleware.formatters import format_books_for_telegram
    markdown = """
| Titel | Författare | Betyg | Datum | Länk |
|-------|------------|-------|-------|------|
| Book 1 | Author 1 | 5 | 2024-01-01 | url |
| Book 2 | Author 2 | 3 | 2024-01-02 | url |
"""
    formatted = format_books_for_telegram(markdown, limit=1)
    assert "1. Book 1" in formatted
    assert "Author 1" in formatted
    assert "⭐⭐⭐⭐⭐" in formatted
    assert "2. Book 2" not in formatted
