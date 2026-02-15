from unittest.mock import AsyncMock, patch, MagicMock
import pytest
from src.sync.parse import sort_books
from src.data.models import Book
from datetime import datetime
from src.bot.commands.sync import sync_books

@pytest.mark.asyncio
async def test_sync_books_command_flow():
    """Test that /sync command correctly orchestrates the sync workflow."""
    # Mock Telegram Update and Context
    update = AsyncMock()
    update.message.reply_text = AsyncMock(return_value=AsyncMock())
    context = MagicMock()

    # Mock dependencies to isolate the command logic
    with patch("src.bot.commands.sync.get_config", return_value="mock_val"), \
         patch("src.bot.commands.sync.fetch_goodreads_rss", return_value=True) as mock_fetch, \
         patch("src.bot.commands.sync.parse_xml", return_value=[]) as mock_parse, \
         patch("src.bot.commands.sync.sort_books", return_value=[]) as mock_sort, \
         patch("src.bot.commands.sync.generate_markdown", return_value="# Log") as mock_render, \
         patch("src.bot.commands.sync.save_reading_log") as mock_save, \
         patch("src.bot.commands.sync.cleanup_files") as mock_cleanup:
        
        # Bypass @auth_only decorator for unit test
        await sync_books.__wrapped__(update, context)

        # Verify orchestration
        mock_fetch.assert_called_once()
        mock_parse.assert_called_once_with("raw_books.xml")
        mock_save.assert_called_once_with("# Log")
        mock_cleanup.assert_called_once()
        
        # Verify response
        final_text = update.message.reply_text.return_value.edit_text.call_args[0][0]
        assert "Sync complete" in final_text

def test_sort_books():
    """Test that books are sorted by date, newest first, with missing dates last."""
    b1 = Book("New", "A", "5", "2024-01-01", datetime(2024, 1, 1), "link")
    b2 = Book("Old", "B", "4", "2023-01-01", datetime(2023, 1, 1), "link")
    b3 = Book("No Date", "C", "3", "Missing", None, "link")
    
    sorted_books = sort_books([b2, b3, b1])
    assert sorted_books == [b1, b2, b3]

def test_book_to_dict():
    """Test the Book dataclass to_dict method."""
    date_obj = datetime(2024, 1, 1)
    book = Book("Title", "Author", "5", "2024-01-01", date_obj, "link")
    d = book.to_dict()
    assert d['title'] == "Title"
    assert d['date_obj'] == date_obj
