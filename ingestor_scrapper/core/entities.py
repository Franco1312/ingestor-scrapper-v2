"""
Domain entities - Framework-agnostic models.

This module contains the core domain models used throughout the application.
These are simple data structures without business logic.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Item:
    """
    Represents a scraped item from a webpage.

    This is a minimal entity that can be extended with additional fields
    as the project grows.

    Attributes:
        title: Title extracted from the page
        content: Main content/text extracted from the page
        url: Source URL of the item
    """

    title: str
    content: Optional[str] = None
    url: Optional[str] = None


@dataclass
class Page:
    """
    Represents a webpage with its raw content.

    This entity encapsulates the HTML content and metadata of a page.

    Attributes:
        url: URL of the page
        html: Raw HTML content
        status_code: HTTP status code (if available)
    """

    url: str
    html: str
    status_code: Optional[int] = None
