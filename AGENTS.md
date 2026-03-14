# Project Guide: Bookclub-Bot

You are assisting in the development of a private literary companion. This project is a specialized bridge between a user's reading history (Goodreads) and an LLM, allowing for context-aware discussions about books.

## 🏗 Project Architecture & Data Flow

### 1. Data Ingestion (Sync)
- **Source:** Goodreads RSS feed (public profile).
- **Process:** `src/sync/fetch.py` retrieves XML -> `src/sync/parse.py` converts to `Book` dataclasses -> `src/sync/render.py` generates `reading_log.md`.
- **Trigger:** Manual via `/sync` bot command or `./bookclub -sync` CLI.

### 2. Reading State
- **Active Book:** Stored in `reading_in_progress.md`. 
- **Validation:** When a user runs `/read`, `src/utils/llm.py` uses an LLM to correct titles/authors. A confirmation flow (`/yes` or `/no`) is required before updating the file.
- **Progress:** Updated via `/progress <percentage>`, which modifies the `Framsteg: XX%` line in the markdown file.

### 3. AI Discussion
- **Engine:** Uses OpenRouter (default: Gemini Flash 2.0).
- **Context:** The system prompt in `docs/BOOKCLUB_CHAT.md` instructs the AI to read both `reading_log.md` and `reading_in_progress.md`.
- **Language:** Internal logic and documentation are in English; the bot persona and user responses are in Swedish.

## 📂 Directory Structure
- `src/bot/`: Telegram bot handlers, commands, and formatting middleware.
- `src/cli/`: Entry points for bot service, sync utility, and health checks.
- `src/data/`: Data models and filesystem storage abstractions.
- `src/sync/`: Logic for Goodreads RSS fetching, parsing, and rendering.
- `src/utils/`: Configuration management, logging, and LLM wrappers.
- `docs/`: Project documentation, roadmap, and AI system prompts.
- `tests/`: Pytest suite covering data parsing, bot formatters, and state transitions.

## 📋 Project Management & Evolution
- **Roadmap:** Consult `docs/ROADMAP.md` for planned features, active stories, and the long-term vision. Use this for inspiration when suggesting improvements.
- **Archive:** Consult `docs/ARCHIVE.md` to understand the historical evolution of the project and to verify if a feature has already been implemented.
- **Workflow:** When a story or milestone from the Roadmap is completed, it must be moved to `docs/ARCHIVE.md` with the completion date.

## 🎯 Development Principles
1. **File-Based Persistence:** We prioritize Markdown for human-readability. The system treats Markdown as the primary database.
2. **Auth-First:** All command handlers must be wrapped with the `@auth_only` decorator.
3. **Graceful Degradation:** If the LLM is unavailable, the bot must still support basic book listing and progress updates.

## 🧪 Testing Standards
- **Mocking:** Tests must never hit external APIs (Goodreads/OpenRouter). Use `unittest.mock`.
- **Coverage:** Changes to `src/bot/middleware/formatters.py` or `src/sync/parse.py` must be accompanied by updated tests.
- **Execution:** Run `pytest` before finalizing changes.

## 🚫 Forbidden Practices
- **No Agentic Bot Execution:** NEVER start the bot (`./bookclub -bot`) within a development session to avoid log pollution and state conflicts.
- **No Hardcoded IDs:** Always use `TELEGRAM_CHAT_ID` from the environment for authorization.
