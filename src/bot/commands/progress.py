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
                if await update_progress_file(val):
                    await update.message.reply_text(f"✅ Progress updated to {val}%")
                else:
                    await update.message.reply_text("❌ Could not update progress file.")
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
    """Update the reading_in_progress.md file with new progress percentage."""
    try:
        content = read_file_content("reading_in_progress.md")
        lines = content.split('\n')
        updated_lines, updated = [], False
        for line in lines:
            if any(kw in line.lower() for kw in ['progress:', 'framsteg:', '%']):
                new_line = re.sub(r'(\d{1,3})%', f'{percentage}%', line)
                updated_lines.append(new_line)
                updated = True
            else:
                updated_lines.append(line)
        if not updated:
            updated_lines.append(f"\n\n**Progress:** {percentage}%")
        
        with open("reading_in_progress.md", "w", encoding="utf-8") as f:
            f.write('\n'.join(updated_lines))
        return True
    except Exception as e:
        logger.exception(f"Error updating progress: {e}")
        return False
