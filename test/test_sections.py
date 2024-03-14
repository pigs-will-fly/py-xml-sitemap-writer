"""
Tests sitemap's custom sections
"""

from . import urls_iterator, test_sitemap


def test_custom_sitemap_section():
    """
    Test how empty sections are handled
    """
    with test_sitemap() as sitemap:
        sitemap.add_section(section_name="articles")
        sitemap.add_urls(urls_iterator(prefix="article", count=5))

        # this section is deliberately left empty
        sitemap.add_section(section_name="authors")

        sitemap.add_section(section_name="blog")
        sitemap.add_urls(urls_iterator(prefix="post", count=5))

        assert len(sitemap) == 10
        assert sitemap.sitemaps == [
            "sitemap-001-articles.xml.gz",
            "sitemap-002-blog.xml.gz",
        ]
