#!/usr/bin/env python3
"""
Läser Goodreads RSS-data (raw_books.xml) och genererar en Markdown-logg.
Scriptet är deterministiskt och robust, designat för att köras på Raspberry Pi.
"""

import xml.etree.ElementTree as ET
from datetime import datetime
import os
import sys

# Konstanter
INPUT_FILE = "raw_books.xml"
OUTPUT_FILE = "reading_log.md"

# Goodreads RSS may send various date formats. We try these in order.
DATE_FORMATS = [
    "%a, %d %b %Y %H:%M:%S %z",         # RFC 822 / RSS pubDate (t.ex. Mon, 9 Feb 2026 00:00:00 +0000)
    "%Y-%m-%d",                         # Enkelt format (YYYY-MM-DD)
    "%a %b %d %H:%M:%S %Y %z",          # Goodreads standard (t.ex. Mon Feb 10 00:00:00 2026 +0000)
    "%a %b %d %H:%M:%S %Y",             # Utan tidszon
    "%Y-%m-%dT%H:%M:%S%z",              # ISO 8601 med tidszon
    "%Y-%m-%d %H:%M:%S"                 # Lokalt format
]

def parse_xml(file_path):
    """
    Parsar Goodreads XML-filen och extraherar bokdata.
    Hanterar saknade fält och datumfel graciöst.
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

        books.append({
            'title': title,
            'author': author,
            'rating': rating,
            'date_display': display_date,
            'date_obj': date_obj,
            'link': link
        })

    return books

def sort_books(books):
    """
    Sorts books based on read date (newest first).
    Books without date are placed last.
    """
    # Sort key: (Has date, Date object) -> reverse=True puts True (has date) first
    return sorted(books, key=lambda x: (x['date_obj'] is None, x['date_obj']), reverse=True)

def generate_markdown(books):
    """
    Genererar Markdown-innehållet baserat på den sorterade boklistan.
    """
    lines = [
        "# Lästa Böcker",
        "",
        "Denna fil innehåller en lista över böcker jag har läst, hämtad från Goodreads RSS-feed.",
        "",
        "| Titel | Författare | Betyg | Datum läst | Länk |",
        "|-------|------------|-------|------------|------|"
    ]

    # Lägg till rader
    for book in books:
        # Replace | with HTML entity to avoid breaking the table
        title = book['title'].replace('|', '&#124;')
        author = book['author'].replace('|', '&#124;')
        lines.append(f"| {title} | {author} | {book['rating']} | {book['date_display']} | [Link]({book['link']}) |")

    # Sammanfattning
    total_books = len(books)
    top_rated_books = [b['title'] for b in books if b['rating'] == '5']
    
    latest_book = books[0] if books else None
    oldest_book = None

    # Hitta äldsta boken med ett giltigt datum
    for book in reversed(books):
        if book['date_obj']:
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
        lines.append(f"- **Senaste bok:** {latest_book['title']} (läst {latest_book['date_display']})")
    
    if oldest_book:
        lines.append(f"- **Äldsta bok:** {oldest_book['title']} (läst {oldest_book['date_display']})")

    # Noteringar
    lines.extend([
        "",
        "## Noteringar",
        "- Denna fil är automatiskt genererad av sync_books.py."
    ])

    return "\n".join(lines)

def cleanup_files():
    """
    Deletes the raw data file after processing.
    """
    print("🧹 Cleaning up temporary files...")
    
    # Delete raw_books.xml
    if os.path.exists(INPUT_FILE):
        os.remove(INPUT_FILE)
        print(f"   Deleted {INPUT_FILE}")

def main():
    """Main function to run synchronization."""
    print("🔍 Reading XML data...")
    books = parse_xml(INPUT_FILE)
    
    print(f"📚 Found {len(books)} books.")
    
    print("🔄 Sorting and generating Markdown...")
    books = sort_books(books)
    markdown_content = generate_markdown(books)
    
    print(f"💾 Writing to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    # Cleanup
    cleanup_files()
    
    print(f"✅ Done! Log updated.")

    # Import from the refactored script
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    from scripts.sync_books_refactored import main

if __name__ == "__main__":
    main()
