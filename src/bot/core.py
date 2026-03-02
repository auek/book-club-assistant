import logging
import os
from telegram import Update
from telegram.ext import ContextTypes, PicklePersistence, CommandHandler, Application
from src.bot.commands.confirm import confirm_yes, confirm_no
from src.bot.commands.books import show_books
from src.bot.commands.progress import show_progress, start_reading
# Import other command handlers as needed

logger = logging.getLogger(__name__)

def get_persistence():
    """Initialize and return the persistence instance."""
    persistence_file = "bot_persistence.pickle"
    # Ensure the file has restricted permissions if it exists
    if os.path.exists(persistence_file):
        os.chmod(persistence_file, 0o600)
    return PicklePersistence(filepath=persistence_file)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors in telegram bot updates."""
    logger.error("Exception while handling an update:", exc_info=context.error)
    if update and isinstance(update, Update) and update.message:
        try:
            await update.message.reply_text("❌ Sorry, an error occurred. Check the bot logs.")
        except Exception:
            pass

def register_handlers(application: Application) -> None:
    """Register all command handlers to the application."""
    # Import here to avoid circular imports
    from src.bot.commands.base import start, help_command
    from src.bot.commands.info import show_info
    from src.bot.commands.sync import sync_books
    
    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("books", show_books))
    application.add_handler(CommandHandler("progress", show_progress))
    application.add_handler(CommandHandler("read", start_reading))
    application.add_handler(CommandHandler("yes", confirm_yes))
    application.add_handler(CommandHandler("no", confirm_no))
    application.add_handler(CommandHandler("info", show_info))
    application.add_handler(CommandHandler("sync", sync_books))
