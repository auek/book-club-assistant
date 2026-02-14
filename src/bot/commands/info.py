from telegram import Update
from telegram.ext import ContextTypes
from src.bot.middleware.auth import auth_only
from src.utils.llm import get_usage_report

@auth_only
async def show_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Visar statistik om botens användning och konfiguration."""
    stats = get_usage_report()
    
    # Simple cost estimation (example for Gemini Flash: ~$0.10 per 1M tokens)
    estimated_cost = (stats["total_tokens"] / 1_000_000) * 0.10

    message = (
        "🤖 *Systeminformation*\n"
        f"───\n"
        f"*Modell:* `{stats['model']}`\n"
        f"*Antal anrop:* `{stats['request_count']}`\n"
        f"*Prompt tokens:* `{stats['prompt_tokens']}`\n"
        f"*Svars-tokens:* `{stats['completion_tokens']}`\n"
        f"*Totalt:* `{stats['total_tokens']}`\n"
        f"*Uppskattad kostnad:* `${estimated_cost:.4f}`\n"
        f"───\n"
        "_Statistik återställs vid omstart._"
    )
    
    await update.message.reply_text(message, parse_mode='Markdown')
