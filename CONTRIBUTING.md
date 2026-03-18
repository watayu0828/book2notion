# Contributing to Book2Notion

Thank you for your interest in contributing! This guide will help you get started.

## Development Setup

### Prerequisites

- Python 3.10+
- Git

### Getting started

```bash
git clone https://github.com/watayu0828/book2notion.git
cd book2notion
pip install -r requirements-dev.txt
```

### Running the tool

```bash
python -m book2notion
```

### Running tests

```bash
pytest --cov=book2notion --cov-report=term-missing
```

### Linting and formatting

```bash
ruff check .
ruff format .
```

### Type checking

```bash
mypy book2notion/
```

## Project Structure

```text
book2notion/          # Package directory
├── __init__.py       # Version
├── __main__.py       # Entry point (python -m book2notion)
├── config.py         # Environment variable loading
├── parser.py         # Kindle HTML parser
├── notion_client.py  # Notion API client
└── gui.py            # Tkinter UI helpers
tests/
├── fixtures/         # Sample Kindle HTML files for testing
├── test_parser.py
├── test_notion_client.py
└── test_config.py
```

## Adding Support for a New Language

The Kindle parser uses locale-specific regex patterns to extract page numbers. To add a new language:

1. Open `book2notion/parser.py`.
2. Add a new entry to the `PAGE_PATTERNS` dictionary with a regex pattern that captures the page number.
3. Update `_detect_locale()` to recognize the new language based on text in the `noteHeading` elements.
4. Add a test fixture in `tests/fixtures/` and corresponding tests in `tests/test_parser.py`.

## Pull Request Process

1. Fork the repository and create a feature branch.
2. Make your changes and ensure all checks pass:
   - `ruff check .` — no lint errors
   - `ruff format --check .` — code is formatted
   - `mypy book2notion/` — no type errors
   - `pytest` — all tests pass
3. Open a pull request with a clear description of your changes.

## Code of Conduct

Be respectful and constructive. We are all here to build something useful together.
