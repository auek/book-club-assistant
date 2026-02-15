# 📚 Your Personal Book Club Assistant

Transform your reading journey with an "always-on" AI companion designed to live on your Raspberry Pi. This isn't just a sync tool; it's a private, intelligent space to discuss every book you've ever read or are currently devouring.

## ✨ Key Features
- **Deep Book Discussions:** Chat with an LLM that has full context of your personal library—ask for summaries, thematic analysis, or what you should read next based on your history.
- **Seamless Sync:** Automatically pulls your latest reads from Goodreads to keep your digital library up to date.
- **Progress Tracking:** Interactive Telegram commands to update your reading percentage and visualize your momentum.
- **Private & Secure:** Runs on your own hardware (Raspberry Pi) with strict Telegram authentication—your reading data and conversations stay yours.
- **Robust Architecture:** Built with automated backups, health checks, and a rolling conversation memory.

## Requirements
- Python 3.10+
- Goodreads User ID (Public profile)
- Telegram Bot Token & Chat ID
- OpenRouter API Key (for AI features)

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
To verify that the environment is correctly configured (especially on Raspberry Pi):
```bash
python3 -m src.cli.health
```

### Bot-kommandon
- `/start` – Starta boten och få ett välkomstmeddelande.
- `/help` – Visa en lista över alla tillgängliga kommandon.
- `/books` – Visa din kompletta läslogg från `reading_log.md`.
- `/progress` – Se nuvarande framsteg eller uppdatera (t.ex. `/progress 45`).
- `/sync` – Tvinga en synkronisering med Goodreads manuellt.
- `/info` – Visa systemstatus, drifttid och AI-tokenstatistik.
- *Textmeddelande* – Skriv direkt till boten för att diskutera dina böcker med AI:n.

## Project Structure
- `src/` – Modular Python source code (Bot, Sync, CLI, Data, Utils).
- `bookclub` – Main entry point script (Bash).
- `bookclub.pi` – Raspberry Pi optimized entry point.
- `reading_log.md` – Generated reading log (git-ignored).
- `reading_in_progress.md` – Current reading status (git-ignored).
- `tests/` – Integration tests for formatters and sync logic.

## Persistence (Running in Background)
To keep the bot running after closing your SSH session:

### Standard Linux (using tmux)
```bash
./bookclub -tmux
```
- **Detach:** `Ctrl+B` then `D`.
- **Reattach:** `./bookclub -tmux`.

### Raspberry Pi / Volumio (using nohup)
```bash
# Start in background
nohup ./bookclub.pi -bot > bot.log 2>&1 &

# Stop the bot
pkill -f bot_cli
```

## Licens
MIT
