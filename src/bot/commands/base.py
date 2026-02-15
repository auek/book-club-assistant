from telegram import Update
from src.utils.llm import get_ai_response
from telegram.ext import ContextTypes
from src.bot.middleware.auth import auth_only

@auth_only
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message."""
    await update.message.reply_text("Välkommen till din bokklubbs-bot! ✨")

@auth_only
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a help message."""
    help_text = """
Tillgängliga kommandon:
/start - Välkomstmeddelande
/help - Visa denna hjälp
/books - Visa läsloggen
/progress - Visa eller uppdatera aktuell lässtatus
    Användning: /progress [1-100] för att uppdatera procent
"""
    await update.message.reply_text(help_text)

@auth_only
async def discuss_books(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle general messages as a discussion about books."""
    user_query = update.message.text
    
    if not user_query or len(user_query) < 2:
        return

    if 'history' not in context.user_data:
        context.user_data['history'] = []

    response = await get_ai_response(user_query, context.user_data['history'])
    
    # Update history
    context.user_data['history'].append({"role": "user", "content": user_query})
    context.user_data['history'].append({"role": "assistant", "content": response})
    
    # Keep only last 40 messages (20 exchanges)
    if len(context.user_data['history']) > 40:
        context.user_data['history'] = context.user_data['history'][-40:]

    try:
        await update.message.reply_text(response, parse_mode='Markdown')
    except Exception:
        # Fallback to plain text if Markdown parsing fails (e.g. malformed markdown from LLM)
        await update.message.reply_text(response)
