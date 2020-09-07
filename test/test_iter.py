"""
Tests a iterator sitemap's API
"""
# https://docs.python.org/3/library/tempfile.html#tempfile.TemporaryDirectory
from tempfile import TemporaryDirectory

from xml_sitemap_writer import XMLSitemap
from . import urls_iterator


def test_add_from_iterable():
    """
    Tests adding URL via iterable
    """
    with TemporaryDirectory(prefix='sitemap_test_') as tmp_directory:
        sitemap = XMLSitemap(path=tmp_directory)
        sitemap.add_urls(urls_iterator())

        print(sitemap)

        assert len(sitemap) == 10
        assert sitemap.sitemaps == ['sitemap-001-pages.xml']
