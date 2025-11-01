"""
BCRA Use Case - Use case for scraping BCRA pages.

This use case handles the specific logic for scraping pages from
www.bcra.gob.ar, following Clean Architecture principles.
"""

import logging
from typing import List

from ingestor_scrapper.application.use_cases import UseCase
from ingestor_scrapper.core.entities import Item, Page
from ingestor_scrapper.core.ports import HtmlFetcher, OutputPort, Parser

logger = logging.getLogger(__name__)


class BcraUseCase(UseCase):  # pylint: disable=too-few-public-methods
    """
    Use case for crawling BCRA URLs and parsing their content.

    Parses BCRA pages into structured items.

    This use case:
    1. Fetches HTML content from a URL using HtmlFetcher
    2. Parses the HTML into Items using Parser
    3. Outputs the results using OutputPort

    The use case is decoupled from specific implementations through dependency
    injection of the ports (interfaces).
    """

    def __init__(
        self, fetcher: HtmlFetcher, parser: Parser, output: OutputPort
    ):
        """
        Initialize the use case with its dependencies.

        Args:
            fetcher: Implementation of HtmlFetcher port
            parser: Implementation of Parser port
            output: Implementation of OutputPort
        """
        self.fetcher = fetcher
        self.parser = parser
        self.output = output

    def execute(self, url: str) -> List[Item]:
        """
        Execute the crawl and parse workflow for BCRA pages.

        Args:
            url: URL to crawl and parse

        Returns:
            List[Item]: List of extracted items

        Best practices:
        - Validate inputs early
        - Check for empty results
        - Clear logging at each step
        """
        # Step 1: Fetch HTML content
        # Best practice: Validate input URL
        if not url or not url.strip():
            logger.warning("Empty URL provided to use case")
            return []

        try:
            page: Page = self.fetcher.fetch(url)
        except Exception as e:
            logger.error("Failed to fetch URL %s: %s", url, e)
            return []

        # Step 2: Validate fetched content
        if not page.html or not page.html.strip():
            logger.warning("Empty HTML content fetched from %s", url)
            return []

        # Step 3: Parse HTML into structured items
        try:
            items: List[Item] = self.parser.parse(page.html, page.url)
        except Exception as e:
            logger.error("Failed to parse HTML from %s: %s", url, e)
            return []

        # Step 4: Validate parsing results
        if not items:
            logger.warning("No items extracted from %s", url)
            return []

        # Step 5: Output the results
        try:
            self.output.emit(items)
        except Exception as e:
            logger.error("Failed to output items: %s", e)

        return items
