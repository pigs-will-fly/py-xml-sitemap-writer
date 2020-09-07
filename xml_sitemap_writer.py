"""
Provides XMLSitemap class used to generate large XML sitemap from iterators
"""
import logging
from typing import List, Iterator
from typing.io import IO  # pylint:disable=import-error

from xml.sax.saxutils import escape as escape_xml


# pylint:disable=too-many-instance-attributes
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
        self.path = path.rstrip("/")
        self.logger = logging.getLogger(self.__class__.__name__)

        self._sitemaps = []
        self.sitemaps_counter = 0
        self.current_section_name = ""

        self.total_urls_counter = 0
        self.sitemap_urls_counter = 0

        # file handler for a current sitemap
        self._sitemap_file = None

        self.add_section("pages")

    def add_url(self, url: str):
        """
        Add a given URL to the sitemap
        """
        self.total_urls_counter += 1
        self.sitemap_urls_counter += 1

        # check per sitemap limits
        if self.sitemap_urls_counter > self.URLS_PER_FILE:
            self.logger.info(
                f"URLs per sitemap counter reached the limit of {self.URLS_PER_FILE}"
            )
            self._add_sitemap()
            self.sitemap_urls_counter = 1

        self.logger.debug(f"Adding URL <{url}>")
        self.write_to_sitemap(f"<url><loc>{escape_xml(url)}</loc></url>")

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

    @property
    def sitemap_file(self) -> IO:
        """
        Returns file handler for a current file
        """
        assert self._sitemap_file is not None, "add_section() needs to called before"
        return self._sitemap_file

    def write_to_sitemap(self, buf: str, indent: bool = True):
        """
        Writes given string to a sitemap file
        """
        if indent:
            buf = "\t" + buf

        self.sitemap_file.write(buf + "\n")

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

    def __enter__(self):
        """
        Called when sitemap context starts
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Called when sitemap context completes
        """
        self._close_sitemap()

    def _add_sitemap(self):
        """
        Called internally to add a new sitemap:

        * when start_section() is called
        * when per-sitemap URLs counter reaches the limit
        """
        # close a previous sitemap, if any
        self._close_sitemap()

        self.sitemaps_counter += 1
        sitemap_name = "sitemap-%03d-%s.xml" % (
            self.sitemaps_counter,
            self.current_section_name,
        )

        self._sitemaps.append(sitemap_name)
        self.logger.info(f"New sitemap added: {sitemap_name}")

        # start a sitemap XML writer
        self._sitemap_file = open(f"{self.path}/{sitemap_name}", mode="wt")
        self.logger.info(f"Will write sitemap XML to {self.sitemap_file.name}")

        self.write_to_sitemap('<?xml version="1.0" encoding="UTF-8"?>', indent=False)
        self.write_to_sitemap(
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">', indent=False
        )

    def _close_sitemap(self):
        """
        Close a sitemap XML
        """
        if self._sitemap_file:
            self.logger.info(f"Closing {self.sitemap_file.name}")

            self.write_to_sitemap("</urlset>", indent=False)
            self.write_to_sitemap(
                f"<!-- {self.sitemap_urls_counter} urls in the sitemap -->",
                indent=False,
            )
            self.sitemap_file.close()
