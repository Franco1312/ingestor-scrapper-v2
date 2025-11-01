"""
Ports - Interfaces/Protocols for dependencies (Hexagonal Architecture).

This module defines the interfaces that the application layer will use.
Adapters in the adapters/ module will implement these interfaces.

These are abstract contracts that allow the core logic to remain
independent of specific implementations (Scrapy, BeautifulSoup, etc.).
"""

from abc import ABC, abstractmethod
from typing import List

from ingestor_scrapper.core.entities import Item, Page


class HtmlFetcher(ABC):
    """
    Port for fetching HTML content from URLs.

    Implementations:
    - AdapterScrapyFetcher (in adapters/fetcher_scrapy.py) uses Scrapy's Request/Response
    - Could also have AdapterRequestsFetcher, AdapterPlaywrightFetcher, etc.

    Example usage:
        fetcher = AdapterScrapyFetcher()
        page = await fetcher.fetch("https://example.com")
    """

    @abstractmethod
    def fetch(self, url: str) -> Page:
        """
        Fetch HTML content from a URL.

        Args:
            url: The URL to fetch

        Returns:
            Page: A Page entity containing the URL and HTML content

        Raises:
            Exception: If the fetch fails (implementation-specific)
        """
        pass


class Parser(ABC):
    """
    Port for parsing HTML content into structured Items.

    Implementations:
    - AdapterScrapeThisSiteParser (in adapters/parser_scrapethissite.py) uses BeautifulSoup4
    - Could also have AdapterLxmlParser, AdapterSelectolaxParser, etc.

    Example usage:
        parser = AdapterScrapeThisSiteParser()
        items = parser.parse(page.html, page.url)
    """

    @abstractmethod
    def parse(self, html: str, url: str) -> List[Item]:
        """
        Parse HTML content and extract structured data.

        Args:
            html: Raw HTML content
            url: Source URL of the HTML

        Returns:
            List[Item]: List of extracted items

        Raises:
            Exception: If parsing fails (implementation-specific)
        """
        pass


class OutputPort(ABC):
    """
    Port for outputting/emitting scraped items.

    Implementations:
    - AdapterStdoutOutput (in adapters/output_stdout.py) prints/logs items
    - Could also have AdapterFileOutput, AdapterDatabaseOutput, AdapterApiOutput, etc.

    Example usage:
        output = AdapterStdoutOutput()
        output.emit(items)
    """

    @abstractmethod
    def emit(self, items: List[Item]) -> None:
        """
        Emit/output scraped items.

        Args:
            items: List of items to output

        Returns:
            None
        """
        pass
