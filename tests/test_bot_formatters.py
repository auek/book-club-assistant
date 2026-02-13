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
