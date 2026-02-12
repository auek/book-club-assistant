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
    """Send the reading log, split into chunks if needed."""
    try:
        with open("reading_log.md", "r", encoding="utf-8") as f:
            book_log = f.read()
    except FileNotFoundError:
        logger.error("reading_log.md not found")
        await update.message.reply_text("Error: Book log not found. Run sync first.")
        return
    except Exception as e:
        logger.exception(f"Unexpected error reading reading_log.md: {e}")
        await update.message.reply_text("Error reading book log. Check logs.")
        return

    # Telegram message length limit
    max_length = 4096
    if len(book_log) <= max_length:
        # Try sending with Markdown, fall back to plain text on error
        try:
            await update.message.reply_text(f"Here are your books:\n{book_log}", parse_mode='Markdown')
        except BadRequest as e:
            logger.warning(f"Markdown parse error, falling back to plain text: {e}")
            # Fall back to plain text
            await update.message.reply_text(f"Here are your books:\n{book_log}", parse_mode=None)
        except Exception as e:
            logger.exception(f"Error sending book log: {e}")
            await update.message.reply_text("Error sending book log. Check logs.")
    else:
        # Split into chunks
        parts = [book_log[i:i+max_length] for i in range(0, len(book_log), max_length)]
        for i, part in enumerate(parts):
            prefix = f"Part {i+1}/{len(parts)}:\n" if len(parts) > 1 else ""
            try:
                await update.message.reply_text(f"{prefix}{part}", parse_mode='Markdown')
            except BadRequest as e:
                logger.warning(f"Markdown parse error in chunk {i+1}, using plain text: {e}")
                await update.message.reply_text(f"{prefix}{part}", parse_mode=None)
            except Exception as e:
                logger.exception(f"Error sending chunk {i+1}: {e}")
                await update.message.reply_text(f"Error sending part {i+1} of book log.")

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
    """Show the current reading progress."""
    try:
        with open("reading_in_progress.md", "r", encoding="utf-8") as f:
            progress = f.read()
        try:
            await update.message.reply_text(f"Current reading:\n{progress}", parse_mode='Markdown')
        except BadRequest:
            await update.message.reply_text(f"Current reading:\n{progress}", parse_mode=None)
    except FileNotFoundError:
        logger.warning("reading_in_progress.md not found")
        await update.message.reply_text("No reading in progress file found.")
    except Exception as e:
        logger.exception(f"Error in show_progress: {e}")
        await update.message.reply_text("Error reading progress file.")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors in telegram bot updates."""
    logger.error("Exception while handling an update:", exc_info=context.error)
    if update and isinstance(update, Update):
        try:
            await update.message.reply_text("Sorry, an error occurred. Check the bot logs.")
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

if __name__ == "__main__":
    main()
