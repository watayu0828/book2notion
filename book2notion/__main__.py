"""Entry point for ``python -m book2notion``."""

from __future__ import annotations

import sys

from book2notion.config import Config, ConfigError
from book2notion.gui import select_file, show_error, show_result
from book2notion.notion_client import NotionClient
from book2notion.parser import ParseError, parse


def main() -> int:
    """Run the Book2Notion import workflow.

    Returns:
        Exit code: 0 on success, 1 on error.
    """
    # Load configuration
    try:
        config = Config.load()
    except ConfigError as e:
        show_error(str(e))
        return 1

    # Select file
    filepath = select_file()
    if filepath is None:
        return 0  # User cancelled

    # Read file
    try:
        with open(filepath, encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        show_error(f"File not found: {filepath}")
        return 1
    except (PermissionError, OSError) as e:
        show_error(f"Cannot read file: {e}")
        return 1

    # Parse highlights
    try:
        book = parse(html_content)
    except ParseError as e:
        show_error(f"Failed to parse Kindle HTML:\n{e}")
        return 1

    if not book.highlights:
        show_error("No highlights found in the selected file.")
        return 1

    # Upload to Notion
    client = NotionClient(token=config.token, data_source_id=config.data_source_id)
    success, failure = client.upload_highlights(book)

    total = len(book.highlights)
    show_result(success, failure, total)

    return 1 if failure > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
