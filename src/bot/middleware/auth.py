import os
import logging
from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

def auth_only(func):
    """Decorator to restrict access to authorized chat ID."""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        incoming_chat_id = str(update.effective_chat.id)
        
        if chat_id and incoming_chat_id != chat_id:
            logger.warning(f"Unauthorized access from chat ID: {incoming_chat_id}")
            await update.message.reply_text("⛔ Unauthorized access.")
            return
        return await func(update, context)
    return wrapper
