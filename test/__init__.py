"""
Generic helper functions
"""
from contextlib import contextmanager

# @see https://docs.python.org/3/library/tempfile.html#tempfile.TemporaryDirectory
from tempfile import TemporaryDirectory
from typing import Iterator, ContextManager

from xml_sitemap_writer import XMLSitemap


def urls_iterator(
    count: int = 10, prefix: str = "page_", host: str = "http://example.net"
) -> Iterator[str]:
    """
    Returns URLs iterator
    """
    for idx in range(1, count + 1):
        yield f"{host}/{prefix}_{idx}.html"


@contextmanager
def test_sitemap() -> ContextManager[XMLSitemap]:
    """
    Context for a test sitemap operating in a temporary directory
    """
    with TemporaryDirectory(prefix="sitemap_test_") as tmp_directory:
        yield XMLSitemap(path=tmp_directory)
