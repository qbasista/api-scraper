from setuptools import setup, find_packages

setup(
    name="api-scraper",
    version="1.0",
    description="Python script to scrap data from api and save to csv",
    author="Jakub Wojciechowski",
    author_email="catchthemlive@gmail.com",
    packages=find_packages(include=["api-scraper", "api-scraper.*"]),
    install_requires=["pytest", "black", "python-environ", "aiohttp"],
)
