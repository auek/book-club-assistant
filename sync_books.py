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

# Goodreads RSS kan skicka olika datumformat. Vi prover dessa i ordning.
DATE_FORMATS = [
    "%Y-%m-%d",                 # Enkelt format (YYYY-MM-DD)
    "%a %b %d %H:%M:%S %Y %z",  # Goodreads standard (t.ex. Mon Feb 10 00:00:00 2026 +0000)
    "%a %b %d %H:%M:%S %Y"      # Utan tidszon
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
    
    # Goodreads RSS items ligger vanligtvis under //item
    for item in root.findall('.//item'):
        # Extrahera data med fallback för saknade taggar
        title_node = item.find('title')
        title = title_node.text if title_node is not None else "Okänd titel"

        author_node = item.find('author_name')
        author = author_node.text if author_node is not None else "Okänd författare"

        rating_node = item.find('user_rating')
        rating = rating_node.text if rating_node is not None else "0"

        link_node = item.find('link')
        link = link_node.text if link_node is not None else "#"

        # Hantera datum
        date_read_node = item.find('user_read_at')
        date_str = date_read_node.text if date_read_node is not None and date_read_node.text else None
        
        date_obj = None
        display_date = "Saknas"

        if date_str:
            # Försök parsa datumet med de definierade formaten
            for fmt in DATE_FORMATS:
                try:
                    date_obj = datetime.strptime(date_str, fmt)
                    # Normalisera visning till YYYY-MM-DD
                    display_date = date_obj.strftime("%Y-%m-%d")
                    break
                except ValueError:
                    continue

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
    Sorterar böcker baserat på läst datum (nyast först).
    Böcker utan datum placeras sist.
    """
    # Sortera nyckel: (Har datum, Datumobjekt) -> reverse=True sätter True (har datum) först
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
        lines.append(f"| {book['title']} | {book['author']} | {book['rating']} | {book['date_display']} | [Länk]({book['link']}) |")

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
    Raderar rådatafilen efter bearbetning.
    """
    print("🧹 Städar upp temporära filer...")
    
    # Radera raw_books.xml
    if os.path.exists(INPUT_FILE):
        os.remove(INPUT_FILE)
        print(f"   Raderade {INPUT_FILE}")

def main():
    """Huvudfunktion för att köra synkroniseringen."""
    print("🔍 Läser XML-data...")
    books = parse_xml(INPUT_FILE)
    
    print(f"📚 Hittade {len(books)} böcker.")
    
    print("🔄 Sorterar och genererar Markdown...")
    books = sort_books(books)
    markdown_content = generate_markdown(books)
    
    print(f"💾 Skriver till {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    # Städning
    cleanup_files()
    
    print(f"✅ Klart! Logg uppdaterad.")

if __name__ == "__main__":
    main()
