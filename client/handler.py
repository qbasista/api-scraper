from typing import Dict, List, Union

from models.album import UsersAlbum
from models.photo import Photo
from models.user import User


class ResponseHandler:
    def __call__(self, status: int, body: Union[Dict, List]):
        self.status = status
        self.body = body

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
    def handle_200(self):
        return [User(**user) for user in self.body]


class UserAlbumsResponseHandler(ResponseHandler):
    def handle_200(self):
        return [UsersAlbum(**album) for album in self.body]


class UserPhotosHandler(ResponseHandler):
    def handle_200(self):
        return [Photo(**photo) for photo in self.body]
