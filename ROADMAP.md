# 🗺️ Comprehensive Roadmap & Migration Plan for Bookclub-Bot

## 🎯 Overview
This document outlines the progression from a monolithic script-based system to a modular architecture supporting PC and Raspberry Pi, with future AI and database integrations.

## 📋 Current Status (Baseline)
- ✅ `./bookclub -sync` works (legacy `sync_books.py`)
- ✅ `python telegram_bot.py` works (legacy monolithic bot)
- ✅ `src/` structure established and core modules refactored.

**Implementation Status (Updated: 2026-02-14):**
- ✅ **Phases 0-4** (Refactoring & Modularization) are COMPLETED.
- ✅ **Features 1-4** (Robustness, Testing, UX, AI) are COMPLETED.
- ⏳ **Story 6** (Discord Frontend) is the current priority.

---

## 🏗️ Architectural Progression

### 🧱 Enablers (Foundational - Sequential)
These tasks build the core infrastructure. They must be completed in order to ensure the modular system works as intended.

#### Phase 0: Preparation - **COMPLETED**
- Environment setup, directory creation, and legacy backups.

#### Phase 1: Sync Module Extraction - **COMPLETED**
- Logic moved to `src/sync/` (`fetch`, `parse`, `render`).
- Created `scripts/sync_books_refactored.py`.

#### Phase 2: Data Layer Extraction - **COMPLETED**
- Created `src/data/models.py` and `storage.py`.
- Isolated File I/O from business logic.

#### Phase 3: Telegram Bot Refactoring - **COMPLETED**
- Logic moved to `src/bot/` (core, middleware, commands).
- Created `scripts/telegram_bot_refactored.py`.
- ✅ Verified commands (/start, /books, /progress) on hardware.

#### Phase 4: Launcher Integration - **COMPLETED**
- **Dependency**: Phases 1-3.
- **Goal**: Switch `bookclub` and `bookclub.pi` to use the new modular code.
- ✅ Create `src/cli/sync_cli.py` and `src/cli/bot_cli.py`.
- ✅ Update Bash launchers to call `python3 -m src.cli.sync_cli`.

---

### 🚀 Features & Improvements (Independent - Flexible Order)
Once Phase 4 is complete, these can be implemented in any order.

#### Feature 1: System Robustness (Enabler/Improvement)
- ✅ **Config Validation**: `src/utils/config.py`.
- ✅ **Health Checks**: `src/cli/health.py` for API/Permission verification.

#### Feature 2: Testing & Documentation
- ✅ Unit tests with `pytest`.
- ✅ Full Raspberry Pi (Volumio) validation.
- ✅ Update `README.md` with new architecture details.

#### Feature 3: Telegram UX Enhancement - **COMPLETED**
- **Goal**: Make bot output leaner and more professional.
- ✅ Limit `/books` to the 10 most recent entries.
- ✅ Improve visual layout with better HTML formatting and separators.
- ✅ Add visual progress bars for the `/progress` command.

#### Feature 4: AI-Chat Integration - **COMPLETED**
- **Goal**: Direct Telegram interaction with the book log using LLMs.
- ✅ `src/utils/llm.py` (OpenRouter wrapper with `httpx` 0.28+ compatibility).
- ✅ Context Injection (inject `reading_log.md`, `reading_in_progress.md`, and `BOKKLUBB.md`).
- ✅ Security: Implemented prompt injection protection using delimiters and system instructions.
- ✅ Implement `/discuss` command logic in bot.
- ✅ Implement `/info` command for token usage and model tracking.
- ✅ Default text messages to AI discussion.
- ✅ **Conversation Memory**: Implemented short-term history using `context.user_data`.

---

### 📖 Backlog (Stories S-L)

#### Story 1: Auto-Backups [S]
- [ ] **Auto-Backups**: Extend `storage.py` to create timestamped backups of `reading_log.md` before overwriting.

#### Story 2: Persistent Bot Memory [M]
- [ ] **Persistent Memory**: Implement `PicklePersistence` for the Telegram bot to preserve conversation history across restarts.
    - *Security Note*: Ensure file permissions are restricted (chmod 600) and evaluate risks of using `pickle` with sensitive data.

#### Story 3: Decouple Development Tools [S]
- [ ] **Clean Launchers**: Remove `-dev` and `-chat` (CLI) modes from `bookclub` and `bookclub.pi`.
    - *Analysis*: Development tools like `aider` should be external to the project's runtime logic to avoid circular dependencies and bloated production environments.
    - *Action*: Move development instructions to a separate `CONTRIBUTING.md` or a dedicated dev-script.

