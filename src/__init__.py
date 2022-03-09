import asyncio
from src.scrapper import Scraper

def main():
    scraper = Scraper()
    asyncio.run(scraper.run())