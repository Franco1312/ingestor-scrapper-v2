"""
Parser adapter for ScrapeThisSite.com pages.

This parser is specific to the structure of scrapethissite.com
and extracts session links with their descriptions.
"""

import logging
from typing import List
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from ingestor_scrapper.core.entities import Item
from ingestor_scrapper.core.ports import Parser

logger = logging.getLogger(__name__)


class AdapterScrapeThisSiteParser(Parser):
    """
    Parser adapter specifically for scrapethissite.com structure.

    This parser extracts:
    - Links that start with /pages/
    - Descriptions from <p class="lead session-desc"> tags
    """

    def __init__(self, parser: str = "html.parser"):
        """
        Initialize the parser.

        Args:
            parser: Parser type to use ('html.parser', 'lxml', 'html5lib')
        """
        self.parser = parser

    def parse(self, html: str, url: str) -> List[Item]:
        """
        Parse HTML from scrapethissite.com and extract session links.

        Args:
            html: Raw HTML content
            url: Source URL of the HTML

        Returns:
            List[Item]: List of extracted session items

        Raises:
            Exception: If parsing fails
        """
        try:
            soup = BeautifulSoup(html, self.parser)

            # Find all links <a> tags with href attribute
            link_tags = soup.find_all("a", href=True)
            items = []

            for link_tag in link_tags:
                # Extract text and href from each link
                link_text = link_tag.get_text(strip=True)
                link_href = link_tag.get("href", "")

                # Skip empty links
                if not link_text:
                    continue

                # Filter: only include links that start with /pages/
                # This excludes navigation links (/, /lessons/, /faq/, etc.)
                if not link_href.startswith("/pages/"):
                    continue

                # Find the description paragraph (session-desc) near this link
                description = ""
                parent = link_tag.parent
                if parent:
                    # Look for p with class "lead session-desc" in the parent
                    desc_tag = parent.find("p", class_="lead session-desc")
                    if not desc_tag:
                        # Try parent's parent (often the link and desc are in a div)
                        grandparent = parent.parent if parent else None
                        if grandparent:
                            desc_tag = grandparent.find(
                                "p", class_="lead session-desc"
                            )

                    if desc_tag:
                        description = desc_tag.get_text(strip=True)

                # Build full URL if href is relative
                full_url = url
                if link_href.startswith("/"):
                    full_url = urljoin(url, link_href)
                elif link_href.startswith("http"):
                    full_url = link_href

                # Create item for each link with description
                items.append(
                    Item(
                        title=link_text,
                        content=description or link_href,
                        url=full_url,
                    )
                )

            logger.info("Extracted %d items from %s", len(items), url)

            # If no links found, return at least one item with page title
            if not items:
                h1_tag = soup.find("h1")
                h1_content = (
                    h1_tag.get_text(strip=True) if h1_tag else "No links found"
                )
                items.append(
                    Item(
                        title=h1_content,
                        content="",
                        url=url,
                    )
                )

            return items

        except Exception as e:
            # Return minimal item if parsing fails
            return [
                Item(
                    title="Parsing error",
                    content=f"Failed to parse HTML: {str(e)}",
                    url=url,
                )
            ]
