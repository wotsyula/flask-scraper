from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="flask-scraper",
    version="0.0.1",
    author="Walter Otsyula",
    author_email="wotsyula@gmail.com",
    description="Flask based scrapper that uses selenium webdriver library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wotsyula/flask-scraper",
    project_urls={
        "Bug Tracker": "https://github.com/wotsyula/flask-scraper/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
)
