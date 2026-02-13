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

    application = ApplicationBuilder().token(token).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("books", show_books))
    application.add_handler(CommandHandler("progress", show_progress))
    application.add_handler(CommandHandler("discuss", discuss_books))
    
    application.add_error_handler(error_handler)

    print("🤖 Refactored bot is starting...")
    application.run_polling()

if __name__ == "__main__":
    main()
