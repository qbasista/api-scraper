import pytest

from client.client import Client
from client.handler import (
    ResponseHandler,
    UsersResponseHandler,
    UserAlbumsResponseHandler,
    UserPhotosHandler,
)
from models.album import UsersAlbum
from models.photo import Photo
from models.user import User
from tests.mocks.album_mock import users_album
from tests.mocks.photo_mock import photo
from tests.mocks.user_mock import user


# @pytest.mark.asyncio
# class TestClient:
#     def setup(self):
#         self.client = Client()
#
#     async def test_get_users(self):
#         async with self.client as client:
#             resp = await client.get_users()
#             assert resp == ""


class TestResponseHandler:
    def setup(self):
        self.handler = ResponseHandler()

    def test_handle_200(self):
        status = 200
        body = {"body": "ok"}

        assert self.handler(status=status, body=body) == body

    def test_handle_400(self):
        status = 400
        body = {"message": "Bad request"}

        with pytest.raises(Exception, match=f"Bad request: {status} - {body}"):
            self.handler(status=status, body=body)

    def test_handle_404(self):
        status = 404
        body = {"message": "Not found"}

        with pytest.raises(Exception, match=f"Not found: {status} - {body}"):
            self.handler(status=status, body=body)

    def test_handle_500(self):
        status = 500
        body = {"message": "External Server Error"}

        with pytest.raises(Exception, match=f"External Server Error"):
            self.handler(status=status, body=body)

    def test_rest(self):
        status = 401
        body = {"message": "UNAUTHORIZED"}

        with pytest.raises(Exception, match=f"Unknown error: {status} - {body}"):
            self.handler(status=status, body=body)


class TestUsersResponseHandler:
    def setup(self):
        self.handler = UsersResponseHandler()

    def test_handle_200(self):
        status = 200

        assert str(self.handler(status=status, body=[user])[0]) == str(User(**user))


class TestUserAlbumsResponseHandler:
    def setup(self):
        self.handler = UserAlbumsResponseHandler()

    def test_handle_200(self):
        status = 200

        assert str(self.handler(status=status, body=[users_album])[0]) == str(
            UsersAlbum(**users_album)
        )


class TestUserPhotosHandler:
    def setup(self):
        self.handler = UserPhotosHandler()

    def test_handle_200(self):
        status = 200

        assert str(self.handler(status=status, body=[photo])[0]) == str(Photo(**photo))
