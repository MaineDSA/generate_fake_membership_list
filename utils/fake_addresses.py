"""Multiple methods of faking addresses, some relying on API access."""

import random
from pathlib import Path
from attrs import define, field
from faker import Faker
from mapbox import Geocoder
from ratelimit import limits, sleep_and_retry

fake = Faker()
geocoder = Geocoder(access_token=Path(".mapbox_token").read_text(encoding="UTF-8"))

# Geocoding API rate limit of 600 req/min https://docs.mapbox.com/api/overview/


@define
class Address:
    """Represents a complete address along with an optional latitude and longitude"""

    address1: str = field()
    address2: str = field()
    city: str = field()
    state: str = field()
    zip: str = field()
    country: str = field()
    lat: float
    lon: float


def get_fake_address(zip_code: str) -> Address:
    """Create an entirely made-up address"""
    return Address(
        address1=fake.building_number() + " " + fake.street_name(),
        address2=fake.secondary_address(),
        city=fake.city(),
        state=fake.state_abbr(),
        zip=zip_code or fake.zipcode(),
        country="US",
        lat=None,
        lon=None,
    )


@sleep_and_retry
@limits(calls=600, period=60)
def get_random_realistic_address(zip_code: str) -> Address:
    """Find a random address within a provided zip code"""
    response_forward = geocoder.forward(zip_code, country=["us"])

    if response_forward.status_code != 200:
        return None

    data_forward = response_forward.json()
    if "features" not in data_forward or len(data_forward["features"]) == 0:
        return None

    random_location = random.choice(data_forward["features"])
    longitude, latitude = random_location["center"]

    # Get a random realistic address based on the random coordinates
    response_reverse = geocoder.reverse(lon=longitude, lat=latitude)
    if response_reverse.status_code != 200:
        return None

    address_features = [feature for feature in response_reverse.json()["features"] if "address" in feature["place_type"]]
    if not address_features:
        return None

    random_location = random.choice(address_features)
    if "address" not in random_location:
        return None

    return Address(
        address1=f"{random_location['address']} {random_location['text']}",
        address2="",
        city=next(
            (item["text"] for item in random_location["context"] if item["id"].startswith("place.")),
            "",
        ),
        state=next(
            (item["text"] for item in random_location["context"] if item["id"].startswith("region.")),
            "",
        ),
        zip=next(
            (item["text"] for item in random_location["context"] if item["id"].startswith("postcode.")),
            "",
        ),
        country="US",
        lat=latitude,
        lon=longitude,
    )
