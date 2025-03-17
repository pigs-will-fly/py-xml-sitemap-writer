"""
Provides XMLSitemap class used to generate large XML sitemap from iterators
"""

import gzip  # https://docs.python.org/3/library/gzip.html
import logging
import re

from datetime import datetime
from typing import List, Iterator, IO, Optional

from xml.sax.saxutils import escape as escape_xml

POWERED_BY_URL = "https://github.com/pigs-will-fly/py-xml-sitemap-writer"

W3C_DATE_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}$")
W3C_DATETIME_REGEX = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\+\d{2}:\d{2}|Z)?$"
)
CHANGEFREQ_VALUES = {
    "always",
    "hourly",
    "daily",
    "weekly",
    "monthly",
    "yearly",
    "never",
}


def is_valid_date(date_str: str) -> bool:
    """
    Checks if the provided string matches the W3C timestamp format
    https://www.w3.org/TR/NOTE-datetime
    """
    return (
        W3C_DATE_REGEX.match(date_str) is not None
        or W3C_DATETIME_REGEX.match(date_str) is not None
    )


def is_valid_changefreq(changefreq: str) -> bool:
    """
    Checks if the provided string is one of the valid values for the <changefreq> tag
    https://www.sitemaps.org/protocol.html#changefreqdef
    """
    return changefreq in CHANGEFREQ_VALUES


def is_valid_priority(priority: str) -> bool:
    """
    Checks if the provided string is a valid numeric value for the <priority> tag
    https://www.sitemaps.org/protocol.html#prioritydef
    """
    try:
        value = float(priority)
        return 0.0 <= value <= 1.0
    except ValueError:
        return False


# pylint:disable=too-many-instance-attributes
class XMLSitemap:
    """
    Generate large XML sitemaps with a sitemap index and sub-sitemap XML files
    """

    # Sitemap file that you provide must have no more than 50,000 URLs
    # and must be no larger than 10MB (10,485,760 bytes).
    # @see http://www.sitemaps.org/protocol.html#index
    URLS_PER_FILE = 15000

    GZIP_COMPRESSION_LEVEL = 9

    def __init__(self, path: str, root_url: str):
        """
        Set up XMLSitemap to write to a given path and using a specified root_url.

        root_url will be used when generating sitemaps index file.
        """
        self.path = path.rstrip("/")
        self.root_url = root_url.rstrip("/")
        self.logger = logging.getLogger(self.__class__.__name__)

        self._sitemaps = []
        self.sitemaps_counter = 0
        self.current_section_name = ""

        self.total_urls_counter = 0
        self.sitemap_urls_counter = 0

        # file handler for a current sitemap
        self._sitemap_file = None

        self.add_section("pages")

    def add_url(
        self,
        url: str,
        lastmod: Optional[str] = None,
        priority: Optional[str] = None,
        changefreq: Optional[str] = None,
    ):
        """
        Adds the provided URL to the sitemap,
        with optional lastmod, priority and changefreq properties
        https://www.sitemaps.org/protocol.html#xmlTagDefinitions
        """
        if self.sitemap_urls_counter == 0:
            self._add_sitemap()

        self.total_urls_counter += 1
        self.sitemap_urls_counter += 1

        if self.sitemap_urls_counter > self.URLS_PER_FILE:
            self.logger.info(
                f"URLs per sitemap counter reached the limit of {self.URLS_PER_FILE}"
            )
            self._add_sitemap()
            self.sitemap_urls_counter = 1

        url = f'{self.root_url}/{url.lstrip("/")}'

        if lastmod and not is_valid_date(lastmod):
            self.logger.warning(f"Invalid <lastmod> format for URL <{url}>: {lastmod}")
            lastmod = None
        if changefreq and not is_valid_changefreq(changefreq):
            self.logger.warning(
                f"Invalid <changefreq> value for URL <{url}>: {changefreq}"
            )
            changefreq = None
        if priority and not is_valid_priority(priority):
            self.logger.warning(f"Invalid <priority> value for URL <{url}>: {priority}")
            priority = None

        self.logger.debug(f"Adding URL <{url}>")
        url_entry = f"<url><loc>{escape_xml(url)}</loc>"
        if lastmod:
            url_entry += f"<lastmod>{escape_xml(lastmod)}</lastmod>"
        if priority:
            url_entry += f"<priority>{escape_xml(priority)}</priority>"
        if changefreq:
            url_entry += f"<changefreq>{escape_xml(changefreq)}</changefreq>"
        url_entry += "</url>"
        self.write_to_sitemap(url_entry)

    def add_urls(self, urls: Iterator[str]):
        """
        Add URLs for a provided iterable
        """
        for url in urls:
            self.add_url(url)

    def add_section(self, section_name: str):
        """
        Starting a new section will lazily create a new sub-sitemap with
        a filename set to "sitemap-<section_name>-<number>.xml.gz"
        """
        self._close_sitemap()

        self.current_section_name = section_name
        self.sitemap_urls_counter = 0

        # the sub-sitemap will be created after calling add_url() for the first time

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
        self._write_index()

    def _add_sitemap(self):
        """
        Called internally to add a new sitemap:

        * when the add_url() after start_section() is called for the first time
        * when per-sitemap URLs counter reaches the limit
        """
        # close a previous sitemap, if any
        self._close_sitemap()

        self.sitemaps_counter += 1
        sitemap_name = (
            f"sitemap-{self.sitemaps_counter:03}-{self.current_section_name}.xml.gz"
        )

        self._sitemaps.append(sitemap_name)
        self.logger.info(f"New sitemap added: {sitemap_name}")

        # start a sitemap XML writer
        self._sitemap_file = gzip.open(
            f"{self.path}/{sitemap_name}",
            mode="wt",
            compresslevel=self.GZIP_COMPRESSION_LEVEL,
        )
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
            self._sitemap_file = None

    def _write_index(self):
        """
        Write a sitemap index XML file
        """
        with open(f"{self.path}/sitemap.xml", mode="wt", encoding="utf-8") as index:
            self.logger.info(f"Will write sitemaps index XML to {index.name}")

            generated_on = datetime.now().strftime("%Y-%m-%d")  # e.g. 2024-11-22

            index.writelines(
                [
                    '<?xml version="1.0" encoding="UTF-8"?>\n',
                    '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n',
                    f"\t<!-- Generated on {generated_on} by {POWERED_BY_URL} -->\n",
                    f"\t<!-- {len(self)} urls in {len(self.sitemaps)} sub-sitemaps -->\n",
                ]
            )

            for sitemap in self.sitemaps:
                index.write(
                    f"\t<sitemap><loc>{self.root_url}/{escape_xml(sitemap)}</loc></sitemap>\n"
                )

            index.write("</sitemapindex>")
