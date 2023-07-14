"""
Package definition
"""
from setuptools import setup

VERSION = "0.5.1"

# @see https://packaging.python.org/tutorials/packaging-projects/#creating-setup-py
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# @see https://github.com/pypa/sampleproject/blob/master/setup.py
setup(
    name="xml_sitemap_writer",
    version=VERSION,
    author="Maciej Brencz",
    author_email="maciej.brencz@gmail.com",
    license="MIT",
    description="Python3 package for writing large XML sitemaps with no external dependencies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pigs-will-fly/py-xml-sitemap-writer",
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 5 - Production/Stable",
        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here.
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.8",
    py_modules=["xml_sitemap_writer"],
    extras_require={
        "dev": [
            "black==23.7.0",
            "coveralls==3.3.1",
            "pylint==2.17.4",
            "pytest==7.4.0",
            "pytest-cov==4.1.0",
        ]
    },
)
