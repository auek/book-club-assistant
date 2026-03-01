import logging
import re
from telegram import Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes
from src.bot.middleware.auth import auth_only
from src.bot.middleware.formatters import format_progress_for_telegram
from src.data.storage import read_file_content

logger = logging.getLogger(__name__)

@auth_only
async def show_progress(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show current reading progress or update it with a percentage."""
    args = context.args
    if args:
        try:
            val = int(args[0])
            if 0 <= val <= 100:
                if val == 100:
                    with open("reading_in_progress.md", "w", encoding="utf-8") as f:
                        f.write("# Pågående läsning\n\nIngen bok läses just nu.")
                    await update.message.reply_text("✅ Grattis! Boken är avslutad. Glöm inte att logga den på Goodreads!")
                    return

                if await update_progress_file(val):
                    content = read_file_content("reading_in_progress.md")
                    formatted = format_progress_for_telegram(content)
                    await update.message.reply_text(f"✅ Uppdaterat till {val}%\n\n{formatted}", parse_mode='HTML')
                else:
                    await update.message.reply_text("❌ Kunde inte uppdatera filen.")
            else:
                await update.message.reply_text("❌ Please provide a number between 0 and 100.")
        except ValueError:
            await update.message.reply_text("❌ Please provide a valid number.")
    else:
        content = read_file_content("reading_in_progress.md")
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
    file_path = "reading_in_progress.md"
    try:
        content = read_file_content(file_path)
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
        
        with open(file_path, "w", encoding="utf-8") as f:
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
    
    input_text = " ".join(context.args)
    if " - " in input_text:
        parts = input_text.split(" - ", 1)
        new_content = f"# Pågående läsning\n\n## {parts[0].strip()}\n- Författare: {parts[1].strip()}\n- Framsteg: 0%"
    else:
        new_content = f"# Pågående läsning\n\n## {input_text}\n- Framsteg: 0%"
    
    try:
        with open("reading_in_progress.md", "w", encoding="utf-8") as f:
            f.write(new_content)
        await update.message.reply_text(f"📖 Nu läser vi: <b>{input_text}</b>", parse_mode='HTML')
    except Exception as e:
        logger.error(f"Error starting new book: {e}")
        await update.message.reply_text("❌ Kunde inte uppdatera filen.")
