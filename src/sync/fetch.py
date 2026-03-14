#!/usr/bin/env python3
"""
Fetch module for Goodreads RSS data.
Handles API calls and raw data retrieval.
"""

import subprocess
import sys
import os
from src.utils.config import BASE_DIR


def fetch_goodreads_rss(user_id: str, api_key: str, output_file: str = str(BASE_DIR / "raw_books.xml")) -> bool:
    """
    Fetch RSS feed from Goodreads API using curl.
    
    Args:
        user_id: Goodreads user ID
        api_key: Goodreads API key
        output_file: Path to save the XML file
        
    Returns:
        True if successful, False otherwise
    """
    url = f"https://www.goodreads.com/review/list_rss/{user_id}?key={api_key}&shelf=read"
    
    print("📥 Fetching RSS feed...")
    
    try:
        # Use curl to fetch the data
        result = subprocess.run(
            ["curl", "-s", "-f", url],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Write to file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result.stdout)
        
        # Verify file is not empty
        if not os.path.exists(output_file) or os.path.getsize(output_file) == 0:
            print("❌ Received empty XML file", file=sys.stderr)
            print("   Check your Goodreads user ID and API key", file=sys.stderr)
            return False
            
        return True
        
    except subprocess.CalledProcessError as e:
        print("❌ Failed to fetch data from Goodreads", file=sys.stderr)
        print("   Check your internet connection and API credentials", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ Unexpected error during fetch: {e}", file=sys.stderr)
        return False
