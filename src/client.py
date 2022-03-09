from datetime import datetime
from pathlib import Path

import aiohttp
import backoff
from aiohttp import ClientResponseError

import settings
from src.models.album import UsersAlbum
from src.models.photo import Photo

from dataclasses import dataclass

from src.models.user import User


@dataclass
class ENDPOINTS:
    USERS: str = "/users"
    USER_ALBUMS: str = "/users/{}/albums/"
    USER_PHOTOS: str = "/users/{}/photos/"


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

    @backoff.on_exception(backoff.expo, ClientResponseError, max_tries=2)
    async def get_users(self):
        print("Started get users")
        async with self._session.get(
            self._reverse(ENDPOINTS.USERS), raise_for_status=True
        ) as resp:
            print(f"Time: {datetime.now()} Get users!")

            return [User(**user) for user in await resp.json()]

    @backoff.on_exception(backoff.expo, ClientResponseError, max_tries=2)
    async def get_user_albums(self, id: int):
        print(f"Started get users albums")
        async with self._session.get(
            self._reverse(ENDPOINTS.USER_ALBUMS.format(id)), raise_for_status=True
        ) as resp:
            print(f"Time: {datetime.now()} Get user albums")
            return [UsersAlbum(**album) for album in await resp.json()]

    @backoff.on_exception(backoff.expo, ClientResponseError, max_tries=2)
    async def get_user_photos(self, id: int):
        print(f"Started get users {id} photos")
        async with self._session.get(
            self._reverse(ENDPOINTS.USER_PHOTOS.format(id)), raise_for_status=True
        ) as resp:
            print(f"Time: {datetime.now()} Get user photos")
            return [Photo(**photo) for photo in await resp.json()]

    @backoff.on_exception(backoff.expo, ClientResponseError, max_tries=2)
    async def download_photo(self, url) -> [str]:
        file_name = f"{settings.ASSETS_DIR}/photos/{url.split('/')[-1:][0]}"
        if Path(file_name).is_file():
            print(f"file {file_name} exists")
            return file_name
        else:
            async with self._session.get(url, raise_for_status=True) as resp:
                with open(file_name, "wb+") as fd:
                    async for chunk in resp.content.iter_chunked(2048):
                        fd.write(chunk)
                        print(f"Saved {fd.name}")
                        return fd.name


    def _reverse(self, path: str) -> str:
        return f"{self.API_URL}{path}"
