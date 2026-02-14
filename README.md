# Book Club Sync

A lightweight Bash/Python tool to synchronize read books from Goodreads to a local Markdown log.

## Features
- **Sync:** Fetches read books from Goodreads via RSS and generates a clean Markdown log.
- **Bot:** A Telegram interface to view logs, track reading progress, and discuss books with AI.
- **Multi-Platform:** Optimized for both standard PC (Linux/macOS) and Raspberry Pi (Debian/Volumio).
- **Robust:** Built-in health checks and error handling for API and file operations.

## Requirements
- Python 3.10+
- Goodreads User ID (Public profile)
- Telegram Bot Token & Chat ID
- OpenRouter API Key (for AI features)

## Quick Setup
1. Clone the repository.
2. Create a `.env` file:
   ```env
   GOODREADS_USER_ID='your_id'
   TELEGRAM_BOT_TOKEN='your_token'
   TELEGRAM_CHAT_ID='your_chat_id'
   OPENROUTER_API_KEY='your_key'
   CHAT_MODEL='google/gemini-2.0-flash-001'
   ```
3. Run health check: `python3 -m src.cli.health`

## Usage

### On PC (Linux/macOS)
Use the `./bookclub` launcher:
```bash
./bookclub -sync   # Sync books from Goodreads
./bookclub -bot    # Start the Telegram bot
```

### On Raspberry Pi
Use the `./bookclub.pi` launcher (optimized for Pi environments):
```bash
./bookclub.pi -setup  # Install system dependencies
./bookclub.pi -sync   # Sync books
./bookclub.pi -bot    # Start the bot
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
