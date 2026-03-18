"""Kindle HTML highlight parser with multi-language support."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

import bs4


class ParseError(Exception):
    """Raised when Kindle HTML parsing fails."""


@dataclass
class Highlight:
    """A single Kindle highlight."""

    text: str
    page: int


@dataclass
class BookData:
    """Parsed book metadata and highlights."""

    title: str
    author: str
    highlights: list[Highlight] = field(default_factory=list)


# Page-number extraction patterns per locale.
# Each pattern must have exactly one capture group for the page number.
PAGE_PATTERNS: dict[str, re.Pattern[str]] = {
    "ja": re.compile(r"\sページ(.+?)\s·位置\d+"),
    "en": re.compile(r"\s[Pp]age\s(\d+)\s·\s[Ll]ocation\s\d+"),
}


def _detect_locale(note_headings: list[bs4.element.Tag]) -> str:
    """Auto-detect Kindle export locale from noteHeading text.

    Falls back to ``"ja"`` if detection is inconclusive.
    """
    for heading in note_headings:
        text = heading.get_text()
        if "Page" in text or "Location" in text:
            return "en"
        if "ページ" in text or "位置" in text:
            return "ja"
    return "ja"


def parse(html_content: str) -> BookData:
    """Parse Kindle export HTML and return structured book data.

    Args:
        html_content: Raw HTML string exported from the Kindle app.

    Returns:
        BookData with title, author, and list of highlights.

    Raises:
        ParseError: If required elements are missing from the HTML.
    """
    soup = bs4.BeautifulSoup(html_content, "html.parser")

    # Title
    title_div = soup.find("div", class_="bookTitle")
    if not title_div:
        raise ParseError("Could not find book title (.bookTitle) in the HTML.")
    book_title = title_div.get_text(strip=True)

    # Author
    author_div = soup.find("div", class_="authors")
    if not author_div:
        raise ParseError("Could not find author (.authors) in the HTML.")
    author = author_div.get_text(strip=True)

    # Highlights
    note_headings = soup.find_all("div", class_="noteHeading")
    note_texts = soup.find_all("div", class_="noteText")

    if len(note_headings) != len(note_texts):
        raise ParseError(
            f"Mismatch between noteHeading ({len(note_headings)}) "
            f"and noteText ({len(note_texts)}) counts."
        )

    locale = _detect_locale(note_headings)
    pattern = PAGE_PATTERNS.get(locale)
    if pattern is None:
        raise ParseError(f"Unsupported locale: {locale}")

    highlights: list[Highlight] = []
    for heading, text_div in zip(note_headings, note_texts):
        match = pattern.search(heading.get_text())
        if not match:
            continue

        page_str = match.group(1).strip()
        try:
            page = int(page_str)
        except ValueError:
            continue

        text = text_div.get_text(strip=True)
        if text:
            highlights.append(Highlight(text=text, page=page))

    return BookData(title=book_title, author=author, highlights=highlights)
