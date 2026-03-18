"""Tests for book2notion.notion_client module."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from book2notion.notion_client import NotionAPIError, NotionClient
from book2notion.parser import BookData, Highlight


@pytest.fixture()
def client() -> NotionClient:
    return NotionClient(token="test-token", data_source_id="test-db-id")


@pytest.fixture()
def book() -> BookData:
    return BookData(
        title="Test Book",
        author="Test Author",
        highlights=[
            Highlight(text="highlight 1", page=1),
            Highlight(text="highlight 2", page=2),
        ],
    )


class TestCreatePage:
    """Tests for NotionClient.create_page."""

    @patch("book2notion.notion_client.requests.post")
    def test_success(self, mock_post: MagicMock, client: NotionClient) -> None:
        mock_post.return_value = MagicMock(
            status_code=200,
            json=MagicMock(return_value={"id": "page-id"}),
        )
        highlight = Highlight(text="test", page=1)
        book = BookData(title="T", author="A", highlights=[highlight])

        result = client.create_page(highlight, book)
        assert result == {"id": "page-id"}
        mock_post.assert_called_once()

    @patch("book2notion.notion_client.requests.post")
    def test_client_error_raises(
        self, mock_post: MagicMock, client: NotionClient
    ) -> None:
        mock_post.return_value = MagicMock(
            status_code=401,
            text='{"message": "Unauthorized"}',
        )
        highlight = Highlight(text="test", page=1)
        book = BookData(title="T", author="A", highlights=[highlight])

        with pytest.raises(NotionAPIError, match="401"):
            client.create_page(highlight, book)

    @patch("book2notion.notion_client.time.sleep")
    @patch("book2notion.notion_client.requests.post")
    def test_rate_limit_retries(
        self, mock_post: MagicMock, mock_sleep: MagicMock, client: NotionClient
    ) -> None:
        rate_limited = MagicMock(
            status_code=429,
            headers={"Retry-After": "0.1"},
            text="rate limited",
        )
        success = MagicMock(
            status_code=200,
            json=MagicMock(return_value={"id": "page-id"}),
        )
        mock_post.side_effect = [rate_limited, success]

        highlight = Highlight(text="test", page=1)
        book = BookData(title="T", author="A", highlights=[highlight])

        result = client.create_page(highlight, book)
        assert result == {"id": "page-id"}
        assert mock_post.call_count == 2
        mock_sleep.assert_called_once_with(0.1)

    @patch("book2notion.notion_client.time.sleep")
    @patch("book2notion.notion_client.requests.post")
    def test_server_error_retries_then_fails(
        self, mock_post: MagicMock, mock_sleep: MagicMock, client: NotionClient
    ) -> None:
        error_response = MagicMock(
            status_code=500,
            text="Internal Server Error",
        )
        mock_post.return_value = error_response

        highlight = Highlight(text="test", page=1)
        book = BookData(title="T", author="A", highlights=[highlight])

        with pytest.raises(NotionAPIError, match="500"):
            client.create_page(highlight, book)
        assert mock_post.call_count == 3


class TestUploadHighlights:
    """Tests for NotionClient.upload_highlights."""

    @patch("book2notion.notion_client.requests.post")
    def test_upload_all_success(
        self, mock_post: MagicMock, client: NotionClient, book: BookData
    ) -> None:
        mock_post.return_value = MagicMock(
            status_code=200,
            json=MagicMock(return_value={"id": "p"}),
        )

        progress_calls: list[tuple[int, int]] = []
        success, failure = client.upload_highlights(
            book, on_progress=lambda c, t: progress_calls.append((c, t))
        )

        assert success == 2
        assert failure == 0
        assert progress_calls == [(1, 2), (2, 2)]

    @patch("book2notion.notion_client.requests.post")
    def test_upload_with_failures(
        self, mock_post: MagicMock, client: NotionClient, book: BookData
    ) -> None:
        mock_post.return_value = MagicMock(
            status_code=401,
            text="Unauthorized",
        )

        success, failure = client.upload_highlights(book)
        assert success == 0
        assert failure == 2
