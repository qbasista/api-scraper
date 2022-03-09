from setuptools import setup, find_packages

setup(
    name="api-scraper",
    version="1.0",
    description="Python script to scrap data from jsonplaceholder.typicode.com api and save to csv",
    author="Jakub Wojciechowski",
    author_email="catchthemlive@gmail.com",
    packages=find_packages(include=["api-scraper", "api-scraper.*"]),
    install_requires=[
        "pytest==7.0.1",
        "black==22.1.0",
        "python-environ==0.4.54",
        "aiohttp==3.8.1",
    ],
    entry_points={
        'console_scripts': [
            'scraper=src:main',
        ]
    }
)
