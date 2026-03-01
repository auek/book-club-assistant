#!/usr/bin/env python3
import os
import sys
import logging

# Add parent directory to path to import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from src.bot.core import error_handler, get_persistence
from src.bot.commands.base import start, help_command, discuss_books
from src.bot.commands.books import show_books
from src.bot.commands.progress import show_progress, start_reading
from src.bot.commands.info import show_info
from src.bot.commands.sync import sync_books

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

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("books", show_books))
    application.add_handler(CommandHandler("progress", show_progress))
    application.add_handler(CommandHandler("read", start_reading))
    application.add_handler(CommandHandler("discuss", discuss_books))
    application.add_handler(CommandHandler("info", show_info))
    application.add_handler(CommandHandler("sync", sync_books))
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
