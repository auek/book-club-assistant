#!/usr/bin/env python3
"""
Get your Telegram user chat ID.
Before running, make sure you have sent at least one message to your bot.
"""
from dotenv import load_dotenv
import os
import requests

def get_chat_id():
    # Load environment variables
    load_dotenv()
    api_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not api_token:
        print("❌ Error: TELEGRAM_BOT_TOKEN not found in .env file")
        print("   Add TELEGRAM_BOT_TOKEN='your_bot_token' to your .env file")
        return None
    
    try:
        # Get updates to see recent messages sent to the bot
        response = requests.get(f"https://api.telegram.org/bot{api_token}/getUpdates")
        if response.status_code != 200:
            print(f"❌ HTTP error: {response.status_code}")
            return None
        
        result = response.json()
        if not result.get('ok'):
            print(f"❌ API error: {result.get('description', 'Unknown error')}")
            return None
        
        updates = result.get('result', [])
        if not updates:
            print("⚠️  No updates found. Please send a message to your bot first.")
            return None
        
        # Extract the chat ID from the first update
        chat = updates[0].get('message', {}).get('chat', {})
        chat_id = chat.get('id')
        if not chat_id:
            print("❌ Could not extract chat ID from update.")
            return None
        
        print(f"✅ Your Telegram chat ID: {chat_id}")
        print("   Add this to your .env file as TELEGRAM_CHAT_ID")
        return chat_id
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return None

if __name__ == "__main__":
    print("This script helps you get your Telegram user chat ID.")
    print("1. First, send a message to your bot in Telegram.")
    print("2. Then run this script to get your chat ID.")
    get_chat_id()
