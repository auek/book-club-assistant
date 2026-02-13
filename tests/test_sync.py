import pytest
from src.sync.parse import sort_books
from src.data.models import Book
from datetime import datetime

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
