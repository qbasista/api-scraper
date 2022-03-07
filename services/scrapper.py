import asyncio
from client.client import Client
from models.user import User
from parsers.parser import CSVParser


class Scraper:
    def __init__(self):
        self.client = Client()
        self.parser = CSVParser()

    async def run(self):
        async with self.client:
            users = await self.get_and_save_users()
            await self.get_and_save_albums(users)
            await self.get_and_save_photos(users)

    async def get_and_save_users(self) -> [User]:
        users = await self.client.get_users()
        self.parser.parse_users_to_csv(users)
        return users

    async def get_and_save_albums(self, users: [User]):
        albums = await asyncio.gather(
            *[self.client.get_user_albums(user.id) for user in users],
        )
        flat_albums = [album for user_albums in albums for album in user_albums]
        self.parser.parse_albums_to_csv(flat_albums)

    async def get_and_save_photos(self, users: [User]):
        photos = []
        for user in users:
            photos = [*photos, *(await self.client.get_and_download_user_photos(user.id))]
        self.parser.parse_photos_to_csv(photos)
