class Photo:
    id: int
    album_id: int
    title: str
    url: str
    thumbnail_url: str
    _local_path: str = None

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.album_id = kwargs.get("albumId")
        self.title = kwargs.get("title")
        self.url = kwargs.get("url")
        self.thumbnail_url = kwargs.get("thumbnail_url")

    def __repr__(self):
        return f"{self.id}. album: {self.album_id} - {self.title}"

    def save(self):
        # TODO save locally
        pass

    def get_local_path(self):
        if not self._local_path:
            raise FileNotFoundError("File wasn't save locally")
        return self._local_path
