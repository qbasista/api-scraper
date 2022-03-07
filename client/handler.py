from datetime import datetime
from typing import Any

from models.album import UsersAlbum
from models.photo import Photo
from models.user import User


class ResponseHandler:
    def __call__(self, status: int, body: Any, **kwargs):
        self.status = status
        self.body = body
        self.kwargs = kwargs

        try:
            return getattr(self, f"handle_{self.status}")()
        except AttributeError:
            return self.handle_rest()

    def handle_200(self):
        return self.body

    def handle_400(self):
        raise Exception(f"Bad request: {self.status} - {self.body}")

    def handle_404(self):
        raise Exception(f"Not found: {self.status} - {self.body}")

    def handle_500(self):
        raise Exception(f"External Server Error")

    def handle_rest(self):
        raise Exception(f"Unknown error: {self.status} - {self.body}")


class UsersResponseHandler(ResponseHandler):
    def handle_200(self) -> [User]:
        print(f"Time: {datetime.now()} Get users!")
        return [User(**user) for user in self.body]


class UserAlbumsResponseHandler(ResponseHandler):
    def handle_200(self) -> [UsersAlbum]:
        print(f"Time: {datetime.now()} Get user albums")
        return [UsersAlbum(**album) for album in self.body]


class UserPhotosHandler(ResponseHandler):
    def handle_200(self) -> [Photo]:
        print(f"Time: {datetime.now()} Get user photos")
        return [Photo(**photo) for photo in self.body]


class DownloadPhotoHandler(ResponseHandler):
    async def handle_200(self) -> str:
        print(f"Time: {datetime.now()} Saved photo")
        with open(self.kwargs.get("file_name"), "wb+") as fd:
            async for chunk in self.body.iter_chunked(2048):
                fd.write(chunk)
                print(f"Saved {fd.name}")
                return fd.name
