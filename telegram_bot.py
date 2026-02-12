import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.error import BadRequest
from telegram.ext import Application, CommandHandler, ContextTypes

# Load environment variables
load_dotenv()

# Configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Enhanced logging configuration
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# Configure file handler
file_handler = logging.FileHandler('telegram_bot.log', encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(log_format))

# Configure console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(log_format))

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[file_handler, console_handler]
)
logger = logging.getLogger(__name__)

def auth_only(func):
    """Decorator to restrict access to authorized chat ID."""
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        incoming_chat_id = str(update.effective_chat.id)
        logger.info(f"Auth check: incoming chat ID {incoming_chat_id}, allowed {CHAT_ID}")
        if CHAT_ID and incoming_chat_id != CHAT_ID:
            logger.warning(f"Unauthorized access from chat ID: {incoming_chat_id}")
            await update.message.reply_text("⛔ Unauthorized access.")
            return
        return await func(update, context)
    return wrapper

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
/progress - Show current reading
/discuss - Start a discussion about your books
"""
    await update.message.reply_text(help_text)

@auth_only
async def show_books(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the reading log in a nice formatted way for Telegram."""
    try:
        with open("reading_log.md", "r", encoding="utf-8") as f:
            book_log = f.read()
    except FileNotFoundError:
        logger.error("reading_log.md not found")
        await update.message.reply_text("❌ Error: Book log not found. Run sync first.")
        return
    except Exception as e:
        logger.exception(f"Unexpected error reading reading_log.md: {e}")
        await update.message.reply_text("❌ Error reading book log. Check logs.")
        return

    # Format books for better Telegram display
    formatted_books = format_books_for_telegram(book_log)
    
    # Telegram message length limit
    max_length = 4096
    
    if len(formatted_books) <= max_length:
        try:
            await update.message.reply_text(formatted_books, parse_mode='HTML')
        except BadRequest as e:
            logger.warning(f"HTML parse error, falling back to plain text: {e}")
            # Remove HTML tags and send as plain text
            plain_text = formatted_books.replace('<b>', '').replace('</b>', '').replace('<i>', '').replace('</i>', '')
            await update.message.reply_text(plain_text, parse_mode=None)
        except Exception as e:
            logger.exception(f"Error sending book list: {e}")
            await update.message.reply_text("❌ Error sending book list. Check logs.")
    else:
        # Split into chunks using our helper function
        parts = split_text_into_chunks(formatted_books, max_length)
        for i, part in enumerate(parts):
            prefix = f"📚 <b>Part {i+1}/{len(parts)}</b>\n\n" if len(parts) > 1 else ""
            try:
                await update.message.reply_text(f"{prefix}{part}", parse_mode='HTML')
            except BadRequest as e:
                logger.warning(f"HTML parse error in chunk {i+1}, using plain text: {e}")
                plain_part = part.replace('<b>', '').replace('</b>', '').replace('<i>', '').replace('</i>', '')
                plain_prefix = f"📚 Part {i+1}/{len(parts)}:\n\n" if len(parts) > 1 else ""
                await update.message.reply_text(f"{plain_prefix}{plain_part}", parse_mode=None)
            except Exception as e:
                logger.exception(f"Error sending chunk {i+1}: {e}")
                await update.message.reply_text(f"❌ Error sending part {i+1} of book list.")

