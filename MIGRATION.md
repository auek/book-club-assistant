# 📦 Migration to Modular Project Structure – PRACTICAL PLAN

## 🎯 Overview & Current State Assessment

Based on recent test runs, here’s what **actually works** right now:
- `./bookclub -sync` works perfectly (using the original `sync_books.py`)
- `python telegram_bot.py` works (the monolithic bot runs fine)
- `bookclub.pi` exists but lacks execute permission (`chmod +x bookclub.pi` needed)
- The modular `src/` skeleton exists (import test passes) but contains no real code yet.

**Goal**: Gradually move from the current working monolithic code to a clean modular structure **without breaking anything** that already works.

## 📁 Target Project Structure (Realistic)

```
bookclub/
├── bookclub.pi                      # Pi launcher (needs +x)
├── bookclub                         # PC launcher (unchanged)
│
├── src/                             # New modular Python package
│   ├── __init__.py
│   │
│   ├── cli/                         # CLI entry points
│   │   ├── __init__.py
│   │   ├── sync_cli.py              # CLI for sync (calls sync.*)
│   │   └── bot_cli.py               # CLI for bot (calls bot.*)
│   │
│   ├── sync/                        # Goodreads sync logic
│   │   ├── __init__.py
│   │   ├── fetch.py                 # Goodreads API & XML download
│   │   ├── parse.py                 # XML → Python objects
│   │   └── render.py                # Python objects → reading_log.md
│   │
│   ├── bot/                         # Telegram bot
│   │   ├── __init__.py
│   │   ├── core.py                  # Bot app setup, polling, error handler
│   │   ├── commands/                # Each command in separate file
│   │   │   ├── __init__.py
│   │   │   ├── start.py
│   │   │   ├── help.py
│   │   │   ├── books.py
│   │   │   ├── progress.py
│   │   │   └── discuss.py
│   │   ├── middleware/              # Auth, formatting, utilities
│   │   │   ├── auth.py
│   │   │   ├── formatters.py
│   │   │   └── utils.py
│   │   └── models.py                # Bot‑specific data models
│   │
│   ├── data/                        # Data layer (file I/O, models)
│   │   ├── __init__.py
│   │   ├── models.py                # Book, ReadingProgress
│   │   └── storage.py               # read/write reading_log.md, reading_in_progress.md
│   │
│   └── utils/                       # Cross‑cutting utilities
│       ├── __init__.py
│       ├── config.py                # Load .env, validate
│       ├── logging.py               # Consistent logging setup
│       └── dates.py                 # Date parsing/formatting helpers
│
├── scripts/                         # Stand‑alone executable scripts
│   ├── sync_books.py                # LEGACY – will become a thin wrapper
│   ├── telegram_bot.py              # LEGACY – will become a thin wrapper
│   └── get_chat_id.py               # Unchanged
│
├── config/
│   ├── settings.py                  # App constants (SYNC_INTERVAL etc.)
│   └── prompts/
│       └── BOOKCLUB_CHAT.md         # AI prompt (unchanged)
│
├── data/                            # Generated content (git‑ignored)
│   ├── reading_log.md
│   ├── reading_in_progress.md
│   └── backups/                     # Auto‑backups
│
├── logs/                            # Log files (git‑ignored)
│   ├── telegram_bot.log
│   └── sync.log
│
└── tests/
    ├── conftest.py
    ├── test_sync/
    ├── test_bot/
    └── test_utils/
```

## 🔄 Migration Phases – Step‑by‑Step

### Phase 0: Preparation (Day 1)
**Goal**: Set up the stage without touching any working code.

1. **Fix permissions** (so `bookclub.pi` can be tested):
   ```bash
   chmod +x bookclub.pi
   ```

2. **Create the empty `src/` subdirectories** (if not already there):
   ```bash
   mkdir -p src/{cli,sync,bot/{commands,middleware},data,utils}
   mkdir -p config/prompts tests/{test_sync,test_bot,test_utils}
   ```

