from src.bot.middleware.formatters import format_progress_for_telegram

def test_format_progress_empty():
    """Test formatting when progress is empty."""
    assert "Ingen bok" in format_progress_for_telegram("")

def test_format_progress_content():
    """Test formatting with actual content."""
    content = "# Current\n- Book A"
    formatted = format_progress_for_telegram(content)
    assert "<b>Current</b>" in formatted
    assert "• Book A" in formatted

def test_format_progress_bar():
    """Test the visual progress bar logic."""
    # Use 'framsteg' as expected by the Swedish-localized formatter
    content = "Framsteg: 45%"
    formatted = format_progress_for_telegram(content)
    # The formatter now uses a 20-character wide bar (Story 8)
    # 45% of 20 = 9 blocks
    expected_bar = "█" * 9 + "░" * 11
    assert f"<code>[{expected_bar}] 45%</code>" in formatted

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
    assert "Senaste 1 böckerna" in formatted
