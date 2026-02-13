# Book Club Sync

A lightweight Bash/Python tool to synchronize read books from Goodreads to a local Markdown log.

## Features
- Fetches read books from Goodreads via RSS.
- Generates a clean Markdown table with metadata (title, author, rating, date, link).
- AI-powered book discussions via Telegram (Grok/DeepSeek).
- Automatic cleanup of temporary files.
- **Telegram Bot** to view reading logs and current progress via chat.
- **Health Checks** to ensure environment readiness on Raspberry Pi/Volumio.

## Requirements
- Python 3.10+
- Zsh or Bash
- Goodreads User ID (Public profile)
- Telegram Bot Token (for bot features)
- XAI/DeepSeek API Key (for AI features)

## Quick Setup
1. Clone the repository.
2. Create a `.env` file with your credentials:
   ```env
   GOODREADS_USER_ID='your_user_id_here'
   TELEGRAM_BOT_TOKEN='your_bot_token_here'
   TELEGRAM_CHAT_ID='your_chat_id_here'
   XAI_API_KEY='your_key_here'
   ```
   Find your User ID at [goodreads.com/settings](https://www.goodreads.com/settings).
3. Run the health check to verify setup:
   ```bash
   python3 -m src.cli.health
   ```
4. Run `./bookclub -sync` to fetch and generate the log.

## Usage
```bash
# Synchronize books from Goodreads
./bookclub -sync

# Start AI chat about your books (uses Grok)
./bookclub -chat

# Development mode with DeepSeek
./bookclub -dev

# Start the Telegram Bot (optimized for Raspberry Pi)
./bookclub.pi -bot
```

## Telegram Bot Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a bot via [@BotFather](https://t.me/botfather) on Telegram and copy the token.
3. Run `python3 get_chat_id.py` to find your chat ID (send a message to your bot first).
4. Start the bot:
   ```bash
   ./bookclub.pi -bot
   ```

## System Health
To verify that the environment is correctly configured (especially on Raspberry Pi):
```bash
python3 -m src.cli.health
```

### Bot Commands
- `/start` – Välkomstmeddelande
- `/help` – Visa tillgängliga kommandon
- `/books` – Visa hela läsloggen
- `/progress` – Visa pågående läsning
- `/discuss` – Starta en diskussion om böckerna

## Project Structure
- `src/` – Modular Python source code (Bot, Sync, CLI, Data, Utils).
- `bookclub` – Main entry point script (Bash).
- `bookclub.pi` – Raspberry Pi optimized entry point.
- `reading_log.md` – Generated reading log (git-ignored).
- `reading_in_progress.md` – Current reading status (git-ignored).
- `tests/` – Integration tests for formatters and sync logic.

## Workflow
1. `-sync` fetches RSS data → creates `raw_books.xml` → parses to `reading_log.md`.
2. `-chat` or `/discuss` reads `reading_log.md` and initializes the LLM context.
3. Temporary files are automatically deleted after synchronization.
4. The system is designed to run efficiently on low-resource hardware like Raspberry Pi.

## Licens
MIT
