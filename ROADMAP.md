# 🗺️ Comprehensive Roadmap & Migration Plan for Bookclub-Bot

## 🎯 Overview
This document outlines the progression from a monolithic script-based system to a modular architecture supporting PC and Raspberry Pi, with future AI and database integrations.

## 📋 Current Status (Baseline)
- ✅ `./bookclub -sync` works (legacy `sync_books.py`)
- ✅ `python telegram_bot.py` works (legacy monolithic bot)
- ✅ `src/` structure established and core modules refactored.

**Implementation Status (Updated: 2026-02-13):**
- ✅ **Phases 0-3** (Refactoring & Modularization) are COMPLETED.
- ❌ **Phase 4+** (Integration & New Features) are PENDING.

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

#### Feature 4: AI-Chat Integration - **IN PROGRESS**
- **Goal**: Direct Telegram interaction with the book log using LLMs.
- ✅ `src/utils/llm.py` (OpenRouter wrapper).
- ✅ Context Injection (inject `reading_log.md` into prompt).
- ✅ Implement `/discuss` command logic in bot.
- ✅ Default text messages to AI discussion.
- [ ] **Conversation Memory**: Implement short-term history (last 20 messages) using `context.user_data`.

---

### 📖 Backlog

#### Story 1: Auto-Backups
- [ ] **Auto-Backups**: Extend `storage.py` to create timestamped backups of `reading_log.md` before overwriting.

---

### 🔮 Future Evolution (Major Shifts)

#### Feature 4: SQLite Integration
- **Goal**: Move from Markdown-parsing to a database as the "source of truth".
- [ ] `src/data/database.py` for SQLite management.
- [ ] Update Sync logic to save to DB first, then export to Markdown.
- [ ] Security considerations for local DB access is of utmost importance.

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
