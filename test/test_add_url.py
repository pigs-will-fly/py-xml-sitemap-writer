"""
Tests a sitemap's add_url method

Mocks away all I/O related functions, lets the test assert the XML tag content
"""

from typing import Optional

from xml_sitemap_writer import XMLSitemap
from . import DEFAULT_HOST


class MockedXMLSitemap(XMLSitemap):
    """
    Mocked version of the XMLSitemap class that does not perform writes
    """

    def __init__(self, root_url: str):
        super().__init__(path="/", root_url=root_url)

        self._write_to_sitemap_buf: Optional[str] = None

    def _add_sitemap(self):
        """
        Skip writing gzip files while testing
        """

    def write_to_sitemap(self, buf: str, indent: bool = True):
        """
        Keeps the buf passed here for testing
        """
        self._write_to_sitemap_buf = buf

    @property
    def recent_write_to_sitemap_buf(self) -> Optional[str]:
        """
        A helper for assertions
        """
        return self._write_to_sitemap_buf


def test_add_basic_url():
    """
    Asserts that the call creates a proper simple <url> tag
    """
    sitemap = MockedXMLSitemap(root_url=DEFAULT_HOST)
    sitemap.add_url("/page_1.html")

    assert (
        sitemap.recent_write_to_sitemap_buf
        == f"<url><loc>{DEFAULT_HOST}/page_1.html</loc></url>"
    )


def test_add_url_with_props():
    """
    Asserts that the call creates a proper <url> tag with all optional subtags
    """
    sitemap = MockedXMLSitemap(root_url=DEFAULT_HOST)
    sitemap.add_url(
        "/page_1.html", priority="1.0", changefreq="daily", lastmod="1997-07-16"
    )

    assert (
        sitemap.recent_write_to_sitemap_buf
        == f"<url><loc>{DEFAULT_HOST}/page_1.html</loc>"
        f"<lastmod>1997-07-16</lastmod>"
        f"<priority>1.0</priority>"
        f"<changefreq>daily</changefreq></url>"
    )

    sitemap.add_url(
        "/page_2.html",
        priority="high",
        changefreq="every two days",
        lastmod="1997/07/16",
    )

    assert (
        sitemap.recent_write_to_sitemap_buf
        == f"<url><loc>{DEFAULT_HOST}/page_2.html</loc></url>"
    )
