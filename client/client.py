import asyncio

import aiohttp

from client.handler import (
    UsersResponseHandler,
    UserAlbumsResponseHandler,
    UserPhotosHandler,
    DownloadPhotoHandler,
)
from core import settings
from client.urls import ENDPOINTS
from models.photo import Photo


class Client:
    def __init__(self):
        self.api_url = getattr(settings, "API_URL", "http://localhost")
        self.req_limit = getattr(settings, 'IO_REQUEST_LIMIT', 100)

    async def __aenter__(self):
        print(self.req_limit)
        self._connector = aiohttp.TCPConnector(limit=self.req_limit)
        self._session = aiohttp.ClientSession(connector=self._connector)
        return self

    async def __aexit__(self, *err):
        await self._session.close()
        self._session = None

    async def get_users(self):
        print('Started get users')
        handler = UsersResponseHandler()
        async with self._session.get(self._reverse(ENDPOINTS.USERS)) as resp:
            return handler(status=resp.status, body=await resp.json())

    async def get_user_albums(self, id):
        print(f'Started get albums {id} user')
        handler = UserAlbumsResponseHandler()
        async with self._session.get(
            self._reverse(ENDPOINTS.USER_ALBUMS.format(id))
        ) as resp:
            return handler(status=resp.status, body=await resp.json())

    async def get_and_download_user_photos(self, id) -> [Photo]:
        print(f'Started get and download photos {id} user')
        photo_response = await self.get_user_photos(id)
        if isinstance(photo_response[0], Photo):
            print(f'Started download photos {id} user')
            paths = await asyncio.gather(
                *[self.download_photo(photo.url) for photo in photo_response]
            )
            return [
                photo.set_file_path(paths[i]) for i, photo in enumerate(photo_response)
            ]
        else:
            return photo_response

    async def get_user_photos(self, id) -> [Photo]:
        # print(f'Started get photos {id} user')
        handler = UserPhotosHandler()
        async with self._session.get(
            self._reverse(ENDPOINTS.USER_PHOTOS.format(id))
        ) as resp:
            return handler(status=resp.status, body=await resp.json())

    async def download_photo(self, url) -> [str]:
        # print(f'Started download photo {url}')
        handler = DownloadPhotoHandler()
        file_name = f"{settings.ASSETS_DIR}/{url.split('/')[-1:][0]}"
        async with self._session.get(url) as resp:
            return await handler(
                status=resp.status,
                body=resp.content,
                file_name=file_name,
            )

    def _reverse(self, path: str) -> str:
        return f"{self.api_url}{path}"
