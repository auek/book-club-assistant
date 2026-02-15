# Project Specifics: Bookclub-Bot

## 🎯 Boy Scout Principles
1. **Code Review:** Analyze current Bash scripts and Python logic to identify weaknesses or redundancy.
2. **Robustness:** Propose and implement better error handling (e.g., what happens if a file is missing or an API key is incorrect?).
3. **Documentation:** Ensure the code is self-explanatory and well-document.

## Forbidden Practices
- NEVER run the bot inside the agentic session in any form or way (Note: This does not apply to running automated tests via pytest). This includes but is not limited to:
    - `./bookclub -bot`
    - `./bookclub.pi -bot`
    - `python3 -m src.cli.bot_cli`
  Running the bot in the same terminal session as development leads to confusion, log pollution, and potential security risks.

## 🛠 Technical Standards
- **Token Efficiency:** Bot responses and prompts should be structured to minimize token usage while maintaining a helpful Swedish persona.
- **Roadmap Maintenance:** After every code change, check `ROADMAP.md` and update it accordingly if needed to reflect the current project status.
- **Archive Policy:** Completed stories must be moved from `ROADMAP.md` to `ARCHIVE.md` ONLY after they are verified and tested. Each archived entry must include a completion date in `[YYYY-MM-DD]` format.
- **Readme Updates:** If a code change affects user-facing functionality (e.g., bot commands, setup instructions), update `README.md` to reflect these changes.

## 🧪 Testing Standards
- **Unit Testing**: New logic in `src/` should be accompanied by unit tests in the `tests/` directory.
- **Regression**: Ensure that changes to formatters or data parsing do not break existing Markdown output formats.
- **Environment**: Tests should not require active API keys; use mocking for network calls (Goodreads/OpenRouter).
- **Execution**: Run tests using `pytest` before committing major changes.

## Language
All code, comments, and documentation should be in English to maintain consistency and accessibility for potential future collaborators. However, user-facing strings in the Telegram bot can remain in Swedish as per the current design, but should be externalized for future internationalization efforts.
The endpoints for the bot /sync, /books, /progress, /info and /help should also remain in English for consistency with the codebase, but the bot's responses (including plain text discussions) will always be in swedish.