3. **Add minimal `__init__.py` files** in each Python directory (already done in part).

4. **Update `.gitignore`** to include the new generated directories:
   ```bash
   echo -e "\n# New modular structure\ndata/\nlogs/\n__pycache__/\n*.pyc\n" >> .gitignore
   ```

5. **Create a backup** of the current working scripts:
   ```bash
   cp sync_books.py sync_books.py.backup
   cp telegram_bot.py telegram_bot.py.backup
   ```

### Phase 1: Extract the Sync Module (Days 2–3)
**Rule**: Keep the original `sync_books.py` working unchanged while building the new module alongside.

1. **Create `src/sync/fetch.py`** – move the `curl`/API logic from `sync_books.py` into a `GoodreadsClient` class.
2. **Create `src/sync/parse.py`** – move the `parse_xml()` and `sort_books()` functions.
3. **Create `src/sync/render.py`** – move `generate_markdown()` and `cleanup_files()`.
4. **Write a new `scripts/sync_books_refactored.py`** that imports from `src.sync` and reproduces the exact same behavior.
5. **Test side‑by‑side**:
   ```bash
   ./bookclub -sync                  # original
   python scripts/sync_books_refactored.py   # new module
   diff reading_log.md reading_log.md.backup
   ```
6. **Once they produce identical output**, replace the original `sync_books.py` with a thin wrapper that delegates to `src.sync`. Verify `./bookclub -sync` still works.

### Phase 2: Extract the Data Layer (Day 4)
**Goal**: Isolate file I/O and data models.

1. **Create `src/data/models.py`** with `Book` dataclass (mirroring the dict keys used in sync).
2. **Create `src/data/storage.py`** with functions:
   - `read_reading_log()` / `write_reading_log()`
   - `read_progress_file()` / `write_progress_file()`
   - `update_progress_percentage()` (the logic currently inside `update_progress_file()`)
3. **Update the sync module** to use these data functions instead of direct file I/O.
4. **Test** that the sync still works.

### Phase 3: Refactor the Telegram Bot (Days 5–7)
**Most delicate part** – the bot is currently running fine. We’ll proceed incrementally.

1. **Create `src/bot/core.py`** – move the `main()` function, application builder, and error handler.
2. **Create `src/bot/middleware/auth.py`** – move the `@auth_only` decorator.
3. **Create `src/bot/middleware/formatters.py`** – move `format_books_for_telegram`, `format_progress_for_telegram`, `split_text_into_chunks`.
4. **Create `src/bot/commands/`** – one file per command:
   - `start.py` → `async def start(...)`
   - `help.py` → `async def help_command(...)`
   - `books.py` → `async def show_books(...)`
   - `progress.py` → `async def show_progress(...)` and `_show_current_progress(...)`
   - `discuss.py` → `async def discuss_books(...)`
5. **Create `src/bot/models.py`** for any bot‑specific data structures.
6. **Write a new `scripts/telegram_bot_refactored.py`** that imports from `src.bot` and starts the bot exactly as before.
7. **Run both bots temporarily** (on different test tokens if possible) to verify they behave identically.
8. **Once confident**, replace the original `telegram_bot.py` with a thin wrapper that calls `src.bot.core.main()`.

### Phase 4: Update the Launcher Scripts (Day 8)
**Goal**: Make `bookclub` and `bookclub.pi` use the new modules internally.

1. **Create `src/cli/sync_cli.py`** – a function that mimics the `-sync` branch of `bookclub`.
2. **Create `src/cli/bot_cli.py`** – a function that mimics the `-bot` branch.
3. **Modify `bookclub`** (the Bash script) to call `python3 -m src.cli.sync_cli` instead of invoking `sync_books.py` directly.
4. **Modify `bookclub.pi`** similarly.
5. **Test** that `./bookclub -sync`, `./bookclub -chat`, `./bookclub.pi -sync`, `./bookclub.pi -bot` all still work.

