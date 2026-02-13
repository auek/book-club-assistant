#!/usr/bin/env python3
import os
import sys

# Add parent directory to path to import from src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.telegram_bot_refactored import main

if __name__ == "__main__":
    main()
