import csv
from typing import Dict

from core import settings
from models.album import UsersAlbum
from models.photo import Photo
from models.user import User


class CSVParser:
    def __init__(self):
        self.dir_path = f"{getattr(settings, 'ASSETS_DIR', '')}"

    def parse_albums_to_csv(self, albums: [UsersAlbum]) -> None:
        self._save_to_csv(file_name="albums.csv", **self._prepare_data(data=albums))

    def parse_users_to_csv(self, users: [User]) -> None:
        self._save_to_csv(file_name="users.csv", **self._prepare_data(data=users))

    def parse_photos_to_csv(self, photos: [Photo]) -> None:
        self._save_to_csv(file_name="photos.csv", **self._prepare_data(data=photos))

    def _prepare_data(self, data: [any], sort_key: str = "id") -> Dict:
        fieldnames: [str] = list(data[0].to_flat_dict().keys())
        data: [Dict] = [item.to_flat_dict() for item in data]
        result: [Dict] = self._sort(data=self._remove_duplicates(data), by=sort_key)
        return {"fieldnames": fieldnames, "data": result}

    @staticmethod
    def _sort(data: [Dict], by: str) -> [Dict]:
        return sorted(data, key=lambda d: d[by])

    @staticmethod
    def _remove_duplicates(data: [Dict]) -> [Dict]:
        return [dict(t) for t in {tuple(d.items()) for d in data}]

    def _save_to_csv(self, file_name: str, fieldnames: [str], data: [Dict]) -> None:
        with open(f"{self.dir_path}/{file_name}", "w+") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            [writer.writerow(item) for item in data]
