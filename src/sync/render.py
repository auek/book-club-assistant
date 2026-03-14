#!/usr/bin/env python3
"""
Render module for generating Markdown output.
Handles Markdown generation and file cleanup.
"""

from typing import List
import os
from src.data.models import Book
from src.utils.config import BASE_DIR


def generate_markdown(books: List[Book]) -> str:
    """
    Generate Markdown content based on the sorted book list.
    
    Args:
        books: List of book dictionaries
        
    Returns:
        Markdown formatted string
    """
    lines = [
        "# Lästa Böcker",
        "",
        "Denna fil innehåller en lista över böcker jag har läst, hämtad från Goodreads RSS-feed.",
        "",
        "| Titel | Författare | Betyg | Datum läst | Länk |",
        "|-------|------------|-------|------------|------|"
    ]

    # Add rows
    for book in books:
        # Replace | with HTML entity to avoid breaking the table
        title = book.title.replace('|', '&#124;')
        author = book.author.replace('|', '&#124;')
        lines.append(f"| {title} | {author} | {book.rating} | {book.date_display} | [Link]({book.link}) |")

    # Summary
    total_books = len(books)
    top_rated_books = [b.title for b in books if b.rating == '5']
    
    latest_book = books[0] if books else None
    oldest_book = None

    # Find oldest book with a valid date
    for book in reversed(books):
        if book.date_obj:
            oldest_book = book
            break

    lines.extend([
        "",
        "## Sammanfattning",
        f"- **Totalt antal böcker:** {total_books}",
    ])

    if top_rated_books:
        lines.append(f"- **Högsta betyg:** 5 ({', '.join(top_rated_books)})")
    else:
        lines.append("- **Högsta betyg:** Saknas")

    if latest_book:
        lines.append(f"- **Senaste bok:** {latest_book.title} (läst {latest_book.date_display})")
    
    if oldest_book:
        lines.append(f"- **Äldsta bok:** {oldest_book.title} (läst {oldest_book.date_display})")

    # Notes
    lines.extend([
        "",
        "## Noteringar",
        "- Denna fil är automatiskt genererad av sync_books.py."
    ])

    return "\n".join(lines)


def cleanup_files(input_file: str = str(BASE_DIR / "raw_books.xml")) -> None:
    """
    Delete the raw data file after processing.
    
    Args:
        input_file: Path to the raw XML file to delete
    """
    print("🧹 Cleaning up temporary files...")
    
    # Delete raw_books.xml
    if os.path.exists(input_file):
        os.remove(input_file)
        print(f"   Deleted {input_file}")
