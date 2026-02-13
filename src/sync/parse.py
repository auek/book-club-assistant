#!/usr/bin/env python3
"""
Parse module for Goodreads XML data.
Handles XML parsing, data extraction, and sorting.
"""

import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Optional
import os
import sys
from src.data.models import Book


# Goodreads RSS may send various date formats. We try these in order.
DATE_FORMATS = [
    "%a, %d %b %Y %H:%M:%S %z",         # RFC 822 / RSS pubDate
    "%Y-%m-%d",                         # Simple format (YYYY-MM-DD)
    "%a %b %d %H:%M:%S %Y %z",          # Goodreads standard
    "%a %b %d %H:%M:%S %Y",             # Without timezone
    "%Y-%m-%dT%H:%M:%S%z",              # ISO 8601 with timezone
    "%Y-%m-%d %H:%M:%S"                 # Local format
]


def parse_xml(file_path: str) -> List[Book]:
    """
    Parse Goodreads XML file and extract book data.
    Handles missing fields and date errors gracefully.
    
    Args:
        file_path: Path to the XML file
        
    Returns:
        List of Book objects
    """
    if not os.path.exists(file_path):
        print(f"❌ Fel: Filen '{file_path}' saknas.", file=sys.stderr)
        sys.exit(1)

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"❌ Fel vid parsning av XML: {e}", file=sys.stderr)
        sys.exit(1)

    books = []
    
    # Goodreads RSS items are typically under //item
    for item in root.findall('.//item'):
        # Extract data with fallback for missing tags
        title_node = item.find('title')
        title = title_node.text if title_node is not None else "Unknown title"

        author_node = item.find('author_name')
        author = author_node.text if author_node is not None else "Unknown author"

        rating_node = item.find('user_rating')
        rating = rating_node.text if rating_node is not None else "0"

        link_node = item.find('link')
        link = link_node.text if link_node is not None else "#"

        # Handle date: first user_read_at, then pubDate as fallback
        date_read_node = item.find('user_read_at')
        date_str = date_read_node.text if date_read_node is not None and date_read_node.text else None
        
        # Fallback to pubDate if user_read_at is missing
        if not date_str:
            pub_date_node = item.find('pubDate')
            date_str = pub_date_node.text if pub_date_node is not None and pub_date_node.text else None
        
        date_obj = None
        display_date = "Missing"

        if date_str:
            # Try to parse the date with the defined formats
            for fmt in DATE_FORMATS:
                try:
                    date_obj = datetime.strptime(date_str, fmt)
                    # Normalize display to YYYY-MM-DD
                    display_date = date_obj.strftime("%Y-%m-%d")
                    break
                except ValueError:
                    continue
        else:
            # If no date found at all, mark as missing
            display_date = "Missing"

        books.append(Book(
            title=title,
            author=author,
            rating=rating,
            date_display=display_date,
            date_obj=date_obj,
            link=link
        ))

    return books


def sort_books(books: List[Book]) -> List[Book]:
    """
    Sort books based on read date (newest first).
    Books without date are placed last.
    
    Args:
        books: List of Book objects
        
    Returns:
        Sorted list of books
    """
    # Sort key: (Has date, Date object)
    # x.date_obj is not None is True (1) for books with dates, False (0) for missing.
    # reverse=True makes 1 come before 0, and newer dates come before older ones.
    return sorted(books, key=lambda x: (x.date_obj is not None, x.date_obj), reverse=True)
