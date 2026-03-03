# 🗺️ Roadmap

### 📖 Active Stories (S-M)

#### Story: UX Polish (Inline Keyboards) [S]
- [ ] **Inline Keyboards**: Replace `/yes` and `/no` commands with Telegram Inline Keyboards for a native app feel.

#### Story: Search & Retrieval [M]
- [ ] **Search Command**: Implement `/search <query>` to allow querying the `reading_log.md` using the LLM.

#### Story: Natural Language Progress Updates [M]
- [ ] **Intent Interception**: Refactor `discuss_books` to intercept progress updates (e.g., "I'm 50% done") and trigger `update_progress_file`.

#### Story: Technical Excellence [M]
- [ ] **Centralized Config**: Migrate all hardcoded file paths to `src/utils/config.py`.
- [ ] **Async Storage**: Refactor `src/data/storage.py` to use `aiofiles` for non-blocking I/O.

---

### 🔮 Future Evolution (L-XL)

#### Feature: Modular Assistant Architecture
- [ ] **SQLite Migration**: Move from flat files to SQLite for better data integrity and querying.
- [ ] **Plugin Registry**: Refactor `src/utils/llm.py` to accept a registry of context blocks (Books, Garmin, Notion).
- [ ] **Multi-Client Adapter**: Decouple bot logic to support Discord or CLI interfaces alongside Telegram.

#### Feature: New Domains
- [ ] **Garmin Connect Integration**: Fetch fitness data with strict privacy stripping and medical disclaimers.
- [ ] **Notion Workspace Integration**: Allow AI to search and append notes to Notion databases.
- [ ] **Internationalization (i18n)**: Move hardcoded Swedish strings to localizable files.

---
*See [ARCHIVE.md](ARCHIVE.md) for completed tasks and historical milestones.*
