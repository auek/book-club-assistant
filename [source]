#!/usr/bin/env python3
from dotenv import load_dotenv
import os
import requests

def get_chat_id():
    # Load environment variables
    load_dotenv()
    api_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not api_token:
        print("Error: TELEGRAM_BOT_TOKEN not found in .env file")
        return
    
    try:
        response = requests.get(f"https://api.telegram.org/bot{api_token}/getMe")
        if response.status_code == 200:
            result = response.json()
            if result['ok']:
                chat_id = result['result']['id']  # This is your bot's ID, not your user ID
                print(f"Your Telegram chat ID: {chat_id}")
                return chat_id
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
    
    print("Failed to get chat ID")
    return None

if __name__ == "__main__":
    print("This script helps you get your Telegram chat ID.")
    print("1. First, send a message to your bot in Telegram.")
    print("2. Then run this script to get your chat ID.")
    get_chat_id()
