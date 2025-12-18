"""
Article content extraction service.
"""

from typing import Dict, Optional

from newspaper import Article as NewspaperArticle

from ..core.logging import get_logger

logger = get_logger(__name__)


class ArticleExtractorService:
    """Service for extracting article content from URLs."""

    def extract(self, url: str) -> Optional[Dict[str, str]]:
        """Extract article content from URL.

        Args:
            url: Article URL

        Returns:
            Dictionary with extracted article data or None if extraction fails
        """
        try:
            article = NewspaperArticle(url)
            article.download()
            article.parse()

            return {
                "title": article.title or "",
                "content": article.text or "",
                "summary": article.summary or "",
                "authors": article.authors or [],
                "published_date": (
                    article.publish_date.isoformat() if article.publish_date else None
                ),
                "images": article.images or [],
                "keywords": article.keywords or [],
            }
        except Exception as e:
            logger.error(f"Failed to extract article from {url}: {str(e)}")
            return None
