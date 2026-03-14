import logging
from telegram import Update
from telegram.ext import ContextTypes
from src.bot.middleware.auth import auth_only
from src.sync.fetch import fetch_goodreads_rss
from src.sync.parse import parse_xml, sort_books
from src.sync.render import generate_markdown, cleanup_files
from src.data.storage import save_reading_log
from src.utils.config import get_config, BASE_DIR

logger = logging.getLogger(__name__)

@auth_only
async def sync_books(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manually trigger the Goodreads sync process."""
    status_msg = await update.message.reply_text("🔄 Syncing with Goodreads...")
    
    try:
        # Get credentials from config
        user_id = get_config("GOODREADS_USER_ID")
        api_key = get_config("GOODREADS_API_KEY")
        
        if not user_id:
            await status_msg.edit_text("❌ Configuration missing: GOODREADS_USER_ID.")
            return

        # Execute sync workflow
        # Note: api_key might be optional depending on fetch_goodreads_rss implementation
        success = fetch_goodreads_rss(user_id, api_key or "")
        if not success:
            await status_msg.edit_text("❌ Failed to fetch RSS feed.")
            return

        books = parse_xml(str(BASE_DIR / "raw_books.xml"))
        sorted_books = sort_books(books)
        markdown = generate_markdown(sorted_books)
        save_reading_log(markdown, output_file=str(BASE_DIR / "docs" / "reading_log.md"))
        cleanup_files()

        await status_msg.edit_text("✅ Sync complete! Use /books to see updates.")
    except Exception as e:
        logger.error(f"Sync error: {e}")
        await status_msg.edit_text(f"❌ Sync failed: {str(e)}")
