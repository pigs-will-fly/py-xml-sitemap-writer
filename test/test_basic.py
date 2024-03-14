"""
Tests a basic sitemap's API
"""

from . import urls_iterator, test_sitemap


def test_simple_single_sitemap():
    """
    Tests a single sitemap
    """
    with test_sitemap() as sitemap:
        sitemap.add_section("articles")

        for url in urls_iterator():
            sitemap.add_url(url)

        print(sitemap)

        assert len(sitemap) == 10
        assert "(10 URLs)" in repr(sitemap)
        assert sitemap.sitemaps == ["sitemap-001-articles.xml.gz"]


def test_sub_sitemaps():
    """
    Tests two sub-sitemaps
    """
    with test_sitemap() as sitemap:
        for url in urls_iterator():
            sitemap.add_url(url)

        sitemap.add_section(section_name="users")

        for url in urls_iterator(prefix="user"):
            sitemap.add_url(url)

        print(sitemap)

        assert len(sitemap) == 20
        assert sitemap.sitemaps == [
            "sitemap-001-pages.xml.gz",
            "sitemap-002-users.xml.gz",
        ]
