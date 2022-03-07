import csv
from typing import Dict

from core import settings
from models.album import UsersAlbum
from models.photo import Photo
from models.user import User


class CSVParser:
    def __init__(self):
        self.dir_path = f"{getattr(settings, 'ASSETS_DIR', '')}"

    def parse_albums_to_csv(self, albums: [UsersAlbum]):
        file_name = "albums.csv"
        fieldnames = albums[0].to_flat_dict().keys()
        data = [album.to_flat_dict() for album in albums]
        self._save_to_csv(file_name=file_name, fieldnames=fieldnames, data=data)

    def parse_users_to_csv(self, users: [User]):
        file_name = "users.csv"
        fieldnames = users[0].to_flat_dict().keys()
        data = [user.to_flat_dict() for user in users]
        self._save_to_csv(file_name=file_name, fieldnames=fieldnames, data=data)

    def parse_photos_to_csv(self, photos: [Photo]):
        file_name = "photos.csv"
        fieldnames = photos[0].to_flat_dict().keys()
        data = [photo.to_flat_dict() for photo in photos]
        self._save_to_csv(file_name=file_name, fieldnames=fieldnames, data=data)

    def _save_to_csv(self, file_name: str, fieldnames: [str], data: [Dict]):
        with open(f"{self.dir_path}/{file_name}", "w+") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            [writer.writerow(item) for item in data]
