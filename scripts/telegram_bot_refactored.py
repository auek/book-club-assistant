import os
import sys
import logging
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler

# Add parent directory to path to import from src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.bot.core import error_handler
from src.bot.commands.base import start, help_command, discuss_books
from src.bot.commands.books import show_books
from src.bot.commands.progress import show_progress

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

    # Use a more robust initialization to avoid Python 3.13 compatibility issues
    # We avoid run_polling() which triggers the Updater class bug on Python 3.13
    application = ApplicationBuilder().token(token).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("books", show_books))
    application.add_handler(CommandHandler("progress", show_progress))
    application.add_handler(CommandHandler("discuss", discuss_books))
    
    application.add_error_handler(error_handler)

    print("🤖 Refactored bot is starting...")
    
    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if loop.is_running():
        # If we are in an environment with a running loop (like some IDEs)
        import nest_asyncio
        nest_asyncio.apply()
        
    application.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
