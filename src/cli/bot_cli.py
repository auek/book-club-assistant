#!/usr/bin/env python3
import os
import sys
import logging

# Add parent directory to path to import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from src.bot.core import error_handler, get_persistence
from src.bot.commands.base import discuss_books

def main():
    load_dotenv()
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("❌ Error: TELEGRAM_BOT_TOKEN not set")
        return

    # Configure logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # Build application with specific defaults to avoid common initialization errors
    persistence = get_persistence()
    application = ApplicationBuilder().token(token).persistence(persistence).build()

    # Use the central registration logic from core.py
    from src.bot.core import register_handlers
    register_handlers(application)
    
    # Add the global message handler for AI discussions LAST
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, discuss_books))
    
    application.add_error_handler(error_handler)

    print("🤖 Bot is starting...")
    
    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if loop.is_running():
        try:
            import nest_asyncio
            nest_asyncio.apply()
        except ImportError:
            pass
        
    application.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
