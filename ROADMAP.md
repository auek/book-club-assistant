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

### 🛠️ DevOps & Infrastructure [M]
*Status: Planned - Improving deployment reliability and developer experience.*

#### Feature: CI/CD Pipeline
- **Story: Automated Testing [S]**: Create a GitHub Actions workflow to run `pytest` on all branches and Pull Requests to ensure `main` remains stable.
- **Story: Branch Protection & Workflow [S]**: Define a branching strategy where features are developed in `feature/*` branches and merged only after passing tests.
- **Story: Self-Hosted Deployment [M]**: Set up a GitHub Actions runner on the Raspberry Pi for automated code updates and bot restarts.
- **Story: Security Scrubbing [S]**: Use `git filter-repo` to permanently remove historical traces of leaked API keys before potentially moving to a Public repository.

### 🔮 Future Evolution: Personal Assistant Architecture [XL]
*Strategic goal: Transform the monolithic Bookclub bot into a multi-purpose Personal Assistant with a plugin-based architecture.*

#### Feature: Modular Orchestration
- **Story: Modular Context Providers [M]**: Refactor `src/utils/llm.py` to accept a registry of context blocks instead of hardcoded file paths.
- **Story: Plugin Registry System [M]**: Implement a way to dynamically register modules (Books, Garmin, Notion) so they can contribute commands and system prompts.
- **Story: Multi-Client Adapter [L]**: (Ref: Story 6) Decouple the bot logic from Telegram to allow Discord or CLI interfaces to share the same LLM "brain".

#### Feature: Centralized Intelligence (SQLite)
- **Story: Database Schema Design [S]**: Create `src/data/database.py` and define tables for books, health metrics, and user preferences.
- **Story: Data Migration & Sync [L]**: Update sync logic to treat SQLite as the "Source of Truth," while keeping Markdown files as human-readable exports.
- **Story: Interaction History Persistence [M]**: Move conversation history from Pickle/RAM to the database for long-term "memory."

#### Feature: New Domains (Plugins)
- **Story: AI Book Recommendations [S]**: Implement a `/recommend` command that uses the LLM to suggest a new book based on the current library, but with a "wildcard" factor to keep suggestions unpredictable and fun.
- **Story: Garmin Connect Integration [M]**: (Ref: Story 5) Fetch fitness data. Includes mandatory privacy stripping and medical disclaimers.
- **Story: Notion Workspace Integration [L]**: (Ref: Story 5) Allow the AI to search and append notes to a specific Notion database.
- **Story: Internationalization (i18n) [M]**: (Ref: Story 10) Move hardcoded Swedish strings to localizable files to allow easy language switching.

---
*See [ARCHIVE.md](ARCHIVE.md) for completed tasks and historical milestones.*
