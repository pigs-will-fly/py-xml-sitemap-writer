"""
Tests big sitemaps
"""
from . import urls_iterator, test_sitemap


def test_a_big_sitemap():
    """
    Tests a big sitemap
    """
    with test_sitemap() as sitemap:
        sitemap.add_urls(urls_iterator(count=100000, prefix="article"))

        print(sitemap)

        assert len(sitemap) == 100000
        assert "(100000 URLs)" in repr(sitemap)
        assert sitemap.sitemaps == [
            "sitemap-001-pages.xml.gz",
            "sitemap-002-pages.xml.gz",
            "sitemap-003-pages.xml.gz",
            "sitemap-004-pages.xml.gz",
            "sitemap-005-pages.xml.gz",
            "sitemap-006-pages.xml.gz",
            "sitemap-007-pages.xml.gz",
        ]
