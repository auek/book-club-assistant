#!/usr/bin/env python3
import os
import sys
import requests
from src.utils.config import validate_config

def check_connectivity():
    """Checks if external APIs are reachable."""
    try:
        requests.get("https://www.goodreads.com", timeout=5)
        print("✅ Goodreads API is reachable.")
        return True
    except Exception as e:
        print(f"❌ Goodreads API is unreachable: {e}")
        return False

def check_permissions():
    """Checks if the application has necessary file permissions."""
    paths = ['.', 'src']
    all_ok = True
    for path in paths:
        if os.access(path, os.W_OK):
            print(f"✅ Write permission OK for: {path}")
        else:
            print(f"❌ No write permission for: {path}")
            all_ok = False
    return all_ok

def main():
    print("🔍 Running System Health Check...")
    
    valid, msg = validate_config()
    print(msg)
    
    conn_ok = check_connectivity()
    perm_ok = check_permissions()
    
    if valid and conn_ok and perm_ok:
        print("\n🚀 System is healthy and ready!")
    else:
        print("\n⚠️ System has health issues. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
