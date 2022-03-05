from dataclasses import dataclass


@dataclass
class ENDPOINTS:
    USERS: str = "/users"
    USER_ALBUMS: str = "/users/{}/albums/"
    USER_PHOTOS: str = "/users/{}/photos/"
