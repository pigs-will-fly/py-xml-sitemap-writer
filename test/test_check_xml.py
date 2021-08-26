"""
Tests a sitemap's XML output
"""
import gzip
from tempfile import TemporaryDirectory

from xml_sitemap_writer import XMLSitemap
from . import urls_iterator, DEFAULT_HOST


def test_simple_single_sitemap_output():
    """
    Tests a single sitemap XML output
    """
    with TemporaryDirectory(prefix="sitemap_test_") as tmp_directory:
        with XMLSitemap(path=tmp_directory, root_url=DEFAULT_HOST) as sitemap:
            sitemap.add_urls(urls_iterator(count=5, prefix="product"))

        with gzip.open(f"{tmp_directory}/sitemap-001-pages.xml.gz", "rt") as xml:
            content = xml.read()

            print("xml", content)

            assert (
                '<?xml version="1.0" encoding="UTF-8"?>' in content
            ), "XML header is properly emitted"

            assert (
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                in content
            ), "Root element is properly emitted"

            assert "</urlset>" in content, "Root element is properly closed"

            assert (
                "<!-- 5 urls in the sitemap -->" in content
            ), "URLs counter is properly added"

            for idx in range(1, len(sitemap) + 1):
                assert (
                    f"<url><loc>{DEFAULT_HOST}/product_{idx}.html</loc></url>"
                    in content
                ), "URL is properly added to the sitemap"

        with open(f"{tmp_directory}/sitemap.xml", "rt", encoding="utf-8") as index_xml:
            content = index_xml.read()

            print("index_xml", content)

            assert (
                '<?xml version="1.0" encoding="UTF-8"?>' in content
            ), "XML header is properly emitted"

            assert (
                '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                in content
            ), "Root element is properly emitted"

            assert (
                f"<sitemap><loc>{DEFAULT_HOST}/sitemap-001-pages.xml.gz</loc></sitemap"
                in content
            ), "<sitemap> element is properly emitted"

            assert "<!-- 5 urls -->" in content, "URLs counter is properly added"


def test_encode_urls():
    """
    Tests URLs encoding
    """
    with TemporaryDirectory(prefix="sitemap_test_") as tmp_directory:
        with XMLSitemap(path=tmp_directory, root_url=DEFAULT_HOST) as sitemap:
            sitemap.add_url("/foo.php")
            sitemap.add_url("/foo.php?test=123")
            sitemap.add_url("/foo.php?test&bar=423")

        with gzip.open(f"{tmp_directory}/sitemap-001-pages.xml.gz", "rt") as xml:
            content = xml.read()

            print("xml", content)

            assert "<loc>http://example.net/foo.php</loc>" in content
            assert "<loc>http://example.net/foo.php?test=123</loc>" in content
            assert "<loc>http://example.net/foo.php?test&amp;bar=423</loc>" in content


def test_multi_sitemaps_urls_counter():
    """
    Tests multiple sitemaps and their URLs counter
    """
    with TemporaryDirectory(prefix="sitemap_test_") as tmp_directory:
        with XMLSitemap(path=tmp_directory, root_url=DEFAULT_HOST) as sitemap:
            sitemap.add_url("/foo.php")

            sitemap.add_section("phones")
            sitemap.add_url("/iphone")
            sitemap.add_url("/nokia")
            sitemap.add_url("/samsung")

        with gzip.open(f"{tmp_directory}/sitemap-001-pages.xml.gz", "rt") as xml:
            content = xml.read()
            print("xml", content)

            assert (
                "<!-- 1 urls in the sitemap -->" in content
            ), "There should be one URL in the sitemap"

        with gzip.open(f"{tmp_directory}/sitemap-002-phones.xml.gz", "rt") as xml:
            content = xml.read()
            print("xml", content)

            assert (
                "<!-- 3 urls in the sitemap -->" in content
            ), "There should be three URLs in the sitemap"
