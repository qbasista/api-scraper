from src.models.album import UsersAlbum
from src.models.photo import Photo
from src.models.user import User
from tests.mocks import users_album, user, photo


class TestUserModel:
    def setup(self):
        self.user = User(**user)

    def test_to_flat_dict(self):
        assert self.user.to_flat_dict() == {
            "id": 1,
            "name": "Leanne Graham",
            "username": "Bret",
            "email": "Sincere@april.biz",
            "address_street": "Kulas Light",
            "address_suite": "Apt. 556",
            "address_city": "Gwenborough",
            "address_zipcode": "92998-3874",
            "address_geo_lat": "-37.3159",
            "address_geo_lng": "81.1496",
            "phone": "1-770-736-8031 x56442",
            "website": "hildegard.org",
            "company_name": "Romaguera-Crona",
            "company_catchPhrase": "Multi-layered client-server neural-net",
            "company_bs": "harness real-time e-markets",
        }


class TestUsersAlbumModel:
    def setup(self):
        self.users_album = UsersAlbum(**users_album)

    def test_to_flat_dict(self):
        assert self.users_album.to_flat_dict() == users_album


class TestPhotoModel:
    def setup(self):
        self.photo = Photo(**photo)
        self.photo.set_file_path("/")

    def test_to_flat_dict(self):
        assert self.photo.to_flat_dict() == {**photo, "filePath": "/"}
