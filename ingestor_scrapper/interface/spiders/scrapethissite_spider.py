"""
ScrapeThisSite spider - Scrapes pages from scrapethissite.com.

This spider demonstrates the Clean Architecture layers:
1. Uses ScrapeThisSiteUseCase from application layer
2. Injects adapters (Scrapy fetcher, ScrapeThisSite parser, stdout output)
3. Executes the use case to crawl and parse scrapethissite.com

Run with: scrapy crawl scrapethissite
"""

import logging

import scrapy

from ingestor_scrapper.adapters.fetcher_scrapy import AdapterScrapyFetcher
from ingestor_scrapper.adapters.output_stdout import AdapterStdoutOutput
from ingestor_scrapper.adapters.parser_scrapethissite import (
    AdapterScrapeThisSiteParser,
)
from ingestor_scrapper.application.scrape_this_site_use_case import (
    ScrapeThisSiteUseCase,
)

logger = logging.getLogger(__name__)


class ScrapeThisSiteSpider(scrapy.Spider):
    """
    Spider that crawls scrapethissite.com and extracts session links.

    This spider demonstrates the Clean Architecture pattern:
    - Spider (interface layer) orchestrates the use case
    - Use case (application layer) coordinates the ports
    - Adapters (adapters layer) implement the ports with specific frameworks
    """

    name = "scrapethissite"
    allowed_domains = ["scrapethissite.com"]
    start_urls = ["https://www.scrapethissite.com/pages/"]

    def __init__(self, *args, **kwargs):
        """
        Initialize the spider.

        Note: Spiders are instantiated by Scrapy, so we can't easily
        inject dependencies here. Instead, we instantiate adapters in parse().

        TODO: Consider using spider middleware or custom spider loader
        for better dependency injection.
        """
        super().__init__(*args, **kwargs)

    def parse(self, response):
        """
        Parse the response using Clean Architecture layers.

        This method:
        1. Creates adapters (fetcher, parser, output)
        2. Creates and executes the use case
        3. Logs the results

        Args:
            response: Scrapy Response object
        """
        # Step 1: Create adapters (wire dependencies)
        fetcher = AdapterScrapyFetcher(response)
        parser = (
            AdapterScrapeThisSiteParser()
        )  # Parser específico para scrapethissite
        output = AdapterStdoutOutput()

        # Step 2: Create use case and inject dependencies
        use_case = ScrapeThisSiteUseCase(
            fetcher=fetcher, parser=parser, output=output
        )

        # Step 3: Execute the use case
        # Note: The fetcher already has the response, so we pass the URL
        # for consistency with the interface
        try:
            items = use_case.execute(response.url)

            # Log the result for Scrapy output
            logger.info("Successfully parsed %s", response.url)
            title = items[0].title if items else "N/A"
            logger.info("Extracted title: %s", title)

        except Exception as e:
            logger.error(
                "Error processing %s: %s", response.url, e, exc_info=True
            )
