import aiohttp

from client.handler import (
    UsersResponseHandler,
    UserAlbumsResponseHandler,
    UserPhotosHandler,
    DownloadPhotoHandler,
)
from core import settings
from client.urls import ENDPOINTS


class Client:
    def __init__(self):
        self.api_url = getattr(settings, "API_URL", "http://localhost")

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *err):
        await self._session.close()
        self._session = None

    async def get_users(self):
        handler = UsersResponseHandler()
        async with self._session.get(self._reverse(ENDPOINTS.USERS)) as resp:
            return handler(status=resp.status, body=await resp.json())

    async def get_user_albums(self, id):
        handler = UserAlbumsResponseHandler()
        async with self._session.get(
            self._reverse(ENDPOINTS.USER_ALBUMS.format(id))
        ) as resp:
            return handler(status=resp.status, body=await resp.json())

    async def get_user_photos(self, id):
        handler = UserPhotosHandler()
        async with self._session.get(
            self._reverse(ENDPOINTS.USER_PHOTOS.format(id))
        ) as resp:
            return handler(status=resp.status, body=await resp.json())

    async def download_photo(self, url):
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
