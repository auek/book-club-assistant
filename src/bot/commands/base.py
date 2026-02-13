from telegram import Update
from src.utils.llm import get_ai_response
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message."""
    await update.message.reply_text("Welcome to your book club bot! ✨")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a help message."""
    help_text = """
Available commands:
/start - Welcome message
/help - Show this help
/books - Show reading log
/progress - Show or update current reading progress
    Usage: /progress [1-100] to update percentage
/discuss - Start a discussion about your books
"""
    await update.message.reply_text(help_text)

async def discuss_books(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start a discussion about books."""
    user_query = update.message.text.replace('/discuss', '').strip()
    response = await get_ai_response(user_query)
    await update.message.reply_text(response)
