black:
	black .

check:
	pylint *.py test/
	pytest -vv
