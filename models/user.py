from typing import Optional


class Geo:
    lat: Optional[str]
    lng: Optional[str]

    def __init__(self, **kwargs):
        self.lat = kwargs.get("lat")
        self.lng = kwargs.get("lng")


class Address:
    street: Optional[str]
    suite: str
    city: str
    zipcode: str
    geo: Geo

    def __init__(self, **kwargs):
        self.street = kwargs.get("street")
        self.suite = kwargs.get("suit")
        self.city = kwargs.get("city")
        self.zipcode = kwargs.get("zipcode")
        self.geo = Geo(**kwargs.get("geo"))


class Company:
    name: str
    catch_phrase: str
    bs: str

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.catch_phrase = kwargs.get("catchPhrase")
        self.bs = kwargs.get("bs")


class User:
    id: int
    name: str
    username: str
    email: str
    address: Address
    phone: str
    website: str
    company: Company

    def __init__(self, **kwargs):
        self.id = int(kwargs.get("id"))
        self.name = kwargs.get("name")
        self.username = kwargs.get("username")
        self.email = kwargs.get("email")
        self.address = Address(**kwargs.get("address"))
        self.phone = kwargs.get("phone")
        self.website = kwargs.get("website")
        self.company = Company(**kwargs.get("company"))

    def __repr__(self):
        return f'{self.id}. {self.name} - "{self.username}"'
