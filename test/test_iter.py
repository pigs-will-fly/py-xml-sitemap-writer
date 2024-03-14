"""
Tests a iterator sitemap's API
"""

from . import urls_iterator, test_sitemap


def test_add_from_iterable():
    """
    Tests adding URL via iterable
    """
    with test_sitemap() as sitemap:
        sitemap.add_urls(urls_iterator())

        print(sitemap)

        assert len(sitemap) == 10
        assert sitemap.sitemaps == ["sitemap-001-pages.xml.gz"]
