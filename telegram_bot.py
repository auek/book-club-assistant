import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Load environment variables
load_dotenv()

# Configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def auth_only(func):
    """Decorator to restrict access to authorized chat ID."""
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if CHAT_ID and str(update.effective_chat.id) != CHAT_ID:
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
        await update.message.reply_text("Error: Book log not found. Run sync first.")
        return

    # Telegram message length limit
    max_length = 4096
    if len(book_log) <= max_length:
        await update.message.reply_text(f"Here are your books:\n{book_log}", parse_mode='Markdown')
    else:
        # Split into chunks
        parts = [book_log[i:i+max_length] for i in range(0, len(book_log), max_length)]
        for i, part in enumerate(parts):
            prefix = f"Part {i+1}/{len(parts)}:\n" if len(parts) > 1 else ""
            await update.message.reply_text(f"{prefix}{part}", parse_mode='Markdown')

@auth_only
async def discuss_books(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start a discussion about books."""
    # For now, just a placeholder
    await update.message.reply_text("Let's discuss your books! Which one are you interested in?")

@auth_only
async def show_progress(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show the current reading progress."""
    try:
        with open("reading_in_progress.md", "r", encoding="utf-8") as f:
            progress = f.read()
        await update.message.reply_text(f"Current reading:\n{progress}", parse_mode='Markdown')
    except FileNotFoundError:
        await update.message.reply_text("No reading in progress file found.")

def main() -> None:
    """Start the bot."""
    if not BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set in .env file.")
        print("❌ Error: TELEGRAM_BOT_TOKEN not set in .env file.")
        return

    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("books", show_books))
    application.add_handler(CommandHandler("discuss", discuss_books))
    application.add_handler(CommandHandler("progress", show_progress))

    # Run the bot until Ctrl-C
    print("🤖 Bot is running... Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
