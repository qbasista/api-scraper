import asyncio
from services.scrapper import Scraper


if __name__ == "__main__":
    scraper = Scraper()
    asyncio.run(scraper.run())
