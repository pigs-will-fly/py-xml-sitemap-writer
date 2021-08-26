black:
	black .

check:
	pylint *.py test/
	pytest --cov=xml_sitemap_writer --cov-report=term --cov-report=xml -vv
