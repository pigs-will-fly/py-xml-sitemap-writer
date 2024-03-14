black:
	black .

check:
	pylint xml_sitemap_writer.py test/
	pytest --cov=xml_sitemap_writer --cov-report=term --cov-report=xml --cov-fail-under=100 -vv