@auth_only
async def discuss_books(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start a discussion about books."""
    try:
        # For now, just a placeholder
        await update.message.reply_text("Let's discuss your books! Which one are you interested in?")
    except Exception as e:
        logger.exception(f"Error in discuss_books: {e}")
        await update.message.reply_text("Error starting discussion.")

@auth_only
async def show_progress(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show the current reading progress in a nice format."""
    try:
        with open("reading_in_progress.md", "r", encoding="utf-8") as f:
            progress_content = f.read()
        
        # Format the progress content for better Telegram display
        formatted_progress = format_progress_for_telegram(progress_content)
        
        try:
            await update.message.reply_text(formatted_progress, parse_mode='HTML')
        except BadRequest as e:
            logger.warning(f"HTML parse error for progress, falling back to plain text: {e}")
            # Remove HTML tags and send as plain text
            plain_text = formatted_progress.replace('<b>', '').replace('</b>', '').replace('<i>', '').replace('</i>', '')
            await update.message.reply_text(plain_text, parse_mode=None)
        except Exception as e:
            logger.exception(f"Error sending progress: {e}")
            await update.message.reply_text("❌ Error sending reading progress. Check logs.")
            
    except FileNotFoundError:
        logger.warning("reading_in_progress.md not found")
        await update.message.reply_text("📖 No reading in progress file found. Add some books to reading_in_progress.md")
    except Exception as e:
        logger.exception(f"Error in show_progress: {e}")
        await update.message.reply_text("❌ Error reading progress file.")

def format_progress_for_telegram(markdown_text: str) -> str:
    """Format the reading progress markdown for nice Telegram display."""
    if not markdown_text.strip():
        return "📖 <b>Pågående läsning</b>\n\nInga böcker i pågående läsning för tillfället."
    
    lines = markdown_text.strip().split('\n')
    formatted_lines = ["📖 <b>Pågående läsning</b>\n"]
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check for markdown headings
        if line.startswith('# '):
            formatted_lines.append(f"\n<b>{line[2:]}</b>")
        elif line.startswith('## '):
            formatted_lines.append(f"\n<i>{line[3:]}</i>")
        elif line.startswith('### '):
            formatted_lines.append(f"\n{line[4:]}")
        # Check for bullet points
        elif line.startswith('- '):
            formatted_lines.append(f"• {line[2:]}")
        # Check for numbered lists
        elif line[0].isdigit() and '. ' in line:
            formatted_lines.append(f"  {line}")
        # Check for markdown links [text](url)
        elif '[' in line and ']' in line and '(' in line and ')' in line:
            # Simple link formatting for Telegram HTML
            try:
                text_start = line.find('[')
                text_end = line.find(']')
                url_start = line.find('(')
                url_end = line.find(')')
                
                if text_start < text_end < url_start < url_end:
                    text = line[text_start+1:text_end]
                    url = line[url_start+1:url_end]
                    formatted_line = line[:text_start] + f'<a href="{url}">{text}</a>' + line[url_end+1:]
                    formatted_lines.append(formatted_line)
                else:
                    formatted_lines.append(line)
            except:
                formatted_lines.append(line)
        else:
            formatted_lines.append(line)
    
    # Add a footer
    formatted_lines.append("\n\n📌 <i>Uppdatera filen reading_in_progress.md för att ändra</i>")
    
    return '\n'.join(formatted_lines)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors in telegram bot updates."""
    logger.error("Exception while handling an update:", exc_info=context.error)
    if update and isinstance(update, Update):
        try:
            await update.message.reply_text("❌ Sorry, an error occurred. Check the bot logs.")
        except Exception:
            pass

def main() -> None:
    """Start the bot."""
    if not BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set in .env file.")
        print("❌ Error: TELEGRAM_BOT_TOKEN not set in .env file.")
        return

    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add error handler
    application.add_error_handler(error_handler)

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("books", show_books))
    application.add_handler(CommandHandler("discuss", discuss_books))
    application.add_handler(CommandHandler("progress", show_progress))

    # Run the bot until Ctrl-C
    logger.info("🤖 Bot is starting...")
    print("🤖 Bot is running... Check telegram_bot.log for logs. Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

def format_books_for_telegram(markdown_text: str) -> str:
    """Convert markdown table to a more readable Telegram format."""
    lines = markdown_text.split('\n')
    formatted_lines = []
    
    # Find the table section
    in_table = False
    book_count = 0
    table_rows = []
    
    # First, collect all table rows
    for line in lines:
        if line.startswith('|') and 'Titel' in line and 'Författare' in line:
            in_table = True
            continue  # Skip header row
        elif line.startswith('|') and in_table:
            table_rows.append(line)
        elif line.startswith('## Sammanfattning'):
            in_table = False
    
    # Process each table row
    for i, line in enumerate(table_rows):
        parts = [part.strip() for part in line.split('|') if part.strip()]
        if len(parts) >= 5:
            title, author, rating, date, link = parts[0], parts[1], parts[2], parts[3], parts[4]
            book_count += 1
            
            # Format rating with stars
            try:
                rating_int = int(rating)
                stars = '⭐' * rating_int + '☆' * (5 - rating_int) if rating_int <= 5 else rating
            except ValueError:
                stars = rating
            
            # Format the book entry
            formatted_lines.append(f"<b>{book_count}. {title}</b>")
            formatted_lines.append(f"   👤 <i>{author}</i>")
            formatted_lines.append(f"   {stars} | 📅 {date}")
            # Add a blank line between books, but not after the last one
            if i < len(table_rows) - 1:
                formatted_lines.append("")
    
    # Add summary section
    in_summary = False
    for line in lines:
        if line.startswith('## Sammanfattning'):
            formatted_lines.append("\n📊 <b>Sammanfattning</b>")
            in_summary = True
        elif in_summary and line.startswith('- **'):
            if 'Totalt antal böcker:' in line:
                formatted_lines.append(line.replace('- **', '📚 ').replace('**', ''))
            elif 'Högsta betyg:' in line:
                formatted_lines.append(line.replace('- **', '🏆 ').replace('**', ''))
            elif 'Senaste bok:' in line:
                formatted_lines.append(line.replace('- **', '🆕 ').replace('**', ''))
            elif 'Äldsta bok:' in line:
                formatted_lines.append(line.replace('- **', '📜 ').replace('**', ''))
    
    # If no books were found in table format, return original with header
    if book_count == 0:
        return f"📚 <b>Lästa Böcker</b>\n\n{markdown_text}"
    
    # Add header
    result = f"📚 <b>Lästa Böcker</b> ({book_count} böcker)\n\n"
    result += "\n".join(formatted_lines)
    
    return result

def split_text_into_chunks(text: str, max_length: int) -> list:
    """Split text into chunks that don't exceed max_length."""
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    current_chunk = ""
    
    # Split by lines to avoid breaking in the middle of formatting
    lines = text.split('\n')
    
    for line in lines:
        if len(current_chunk) + len(line) + 1 <= max_length:
            current_chunk += line + "\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = line + "\n"
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

if __name__ == "__main__":
    main()
