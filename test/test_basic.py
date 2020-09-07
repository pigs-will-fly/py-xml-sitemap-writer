"""
Tests a basic sitemap's API
"""
# https://docs.python.org/3/library/tempfile.html#tempfile.TemporaryDirectory
from tempfile import TemporaryDirectory

from xml_sitemap_writer import XMLSitemap
from . import urls_iterator


def test_simple_single_sitemap():
    """
    Tests a single sitemap
    """
    with TemporaryDirectory(prefix='sitemap_test_') as tmp_directory:
        sitemap = XMLSitemap(path=tmp_directory)

        for url in urls_iterator():
            sitemap.add_url(url)

        print(sitemap)

        assert len(sitemap) == 10
        assert sitemap.sitemaps == ['sitemap-001-pages.xml']


def test_sub_sitemaps():
    """
    Tests two sub-sitemaps
    """
    with TemporaryDirectory(prefix='sitemap_test_') as tmp_directory:
        sitemap = XMLSitemap(path=tmp_directory)

        for url in urls_iterator():
            sitemap.add_url(url)

        sitemap.add_section(section_name='users')

        for url in urls_iterator(prefix='user'):
            sitemap.add_url(url)

        print(sitemap)

        assert len(sitemap) == 20
        assert sitemap.sitemaps == ['sitemap-001-pages.xml', 'sitemap-002-users.xml']
