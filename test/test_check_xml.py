"""
Tests a sitemap's XML output
"""
from tempfile import TemporaryDirectory

from xml_sitemap_writer import XMLSitemap
from . import urls_iterator


def test_simple_single_sitemap_output():
    """
    Tests a single sitemap XML output
    """
    with TemporaryDirectory(prefix="sitemap_test_") as tmp_directory:
        with XMLSitemap(path=tmp_directory) as sitemap:
            sitemap.add_urls(urls_iterator())

        with open(f"{tmp_directory}/sitemap-001-pages.xml", "rt") as xml:
            content = xml.read()

            print("xml", content)

            assert (
                '<?xml version="1.0" encoding="UTF-8"?>' in content
            ), "XML header is properly emitted"
            assert (
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                in content
            ), "Root element is properly emitted"
