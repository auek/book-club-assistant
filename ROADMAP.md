# 🗺️ Roadmap Backlog

### 📖 Active Stories (S-L)

#### Story 1: Auto-Backups [S]
- [x] **Auto-Backups**: Extend `storage.py` to create timestamped backups of `reading_log.md` before overwriting.

#### Story 5: Garmin Connect Integration (Health & Workouts) [M]
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

#### Story 6: Discord Frontend Integration [L]
- [ ] **Discord Bot Implementation**: Create a parallel frontend to the Telegram bot using `discord.py`.
    - **Goal**: Provide a desktop/mobile alternative that functions as a cost-effective personal assistant.
    - [ ] Implement `src/bot/discord_core.py` to handle Discord events.
    - [ ] Port existing commands (/books, /progress, /discuss) to Discord Slash Commands.
    - [ ] **Security**: Implement strict User ID whitelisting to ensure only the owner can interact with the bot.
    - [ ] **Economy**: Leverage the existing `src/utils/llm.py` with prompt caching to maintain low API costs compared to flat-rate subscriptions.

#### Story 7: Technical Excellence [M]
- [ ] **Centralized Config**: Migrate all hardcoded file paths and shared constants to `src/utils/config.py`.
- [ ] **Async Storage**: Refactor `src/data/storage.py` to use `aiofiles` for non-blocking I/O.
- [ ] **Duplicate Detection**: Implement logic in `src/sync/parse.py` to prevent duplicate entries if the RSS feed overlaps.

#### Story 10: Multi-language Support (i18n) [M]
- [ ] **Internationalization**: Decouple Swedish strings from the source code to support English (EN) and other languages.
    - [ ] **String Externalization**: Move hardcoded Swedish UI strings from `src/bot/`, `src/sync/render.py`, and `src/utils/llm.py` into language files (e.g., `locales/sv.json`, `locales/en.json`).
    - [ ] **User Toggle**: Implement a `/lang` command (e.g., `/lang en`) that saves the preference to `context.user_data` or a local config.
    - [ ] **Dynamic AI Context**: Update the system prompt in `src/utils/llm.py` to instruct the AI to respond in the user's chosen language.

---

### 🔮 Future Evolution (Major Shifts & XL Features)

#### Feature 1: SQLite Integration [XL]
- **Goal**: Move from Markdown-parsing to a database as the "source of truth".
- [ ] `src/data/database.py` for SQLite management.
- [ ] Update Sync logic to save to DB first, then export to Markdown.
- [ ] Security considerations for local DB access is of utmost importance.

#### Feature 2: Transition to "Personal Assistant" Architecture [XL]
- **Analysis**: Evaluate if Garmin and Notion features belong in the "Bookclub" or if the project should be forked/renamed to a "Personal Assistant" framework.
- [ ] **Task 2.1: Modular Context Providers**: Refactor `src/utils/llm.py` to accept dynamic context blocks instead of hardcoded file reads.
- [ ] **Task 2.2: Plugin Registry**: Create a system to dynamically register modules (Books, Garmin, Notion) and their respective bot commands.
- [ ] **Task 2.3: Data Migration (SQLite)**: Implement a centralized database to serve as the primary source of truth for the assistant.
- [x] **Head Start**: Use the existing Telegram/LLM integration as the foundation for the new project.

---
*See [ARCHIVE.md](ARCHIVE.md) for completed tasks and historical milestones.*
