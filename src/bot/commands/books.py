import logging
from telegram import Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes
from src.bot.middleware.auth import auth_only
from src.bot.middleware.formatters import format_books_for_telegram, split_text_into_chunks
from src.data.storage import read_file_content

logger = logging.getLogger(__name__)

@auth_only
async def show_books(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the reading log in a nice formatted way for Telegram."""
    content = read_file_content("reading_log.md")
    if not content:
        await update.message.reply_text("❌ Error: Book log not found. Run sync first.")
        return

    formatted_books = format_books_for_telegram(content, limit=10)
    parts = split_text_into_chunks(formatted_books)
    
    for part in parts:
        try:
            await update.message.reply_text(part, parse_mode='HTML', disable_web_page_preview=True)
        except BadRequest:
            plain_part = part.replace('<b>', '').replace('</b>', '').replace('<i>', '').replace('</i>', '')
            await update.message.reply_text(f"{prefix}{plain_part}", parse_mode=None)
