"""
Scrapy adapter for HtmlFetcher port.

This adapter implements the HtmlFetcher interface using Scrapy's
Request/Response mechanism. It bridges Scrapy's framework with our
domain layer.
"""

from scrapy.http import Response

from ingestor_scrapper.core.entities import Page
from ingestor_scrapper.core.ports import HtmlFetcher


class AdapterScrapyFetcher(HtmlFetcher):
    """
    Adapter that implements HtmlFetcher using Scrapy's Response object.

    This adapter is typically instantiated within a Scrapy spider's
    parse method, where the Response object is available.

    Usage in a spider:
        response = scrapy.Request(...)  # from spider
        fetcher = AdapterScrapyFetcher(response)
        page = fetcher.fetch(url)  # Uses the response's HTML
    """

    def __init__(self, response: Response):
        """
        Initialize the fetcher with a Scrapy Response.

        Args:
            response: Scrapy Response object containing the HTML
        """
        self.response = response

    def fetch(self, url: str) -> Page:
        """
        Extract HTML from the Scrapy Response and create a Page entity.

        Note: The url parameter is kept for interface consistency,
        but in practice we use self.response.url.

        Args:
            url: URL string (usually same as response.url)

        Returns:
            Page: Page entity with URL and HTML content
        """
        # Use the response's URL and HTML content
        return Page(
            url=self.response.url,
            html=self.response.text,
            status_code=self.response.status,
        )
