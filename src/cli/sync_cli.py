#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path to import from src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.sync.fetch import fetch_goodreads_rss
from src.sync.parse import parse_xml, sort_books
from src.sync.render import generate_markdown, cleanup_files
from src.data.storage import save_reading_log

def main():
    load_dotenv()
    api_key = os.getenv('GOODREADS_API_KEY')
    user_id = os.getenv('GOODREADS_USER_ID')
    
    if not api_key or not user_id:
        print("❌ Error: GOODREADS_API_KEY and GOODREADS_USER_ID must be set")
        sys.exit(1)
    
    input_file = "raw_books.xml"
    output_file = "reading_log.md"
    
    if fetch_goodreads_rss(user_id, api_key, input_file):
        print("🔍 Reading XML data...")
        books = parse_xml(input_file)
        print(f"📚 Found {len(books)} books.")
        
        print("🔄 Sorting and generating Markdown...")
        books = sort_books(books)
        markdown_content = generate_markdown(books)
        
        print(f"💾 Writing to {output_file}...")
        save_reading_log(markdown_content, output_file)
        
        cleanup_files(input_file)
        print(f"✅ Synchronization complete!")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
