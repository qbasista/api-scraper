import asyncio
from src.client import Client
from src.models.photo import Photo
from src.models.user import User
from src.csv_writer import CSVWriter


class Scraper:
    def __init__(self):
        self.client = Client()
        self.parser = CSVWriter()

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
            photos = [
                *photos,
                *(await self._get_and_download_user_photos(user.id)),
            ]
        self.parser.parse_photos_to_csv(photos)

    async def _get_and_download_user_photos(self, id: int):

        print(f"Started get and download user {id} photos")
        photo_response = await self.client.get_user_photos(id)

        if isinstance(photo_response[0], Photo):
            await self._download_photos(photo_response)
        return photo_response

    async def _download_photos(self, photos: [Photo]) -> None:

        paths = await asyncio.gather(
            *[self.client.download_photo(photo.url) for photo in photos]
        )
        [photo.set_file_path(paths[i]) for i, photo in enumerate(photos)]
