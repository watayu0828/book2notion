"""Tests for book2notion.parser module."""

from __future__ import annotations

from pathlib import Path

import pytest

from book2notion.parser import Highlight, ParseError, parse

FIXTURES = Path(__file__).parent / "fixtures"


class TestParseJapanese:
    """Tests for Japanese Kindle HTML parsing."""

    def test_parse_title_and_author(self) -> None:
        html = (FIXTURES / "kindle_ja.html").read_text(encoding="utf-8")
        book = parse(html)
        assert book.title == "テスト書籍タイトル"
        assert book.author == "テスト著者"

    def test_parse_highlights(self) -> None:
        html = (FIXTURES / "kindle_ja.html").read_text(encoding="utf-8")
        book = parse(html)
        assert len(book.highlights) == 2
        assert book.highlights[0] == Highlight(
            text="これはテスト用のハイライトです。", page=42
        )
        assert book.highlights[1] == Highlight(
            text="二つ目のハイライトテキストです。", page=100
        )


class TestParseEnglish:
    """Tests for English Kindle HTML parsing."""

    def test_parse_title_and_author(self) -> None:
        html = (FIXTURES / "kindle_en.html").read_text(encoding="utf-8")
        book = parse(html)
        assert book.title == "Test Book Title"
        assert book.author == "Test Author"

    def test_parse_highlights(self) -> None:
        html = (FIXTURES / "kindle_en.html").read_text(encoding="utf-8")
        book = parse(html)
        assert len(book.highlights) == 2
        assert book.highlights[0] == Highlight(
            text="This is a test highlight.", page=42
        )
        assert book.highlights[1] == Highlight(
            text="This is the second highlight.", page=100
        )


class TestParseEdgeCases:
    """Tests for error handling and edge cases."""

    def test_empty_html_raises_parse_error(self) -> None:
        with pytest.raises(ParseError, match="Could not find book title"):
            parse("")

    def test_missing_authors_raises_parse_error(self) -> None:
        html = '<div class="bookTitle">Title</div>'
        with pytest.raises(ParseError, match="Could not find author"):
            parse(html)

    def test_no_highlights_returns_empty_list(self) -> None:
        html = '<div class="bookTitle">Title</div><div class="authors">Author</div>'
        book = parse(html)
        assert book.highlights == []

    def test_mismatched_heading_text_raises_parse_error(self) -> None:
        html = (
            '<div class="bookTitle">T</div>'
            '<div class="authors">A</div>'
            '<div class="noteHeading">heading</div>'
        )
        with pytest.raises(ParseError, match="Mismatch"):
            parse(html)

    def test_heading_without_page_number_is_skipped(self) -> None:
        html = (
            '<div class="bookTitle">T</div>'
            '<div class="authors">A</div>'
            '<div class="noteHeading">no page info here</div>'
            '<div class="noteText">some text</div>'
        )
        book = parse(html)
        assert book.highlights == []
