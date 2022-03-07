class Album:
    id: int
    title: str

    def __init__(self, **kwargs):
        self.id = int(kwargs.get("id"))
        self.title = kwargs.get("title")


class UsersAlbum(Album):
    user_id: int

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = int(kwargs.get("userId"))

    def __repr__(self):
        return f"{self.id}. {self.title} user_id: {self.user_id}"

    def to_flat_dict(self):
        flat = {**self.__dict__}
        flat["userId"] = flat.pop("user_id")
        return flat
