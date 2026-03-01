import logging
from telegram import Update
from telegram.ext import ContextTypes
from src.bot.middleware.auth import auth_only
from src.data.storage import get_pending_confirmation, clear_pending_confirmation

logger = logging.getLogger(__name__)

@auth_only
async def confirm_yes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Confirm the pending book and save it."""
    chat_id = update.effective_chat.id
    pending = get_pending_confirmation(chat_id)
    
    if not pending:
        await update.message.reply_text("❌ Inget pending bekräftelse. Använd /read först.")
        return
    
    corrected = pending.get("corrected", {})
    title = corrected.get("title", "")
    author = corrected.get("author", "")
    
    # Build the content (same as in start_reading)
    if author:
        new_content = f"# Pågående läsning\n\n## {title}\n- Författare: {author}\n- Framsteg: 0%"
    else:
        new_content = f"# Pågående läsning\n\n## {title}\n- Framsteg: 0%"
    
    try:
        with open("reading_in_progress.md", "w", encoding="utf-8") as f:
            f.write(new_content)
        
        clear_pending_confirmation(chat_id)
        
        if author:
            await update.message.reply_text(f"✅ Sparat: <b>{title}</b> av {author}", parse_mode='HTML')
        else:
            await update.message.reply_text(f"✅ Sparat: <b>{title}</b>", parse_mode='HTML')
            
    except Exception as e:
        logger.error(f"Error saving confirmed book: {e}")
        await update.message.reply_text("❌ Kunde inte spara boken.")

@auth_only
async def confirm_no(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Cancel the pending book."""
    chat_id = update.effective_chat.id
    pending = get_pending_confirmation(chat_id)
    
    if not pending:
        await update.message.reply_text("❌ Inget pending bekräftelse. Använd /read först.")
        return
    
    clear_pending_confirmation(chat_id)
    await update.message.reply_text("❌ Avbröt. Ange boken igen med /read Titel - Författare")
