"""Notion API client for creating highlight pages."""

from __future__ import annotations

import time
from typing import Any, Callable

import requests

from book2notion.parser import BookData, Highlight

NOTION_API_URL = "https://api.notion.com/v1/pages"
NOTION_API_VERSION = "2026-03-11"
MAX_RETRIES = 3
INITIAL_BACKOFF = 1.0  # seconds


class NotionAPIError(Exception):
    """Raised when the Notion API returns an error after exhausting retries."""


class NotionClient:
    """Client for the Notion API."""

    def __init__(self, token: str, data_source_id: str) -> None:
        self._data_source_id = data_source_id
        self._headers = {
            "Accept": "application/json",
            "Notion-Version": NOTION_API_VERSION,
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

    def _build_payload(self, highlight: Highlight, book: BookData) -> dict[str, Any]:
        return {
            "parent": {
                "type": "data_source_id",
                "data_source_id": self._data_source_id,
            },
            "properties": {
                "Highlight": {
                    "title": [{"text": {"content": highlight.text}}],
                },
                "Page": {"number": highlight.page},
                "BookTitle": {
                    "select": {"name": book.title, "color": "default"},
                },
                "Author": {
                    "select": {"name": book.author, "color": "default"},
                },
            },
        }

    def create_page(self, highlight: Highlight, book: BookData) -> dict[str, Any]:
        """Create a single Notion page for a highlight.

        Retries up to ``MAX_RETRIES`` times with exponential backoff on
        transient errors (429 rate-limit and 5xx server errors).

        Raises:
            NotionAPIError: If the request fails after all retries.
        """
        payload = self._build_payload(highlight, book)
        backoff = INITIAL_BACKOFF
        last_exception: Exception | None = None

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = requests.post(
                    NOTION_API_URL,
                    json=payload,
                    headers=self._headers,
                    timeout=30,
                )
            except requests.RequestException as exc:
                last_exception = exc
                if attempt < MAX_RETRIES:
                    time.sleep(backoff)
                    backoff *= 2
                    continue
                break

            if response.status_code == 200:
                return response.json()  # type: ignore[no-any-return]

            # Rate-limited — honour Retry-After header
            if response.status_code == 429:
                header_value = response.headers.get("Retry-After")
                retry_after = backoff
                if header_value is not None:
                    try:
                        retry_after = float(header_value)
                    except ValueError:
                        # Non-numeric Retry-After (e.g. HTTP-date); fall back to current backoff
                        pass
                if attempt < MAX_RETRIES:
                    time.sleep(retry_after)
                    backoff *= 2
                    continue
                break

            # Server error — retry with backoff
            if response.status_code >= 500 and attempt < MAX_RETRIES:
                time.sleep(backoff)
                backoff *= 2
                continue

            # Client error (4xx except 429) or final server error — don't retry
            break

        if last_exception is not None:
            raise NotionAPIError(
                f"Request to Notion API failed after {MAX_RETRIES} attempts: {last_exception}"
            ) from last_exception

        raise NotionAPIError(
            f"Notion API error {response.status_code}: {response.text}"
        )

    def upload_highlights(
        self,
        book: BookData,
        on_progress: Callable[[int, int], None] | None = None,
    ) -> tuple[int, int]:
        """Upload all highlights for a book to Notion.

        Args:
            book: Parsed book data containing highlights.
            on_progress: Optional callback ``(current, total)`` called after
                each highlight is processed.

        Returns:
            Tuple of ``(success_count, failure_count)``.
        """
        total = len(book.highlights)
        success = 0
        failure = 0

        for i, highlight in enumerate(book.highlights, start=1):
            try:
                self.create_page(highlight, book)
                success += 1
            except NotionAPIError:
                failure += 1

            if on_progress is not None:
                on_progress(i, total)

        return success, failure
