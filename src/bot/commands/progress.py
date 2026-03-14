import logging
import re
from telegram import Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes
from src.bot.middleware.auth import auth_only
from src.bot.middleware.formatters import format_progress_for_telegram
from src.data.storage import read_file_content, save_pending_confirmation, get_pending_confirmation, clear_pending_confirmation
from src.utils.llm import validate_book_title
from src.utils.config import BASE_DIR

logger = logging.getLogger(__name__)

PROGRESS_FILE = BASE_DIR / "reading_in_progress.md"

@auth_only
async def show_progress(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show current reading progress or update it with a percentage."""
    args = context.args
    if args:
        try:
            val = int(args[0])
            if 0 <= val <= 100:
                if val == 100:
                    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
                        f.write("# Pågående läsning\n\nIngen bok läses just nu.")
                    await update.message.reply_text("✅ Grattis! Boken är avslutad. Glöm inte att logga den på Goodreads!")
                    return

                if await update_progress_file(val):
                    content = read_file_content(PROGRESS_FILE)
                    formatted = format_progress_for_telegram(content)
                    await update.message.reply_text(f"✅ Uppdaterat till {val}%\n\n{formatted}", parse_mode='HTML')
                else:
                    await update.message.reply_text("❌ Kunde inte uppdatera filen.")
            else:
                await update.message.reply_text("❌ Please provide a number between 0 and 100.")
        except ValueError:
            await update.message.reply_text("❌ Please provide a valid number.")
    else:
        content = read_file_content(PROGRESS_FILE)
        if not content:
            await update.message.reply_text("📖 No reading in progress file found.")
            return
        
        formatted = format_progress_for_telegram(content)
        try:
            await update.message.reply_text(formatted, parse_mode='HTML')
        except BadRequest:
            plain = formatted.replace('<b>', '').replace('</b>', '').replace('<i>', '').replace('</i>', '')
            await update.message.reply_text(plain, parse_mode=None)

async def update_progress_file(percentage: int) -> bool:
    """Update the reading_in_progress.md file with new progress percentage in Swedish."""
    try:
        content = read_file_content(PROGRESS_FILE)
        if not content:
            return False
            
        lines = content.split('\n')
        updated_lines, updated = [], False
        
        # Match 'Framsteg:' case-insensitively
        for line in lines:
            if re.search(r'Framsteg:', line, re.IGNORECASE):
                # Replace the digits before the %
                new_line = re.sub(r'\d+%', f'{percentage}%', line)
                updated_lines.append(new_line)
                updated = True
            else:
                updated_lines.append(line)
        
        # If no 'Framsteg:' line exists, append it under the last book entry or end of file
        if not updated:
            updated_lines.append(f"- Framsteg: {percentage}%")
        
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            f.write('\n'.join(updated_lines).strip() + '\n')
        return True
    except Exception as e:
        logger.error(f"Error updating progress file: {e}")
        return False

@auth_only
async def start_reading(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Overwrite reading_in_progress.md with a new book. Usage: /read Title - Author"""
    if not context.args:
        await update.message.reply_text("❌ Ange bok: /read Titel - Författare")
        return
    
    # Check for existing pending confirmation - abort it
    chat_id = update.effective_chat.id
    if get_pending_confirmation(chat_id):
        clear_pending_confirmation(chat_id)
    
    input_text = " ".join(context.args)
    
    # Validate with LLM
    await update.message.reply_text("🔍 Validerar boken...")
    validation = await validate_book_title(input_text)
    
    if not validation.get("valid", False):
        reason = validation.get("reason", "Okänt fel")
        await update.message.reply_text(f"❌ Kunde inte identifiera boken: {reason}\n\nFörsök igen med /read Titel - Författare")
        return
    
    corrected = validation
    title = corrected.get("title", "")
    author = corrected.get("author", "")
    
    # Show confirmation prompt
    if author:
        prompt = f"Menade du: <b>{title}</b> av <b>{author}</b>?\n\nSvara /yes för att bekräfta eller /no för att avbryta."
    else:
        prompt = f"Menade du: <b>{title}</b>?\n\nSvara /yes för att bekräfta eller /no för att avbryta."
    
    # Save pending confirmation
    save_pending_confirmation(chat_id, {
        "raw_input": input_text,
        "corrected": {"title": title, "author": author}
    })
    
    await update.message.reply_text(prompt, parse_mode='HTML')