### Phase 5: Add Enhancements (Days 9–10)
**Now that the structure is solid**, we can add improvements:

1. **Configuration validation** – in `src/utils/config.py`, add a `validate_config()` that checks for required env vars and prints helpful messages.
2. **Automatic backups** – extend `src/data/storage.py` to create timestamped backups of `reading_log.md` before each sync.
3. **Health checks** – add a `src/cli/health.py` that verifies file permissions, API reachability, etc.
4. **Enhanced logging** – use `src/utils/logging.py` to give both sync and bot consistent, rotating log files.

### Phase 6: Testing & Final Validation (Day 11)
**Goal**: Ensure everything works on both PC and Raspberry Pi.

1. **Write a few key unit tests** (using `pytest`):
   ```bash
   pip install pytest
   pytest tests/ -xvs
   ```
2. **Test on Raspberry Pi** (or simulate with Docker):
   ```bash
   ./bookclub.pi -sync
   ./bookclub.pi -bot
   ```
3. **Verify backward compatibility** – all existing commands, environment variables, and file formats must remain unchanged.
4. **Document the new structure** in `README.md` and add a “For Developers” section.

## 🧪 Testing Strategy – What to Validate at Each Phase

| Phase | What to test | Command |
|-------|--------------|---------|
| 0 | `bookclub.pi` executes | `./bookclub.pi -h` |
| 1 | New sync produces identical output | `diff reading_log.md reading_log.md.backup` |
| 2 | Data layer reads/writes correctly | `python -c "from src.data import storage; storage.read_reading_log()"` |
| 3 | Refactored bot starts and responds | `python scripts/telegram_bot_refactored.py` (with test token) |
| 4 | Launcher scripts still work | `./bookclub -sync && ./bookclub.pi -sync` |
| 5 | Enhancements don’t break anything | Run full suite of existing commands |
| 6 | Everything works on Pi | (actual Pi test) |

## 🔧 Configuration & Environment

No changes to environment variable names are required. The existing `.env` file will keep working.

We will add an **optional** `LOG_LEVEL` variable and a `BACKUP_DIR` variable for phase 5.

## 📈 Benefits of the New Structure

1. **Separation of concerns** – Sync, bot, data, and CLI are isolated.
2. **Testability** – Each module can be unit‑tested in isolation.
3. **Maintainability** – Files are small (≈100‑200 lines) and focused.
4. **Reusability** – The sync module could be used by a future Discord bot or web dashboard.
5. **On‑boarding** – New contributors can understand the codebase quickly.

## 🚨 Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Breaking the working sync | Keep the original `sync_books.py` until the new module passes the diff test. |
| Breaking the Telegram bot | Run the refactored bot in parallel with a test token before switching. |
| Raspberry Pi compatibility | Test `bookclub.pi` after each phase; keep its dependencies minimal. |
| Loss of data | Always create backups before replacing any core script. |

## 🚀 Immediate First Steps (Tomorrow)

1. **Fix permissions** on `bookclub.pi`:
   ```bash
   chmod +x bookclub.pi
   ```
2. **Create the missing directories**:
   ```bash
   mkdir -p src/{cli,bot/commands,bot/middleware} config/prompts tests/{test_sync,test_bot,test_utils}
   ```
3. **Back up the current scripts**:
   ```bash
   cp sync_books.py sync_books.py.backup
   cp telegram_bot.py telegram_bot.py.backup
   ```
4. **Start Phase 1** by creating `src/sync/fetch.py` and moving the Goodreads API logic there.

## 📞 Support During Migration

- If something breaks, revert to the backup copies (`*.backup`).
- Test after **every single file change**.
- Use `git diff` to see exactly what you’re modifying.
- Keep this `MIGRATION.md` file open and check off completed steps.

---
*Last updated: 2026‑02‑12*
*Status: Ready for implementation – start with Phase 0*
