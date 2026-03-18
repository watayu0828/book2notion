# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.2.0] - 2026-03-19

### Added

- Modular package structure (`book2notion/` package with `parser`, `notion_client`, `config`, `gui` modules).
- English Kindle HTML support with automatic language detection.
- Retry logic with exponential backoff for Notion API calls (handles 429 rate limits and 5xx errors).
- Configuration validation with clear error messages for missing `TOKEN` / `DATA_SOURCE_ID`.
- GUI result dialogs showing success/failure counts.
- Unit tests for parser, Notion client, and config modules.
- GitHub Actions CI pipeline (lint, type-check, test across Python 3.10–3.12).
- English README, CONTRIBUTING.md, CHANGELOG.md.
- GitHub Issue and PR templates.

### Changed

- Refactored from single-script (`book2notion.py`) to modular package.
- Run with `python -m book2notion` instead of `python book2notion.py`.
- Replaced bare `except` with specific exception handling.
- Added type annotations throughout.

### Removed

- PyInstaller build configuration (`Book2Notion.spec`, `build/`, `dist/`).

## [0.1.0] - 2024-01-01

### Added

- Initial release.
- Kindle highlight HTML parsing (Japanese only).
- Notion API integration for creating highlight pages.
- Tkinter file selection dialog.
- PyInstaller executable build.
