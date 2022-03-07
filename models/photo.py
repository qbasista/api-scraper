from typing import Optional, Dict


class Photo:
    id: int
    album_id: int
    title: str
    url: str
    thumbnail_url: str
    file_path: Optional[str]

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.album_id = kwargs.get("albumId")
        self.title = kwargs.get("title")
        self.url = kwargs.get("url")
        self.thumbnail_url = kwargs.get("thumbnailUrl")
        self.file_path = None

    def __repr__(self):
        return f"{self.id}. album: {self.album_id} - {self.title}"

    def get_file_path(self) -> Optional[FileNotFoundError, str]:
        if not self.file_path:
            raise FileNotFoundError("File wasn't save locally")
        return self.file_path

    def set_file_path(self, file_path) -> None:
        self.file_path = file_path

    def to_flat_dict(self) -> Dict:
        flat = {**self.__dict__}
        flat["thumbnailUrl"] = flat.pop("thumbnail_url")
        flat["albumId"] = flat.pop("album_id")
        flat["filePath"] = flat.pop("file_path")
        return flat
