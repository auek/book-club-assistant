# Your Personal Book Club Assistant

A personal AI companion designed to run on low-power hardware like the Raspberry Pi. This tool provides a private space to discuss your reading history, analyze themes, and manage your digital library.

## Key Features
- **Book Discussions:** Chat with an LLM that has context of your personal library for summaries, thematic analysis, and recommendations.
- **Goodreads Sync:** Automatically pulls latest reads from Goodreads.
- **Progress Tracking:** Commands to update reading percentage and visualize momentum.
- **Private & Secure:** Host on your own hardware with Telegram authentication.
- **Robust Architecture:** Automated backups, health checks, and rolling conversation memory.

## Requirements
- Python 3.10+
- Goodreads User ID (Public profile)
- [Telegram Bot Token & Chat ID](#telegram-setup)
- OpenRouter API Key

## Telegram Setup
1. **Create a Bot:** Message [@BotFather](https://t.me/botfather) on Telegram and follow the steps to create a new bot and receive your **API Token**.
2. **Privacy Settings:** To allow the bot to read your messages for AI discussion, send `/setprivacy` to @BotFather, select your bot, and set it to **Disabled**.
3. **Get Chat ID:** Start the bot in Telegram, then run `python3 get_chat_id.py` locally to identify your unique Chat ID. This ensures only you can access the bot.
4. **Documentation:** For more details, see the [official Telegram Bot tutorial](https://core.telegram.org/bots/features#botfather).

## Installation & Setup
1. **Clone & Install:**
   ```bash
   git clone <repo-url>
   pip install -r requirements.txt
   ```
2. **Configure:** Create a `.env` file based on the requirements below. Use `python3 get_chat_id.py` to find your Telegram Chat ID.
   ```env
   GOODREADS_USER_ID='your_id'
   TELEGRAM_BOT_TOKEN='your_token'
   TELEGRAM_CHAT_ID='your_chat_id'
   OPENROUTER_API_KEY='your_key'
   CHAT_MODEL='google/gemini-2.0-flash-001'
   ```
3. **Verify:** Run `python3 -m src.cli.health` to check the environment.

## Usage
- **Sync Books:** `./bookclub -sync` (fetches from Goodreads)
- **Start Bot:** `./bookclub -bot` (Telegram interface)
- **Raspberry Pi:** Use `./bookclub.pi` for optimized setup and execution.

## System Health
To verify that the environment is correctly configured:
```bash
python3 -m src.cli.health
```

## Bot Commands
- `/start` – Initialize the bot.
- `/help` – List all available commands.
- `/books` – View entire reading log.
- `/read` – Start a new book (e.g., `/read Title - Author`). Requires confirmation with `/yes`.
- `/yes` – Confirm validated book title.
- `/no` – Cancel pending book validation.
- `/progress` – View current status or update (e.g., `/progress 45`). Use `/progress 100` to finish.
- `/sync` – Trigger a fresh sync with Goodreads.
- `/info` – Check system health, uptime, and AI usage.
- *Any text* – Start a discussion about your books with the AI.

## Project Structure
- `src/` – Python source code (Bot, Sync, CLI, Data, Utils).
- `docs/` – Project documentation, roadmap, and AI system prompts.
- `bookclub` – Main entry point script.
- `bookclub.pi` – Raspberry Pi optimized entry point.
- `reading_log.md` – Generated reading log (git-ignored).
- `reading_in_progress.md` – Current reading status (git-ignored, managed by bot).
- `tests/` – Integration tests for formatters and sync logic.

## Persistence
To keep the bot running after closing your SSH session:

### Standard Linux (using tmux)
```bash
./bookclub -tmux
```

### Raspberry Pi / Volumio (using nohup)
```bash
# Start in background
nohup ./bookclub.pi -bot > bot.log 2>&1 &

# Stop the bot
pkill -f src.cli.bot_cli
```

## License
MIT
