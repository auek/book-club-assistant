# 🗺️ Comprehensive Roadmap for Bookclub-Bot

## 🎯 Overview
This document outlines the progression from a monolithic script-based system to a modular architecture supporting PC and Raspberry Pi, with future AI and database integrations.

## 📋 Current Status (Baseline)
- ✅ `./bookclub -sync` works (legacy `sync_books.py`)
- ✅ `python telegram_bot.py` works (legacy monolithic bot)
- ✅ `src/` structure established and core modules refactored.

**Implementation Status (Updated: 2026-02-14):**
- ✅ **Phases 0-4** (Refactoring & Modularization) are COMPLETED.
- ✅ **Features 1-4** (Robustness, Testing, UX, AI) are COMPLETED.

---

### 📖 Backlog (Stories S-L)

#### Story 1: Auto-Backups [S]
- [ ] **Auto-Backups**: Extend `storage.py` to create timestamped backups of `reading_log.md` before overwriting.

#### Story 2: Persistent Bot Memory [M]
- [ ] **Persistent Memory**: Implement `PicklePersistence` for the Telegram bot to preserve conversation history across restarts.
    - *Security Note*: Ensure file permissions are restricted (chmod 600) and evaluate risks of using `pickle` with sensitive data.

#### Story 3: Decouple Development Tools [S] (COMPLETED)
- [x] **Clean Launchers**: Remove `-dev` and `-chat` (CLI) modes from `bookclub` and `bookclub.pi`.
- [x] **Tool Agnosticism**: Remove `.aider.chat.yml` and `.aider.dev.yml` from the repository.
- [x] **Persona Extraction**: Move general architect instructions from `ARCHITECT.md` to global user config and replace with a project-specific `AGENTS.md`.
- [x] **Git Cleanup**: Update `.gitignore` to ignore any local IDE or LLM-tool specific configurations.

#### Story 4: API Key Separation [S]
- [ ] **Credential Isolation**: Separate OpenRouter API keys for development (Aider) and production (Bot).
    - *Goal*: Enable granular cost tracking and improve security by isolating the Raspberry Pi's credentials from the development environment.
    - [ ] Generate a new OpenRouter key specifically for the Bot.
    - [ ] Update `.env` on the Raspberry Pi with the new key.
    - [ ] Verify that Aider continues to use the global key from `~/.aider.conf.yml`.

#### Story 5: Garmin Connect Integration (Health & Workouts) [L]
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
*See [ARCHIVE.md](ARCHIVE.md) for completed tasks and historical milestones.*
