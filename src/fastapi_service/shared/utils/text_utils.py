"""
Text utility functions.
"""

import re
from typing import List


def clean_text(text: str) -> str:
    """Clean text by removing extra whitespace and newlines.

    Args:
        text: Text to clean

    Returns:
        Cleaned text
    """
    if not text:
        return ""

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text)
    # Remove leading/trailing whitespace
    text = text.strip()
    return text


def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """Extract keywords from text (simple implementation).

    Args:
        text: Text to extract keywords from
        max_keywords: Maximum number of keywords to return

    Returns:
        List of keywords
    """
    if not text:
        return []

    # Simple keyword extraction (can be enhanced with NLP)
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
    # Count word frequency
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1

    # Sort by frequency and return top keywords
    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    return [word for word, _ in sorted_words[:max_keywords]]


def truncate_text(text: str, max_length: int = 200, suffix: str = "...") -> str:
    """Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated text
    """
    if not text or len(text) <= max_length:
        return text

    return text[: max_length - len(suffix)] + suffix
