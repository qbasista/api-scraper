from typing import Optional, Dict

from models.utils import add_prefix_to_keys


class Geo:
    lat: Optional[str]
    lng: Optional[str]

    def __init__(self, **kwargs):
        self.lat = kwargs.get("lat")
        self.lng = kwargs.get("lng")

    def to_flat_dict(self, prefix=None):
        flat = {**self.__dict__}
        if prefix:
            return add_prefix_to_keys(data=flat, prefix=prefix)
        return flat


class Address:
    street: Optional[str]
    suite: str
    city: str
    zipcode: str
    geo: Geo

    def __init__(self, **kwargs):
        self.street = kwargs.get("street")
        self.suite = kwargs.get("suite")
        self.city = kwargs.get("city")
        self.zipcode = kwargs.get("zipcode")
        self.geo = Geo(**kwargs.get("geo"))

    def to_flat_dict(self, prefix: str = None) -> Dict:
        flat = {**self.__dict__}
        geo = flat.pop("geo")
        flat = {**flat, **geo.to_flat_dict(prefix="geo")}
        if prefix:
            return add_prefix_to_keys(data=flat, prefix=prefix)
        return flat


class Company:
    name: str
    catch_phrase: str
    bs: str

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.catch_phrase = kwargs.get("catchPhrase")
        self.bs = kwargs.get("bs")

    def to_flat_dict(self, prefix: str = None) -> Dict:
        flat = {**self.__dict__}
        flat["catchPhrase"] = flat.pop("catch_phrase")
        if prefix:
            flat = add_prefix_to_keys(flat, prefix)
        return flat


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

    def to_flat_dict(self):
        flat = {**self.__dict__}
        company = flat.pop("company")
        address = flat.pop("address")
        return {
            **flat,
            **company.to_flat_dict(prefix="company"),
            **address.to_flat_dict(prefix="address"),
        }