#### Story 4: Garmin Connect Integration (Health & Workouts) [L]
- [ ] **Garmin Connectivity**: Implement MCP to fetch health and activity data (steps, heart rate, sleep, runs) from Garmin Connect.
    - **Goal**: Allow the LLM to analyze fitness trends and suggest personalized running workouts.
    - **Safety & Privacy Precautions (MANDATORY)**:
        - *Data Minimization*: Only fetch the specific metrics required for the requested analysis.
        - *Local Processing*: Ensure health data is processed in-memory and not stored permanently in the book log or shared logs.
        - *Medical Disclaimer*: The AI must prepend a disclaimer stating it is not a medical professional and workout suggestions should be followed at the user's own risk.
        - *Explicit Consent*: Implement a per-session confirmation before the bot accesses health endpoints.
        - *Anonymization*: Strip personal identifiers (name, GPS coordinates of home/work) before sending data to the LLM provider.

#### Story 5: MCP Integration (Notion) [L]
- [ ] **Notion Connectivity**: Implement Model Context Protocol (MCP) or direct Tool Calling to allow the AI to interact with Notion.
    - [ ] Define tool schema for searching and adding notes to Notion.
    - [ ] Implement secure credential management for Notion API keys.
    - [ ] Update `src/utils/llm.py` to handle tool-call loops.
    - [ ] **Security & Constraints**:
        - *Scope*: Restrict Notion Integration to specific databases/pages only.
        - *Safety*: Implement "Human-in-the-loop" confirmation for any write/delete actions.
        - *Privacy*: Acknowledge that retrieved data is sent to the LLM provider.
        - *Robustness*: Implement rate-limiting and token-usage guards to prevent recursive loops.

#### Story 6: Discord Frontend Integration [M]
- [ ] **Discord Bot Implementation**: Create a parallel frontend to the Telegram bot using `discord.py`.
    - **Goal**: Provide a desktop/mobile alternative that functions as a cost-effective personal assistant.
    - [ ] Implement `src/bot/discord_core.py` to handle Discord events.
    - [ ] Port existing commands (/books, /progress, /discuss) to Discord Slash Commands.
    - [ ] **Security**: Implement strict User ID whitelisting to ensure only the owner can interact with the bot.
    - [ ] **Economy**: Leverage the existing `src/utils/llm.py` with prompt caching to maintain low API costs compared to flat-rate subscriptions.

#### Story 7: Persistent SSH Sessions (tmux) [S]
- [ ] **Remote Persistence**: Install and configure `tmux` on the Raspberry Pi (Volumio).
    - **Goal**: Prevent the bot from stopping when the SSH connection is lost.
    - [ ] Install `tmux` via `apt-get`.
    - [ ] Document the workflow: `ssh` -> `tmux attach` -> run bot.
    - [ ] (Optional) Create a simple helper script to auto-attach or start a new session.

---

### 🔮 Future Evolution (Major Shifts & XL Features)

#### Feature 1: SQLite Integration [XL]
- **Goal**: Move from Markdown-parsing to a database as the "source of truth".
- [ ] `src/data/database.py` for SQLite management.
- [ ] Update Sync logic to save to DB first, then export to Markdown.
- [ ] Security considerations for local DB access is of utmost importance.

#### Feature 2: Transition to "Personal Assistant" Architecture [XL]
- **Analysis**: Evaluate if Garmin and Notion features belong in the "Bookclub" or if the project should be forked/renamed to a "Personal Assistant" framework.
- [ ] **Modular Core**: Design a core assistant that can load "plugins" (Bookclub, Garmin, Notion).
- [ ] **Head Start**: Use the existing Telegram/LLM integration as the foundation for the new project.

#### Feature 6: LLM Time Awareness
- **Goal**: Ensure the LLM knows the current local time for context-aware responses.
- ✅ Inject `datetime.now()` into the system prompt in `src/utils/llm.py`.

---

## 🗂️ Target File Structure

```
bookclub/
├── bookclub.pi                      # Pi launcher
├── bookclub                         # PC launcher
├── src/                             # Modular Python package
│   ├── cli/                         # CLI entry points (Phase 4)
│   ├── sync/                        # Goodreads sync logic (Phase 1)
│   ├── bot/                         # Telegram bot (Phase 3)
│   ├── data/                        # Data layer (Phase 2)
│   └── utils/                       # Utilities (Phase 5/7)
├── scripts/                         # Refactored standalone scripts
└── tests/                           # Test suite (Phase 6)
```

## 🧪 Testing Strategy

| Phase/Feature | Validation | Command |
|-----|-------------------|----------|
| Phase 1-3 | Output Parity | `diff reading_log.md reading_log.md.backup` |
| Phase 4 | Launcher Functionality | `./bookclub -sync` |
| Feature 3 | AI Interaction | `/chat "What should I read next?"` |

---
*Last Updated: 2026-02-13*
*Status: Phases 0-4 & Feature 1-2 completed – Next: Feature 3 (AI-Chat).*
