import asyncio

from client.client import Client
from models.user import User
from parsers.parser import Parser


class Scraper:

    def __init__(self):
        self.client = Client()
        self.parser = Parser()

    async def run(self):
        users = await self.get_and_save_users()
        await self.get_and_save_albums(users)
        await self.get_and_save_photos(users)

    async def get_and_save_users(self):
        async with self.client as client:
            users = await client.get_users()
            self._save_to_csv(users)
            return users

    async def get_and_save_albums(self, users: [User]):
        async with self.client as client:
            albums = await asyncio.gather(
                *[client.get_user_albums(user.id) for user in users],
            )
            flat_albums = [album for user_albums in albums for album in user_albums]
            self._save_to_csv(flat_albums)
            return albums

    async def get_and_save_photos(self, users: [User]):
        async with self.client as client:
            photos = await asyncio.gather(
                *[client.get_and_download_user_photos(user.id) for user in users]
            )
            flat_photos = [photo for user_photos in photos for photo in user_photos]
            self._save_to_csv(flat_photos)
            return photos

    def _save_to_csv(self, data):
        # TODO ADD parser
        pass