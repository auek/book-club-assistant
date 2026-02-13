#!/usr/bin/env python3
"""
Refactored sync script using modular structure.
This script imports from src.sync modules.
"""

import sys
import os

# Add parent directory to path to import from src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.sync.fetch import fetch_goodreads_rss
from src.sync.parse import parse_xml, sort_books
from src.sync.render import generate_markdown, cleanup_files


# Constants
INPUT_FILE = "raw_books.xml"
OUTPUT_FILE = "reading_log.md"


def main():
    """Main function to run synchronization using modular structure."""
    # Get credentials from environment
    api_key = os.getenv('GOODREADS_API_KEY')
    user_id = os.getenv('GOODREADS_USER_ID')
    
    if not api_key or not user_id:
        print("❌ Error: GOODREADS_API_KEY and GOODREADS_USER_ID must be set")
        sys.exit(1)
    
    # Fetch data
    if not fetch_goodreads_rss(user_id, api_key, INPUT_FILE):
        sys.exit(1)
    
    # Parse XML
    print("🔍 Reading XML data...")
    books = parse_xml(INPUT_FILE)
    print(f"📚 Found {len(books)} books.")
    
    # Sort and generate markdown
    print("🔄 Sorting and generating Markdown...")
    books = sort_books(books)
    markdown_content = generate_markdown(books)
    
    # Write output
    print(f"💾 Writing to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    # Cleanup
    cleanup_files(INPUT_FILE)
    
    print(f"✅ Done! Log updated.")


if __name__ == "__main__":
    main()
