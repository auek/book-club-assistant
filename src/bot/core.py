import logging
import os
from telegram import Update
from telegram.ext import ContextTypes, PicklePersistence, CommandHandler
from src.bot.commands.confirm import confirm_yes, confirm_no

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
