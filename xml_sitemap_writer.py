"""
Provides XMLSitemap class used to generate large XML sitemap from iterators
"""
import logging
from typing import List, Iterator


class XMLSitemap:
    """
    Generate large XML sitemaps with a sitemap index and sub-sitemap XML files
    """

    # Sitemap file that you provide must have no more than 50,000 URLs
    # and must be no larger than 10MB (10,485,760 bytes).
    # @see http://www.sitemaps.org/protocol.html#index
    URLS_PER_FILE = 15000

    def __init__(self, path: str):
        """
        Set up XMLSitemap to write to a given path
        """
        self.path = path
        self.logger = logging.getLogger(self.__class__.__name__)

        self._sitemaps = []
        self.sitemaps_counter = 0
        self.current_section_name = ""

        self.total_urls_counter = 0
        self.sitemap_urls_counter = 0

        self.add_section("pages")

    def add_url(self, url: str):
        """
        Add a given URL to the sitemap
        """
        self.total_urls_counter += 1
        self.sitemap_urls_counter += 1

        self.logger.debug(f"Adding URL <{url}>")

    def add_urls(self, urls: Iterator[str]):
        """
        Add URLs for a provided iterable
        """
        for url in urls:
            self.add_url(url)

    def add_section(self, section_name: str):
        """
        Starting a new section will create a new sub-sitemap with
        a filename set to "sitemap-<section_name>-<number>.xml"
        """
        self.current_section_name = section_name
        self._add_sitemap()

    @property
    def sitemaps(self) -> List[str]:
        """
        Returns list of sitemaps
        """
        return self._sitemaps

    def __repr__(self):
        """
        A string representation
        """
        return f"<{self.__class__.__name__} at {self.path} ({len(self)} URLs)>"

    def __len__(self):
        """
        How many URLs are there
        """
        return self.total_urls_counter

    def _add_sitemap(self):
        """
        Called internally to add a new sitemap:

        * when start_section() is called
        * when per-sitemap URLs counter reaches the limit
        """
        self.sitemaps_counter += 1
        sitemap_name = "sitemap-%03d-%s.xml" % (
            self.sitemaps_counter,
            self.current_section_name,
        )

        self._sitemaps.append(sitemap_name)
        self.logger.info(f"New sitemap added: {sitemap_name}")
