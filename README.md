# py-xml-sitemap-writer
Python3 package for writing large XML sitemaps with no external dependencies.

```
pip install py-xml-sitemap-writer
```

## Usage

This package is meant to **generate sitemaps with hundred of thousands URLs** in **memory-efficient way** by
making using of **iterators to populate sitemap** with URLs.

```python
from typing import Iterator
from xml_sitemap_writer import XMLSitemap

def get_products_for_sitemap() -> Iterator[str]:
    """
    Replace the logic below with a query from your database.
    """
    for idx in range(1, 1000001):
        yield f"https://your.site.io/product/{idx}.html"

with XMLSitemap(path='/your/web/root', root_url='http:s//your.site.io') as sitemap:
    sitemap.add_section('products')
    sitemap.add_urls(get_products_for_sitemap())
```

`sitemap.xml` and `sitemap-00N.xml.gz` files will be generated once this code runs:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
	<!-- Powered by https://github.com/pigs-will-fly/py-xml-sitemap-writer -->
	<!-- 100000 urls -->
	<sitemap><loc>https://your.site.io/sitemap-products-001.xml.gz</loc></sitemap>
	<sitemap><loc>https://your.site.io/sitemap-products-002.xml.gz</loc></sitemap>
    ...
</sitemapindex>
```

And gzipped sub-sitemaps with up to 15.000 URLs each:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
	<url><loc>https://your.site.io/product/1.html</loc></url>
	<url><loc>https://your.site.io/product/2.html</loc></url>
	<url><loc>https://your.site.io/product/3.html</loc></url>
    ...
</urlset>
<!-- 15000 urls in the sitemap -->
```