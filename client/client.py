import asyncio
from pathlib import Path
from typing import Optional, Union

import aiohttp

from client.handler import (
    UsersResponseHandler,
    UserAlbumsResponseHandler,
    UserPhotosHandler,
    DownloadPhotoHandler,
)
from core import settings
from client.urls import ENDPOINTS
from models.album import UsersAlbum
from models.photo import Photo
from models.user import User


class Client:
    API_URL: str = getattr(settings, "API_URL", "http://localhost")
    REQ_LIMIT: int = getattr(settings, "IO_REQUEST_LIMIT", 100)
    TIMEOUT: int = getattr(settings, "CLIENT_TIMEOUT", 300)

    async def __aenter__(self):
        self._timeout = aiohttp.ClientTimeout(total=self.TIMEOUT)
        self._connector = aiohttp.TCPConnector(limit=self.REQ_LIMIT, force_close=True)
        self._session = aiohttp.ClientSession(
            connector=self._connector, timeout=self._timeout, trust_env=True
        )
        return self

    async def __aexit__(self, *err):
        await self._session.close()
        self._session = None

    async def get_users(self) -> Optional[Union[list[User], BaseException]]:
        print("Started get users")
        async with self._session.get(self._reverse(ENDPOINTS.USERS)) as resp:
            return UsersResponseHandler()(status=resp.status, body=await resp.json())

    async def get_user_albums(self, id: int) -> Optional[Union[list[UsersAlbum], BaseException]]:
        print(f"Started get albums {id} user")
        async with self._session.get(
            self._reverse(ENDPOINTS.USER_ALBUMS.format(id))
        ) as resp:
            return UserAlbumsResponseHandler()(status=resp.status, body=await resp.json())

    async def get_and_download_user_photos(
        self, id: int
    ) -> Optional[Union[list[Photo], BaseException]]:

        print(f"Started get and download photos {id} user")
        photo_response = await self.get_user_photos(id)

        if isinstance(photo_response[0], Photo):
            await self.download_photos(photo_response)
        return photo_response

    async def get_user_photos(self, id: int) -> Optional[Union[list[Photo], BaseException]]:
        async with self._session.get(
            self._reverse(ENDPOINTS.USER_PHOTOS.format(id))
        ) as resp:
            return UserPhotosHandler()(status=resp.status, body=await resp.json())

    async def download_photos(self, photos: [Photo]) -> None:
        print(f"Started download photos {id} user")
        paths = await asyncio.gather(
            *[self.download_photo(photo.url) for photo in photos]
        )
        [photo.set_file_path(paths[i]) for i, photo in enumerate(photos)]

    async def download_photo(self, url) -> [str]:
        file_name = f"{settings.ASSETS_DIR}/photos/{url.split('/')[-1:][0]}"
        if Path(file_name).is_file():
            print("file exists")
            return file_name
        else:
            async with self._session.get(url) as resp:
                return await DownloadPhotoHandler()(
                    status=resp.status,
                    body=resp.content,
                    file_name=file_name,
                )

    def _reverse(self, path: str) -> str:
        return f"{self.API_URL}{path}"
