import os
from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ContextTypes
from datetime import datetime

# Load environment variables
load_dotenv()

# Configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome to your book club bot! ✨"
    )

def show_books(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        with open("reading_log.md", "r", encoding="utf-8") as f:
            book_log = f.read()
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Here are your books:\n" + book_log,
            parse_mode='Markdown'
        )
    except FileNotFoundError:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Error: Book log not found"
        )

def discuss_books(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        with open("reading_log.md", "r", encoding="utf-8") as f:
            book_log = f.read()
            # Implementation for actual book discussion goes here
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Let's discuss your books! Which one are you interested in?",
                parse_mode='Markdown'
            )
    except FileNotFoundError:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Error: Book log not found"
        )

def main() -> None:
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("books", show_books))
    dispatcher.add_handler(CommandHandler("discuss", discuss_books))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
