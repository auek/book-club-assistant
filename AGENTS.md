# Project Specifics: Bookclub-Bot

## 🎯 Short-term Goals (Analysis Phase)
1. **Code Review:** Analyze current Bash scripts and Python logic to identify weaknesses or redundancy.
2. **Robustness:** Propose and implement better error handling (e.g., what happens if a file is missing or an API key is incorrect?).
4. **Documentation:** Ensure the code is self-explanatory and well-document.

## 🛠 Technical Standards
- **Roadmap Maintenance:** After every code change, check `ROADMAP.md` and update it accordingly if needed to reflect the current project status.
- **Archive Policy:** Completed stories must be moved from `ROADMAP.md` to `ARCHIVE.md` ONLY after they are verified and tested. Each archived entry must include a completion date in `[YYYY-MM-DD]` format.

## 🧪 Testing Standards
- **Unit Testing**: New logic in `src/` should be accompanied by unit tests in the `tests/` directory.
- **Regression**: Ensure that changes to formatters or data parsing do not break existing Markdown output formats.
- **Environment**: Tests should not require active API keys; use mocking for network calls (Goodreads/OpenRouter).
- **Execution**: Run tests using `pytest` before committing major changes.

## Language
Everything regarding code and development is done in ENGLISH. However, all copy that reaches the user must be in SWEDISH.

