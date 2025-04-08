"""Multiple methods of faking addresses, some relying on API access."""

import random
from pathlib import Path

import attrs
import mapbox
import ratelimit
from faker import Faker

fake = Faker()
MAPBOX_TOKEN_PATH = Path(".mapbox_token")
geocoder = mapbox.Geocoder()
if MAPBOX_TOKEN_PATH.is_file():
    geocoder = mapbox.Geocoder(access_token=MAPBOX_TOKEN_PATH.read_text(encoding="UTF-8"))


# Geocoding API rate limit of 600 req/min https://docs.mapbox.com/api/overview/


@attrs.define
class Address:
    """Represents a complete address along with an optional latitude and longitude."""

    address1: str = attrs.field()
    address2: str = attrs.field()
    city: str = attrs.field()
    state: str = attrs.field()
    zip: str = attrs.field()
    country: str = attrs.field()
    lat: float | None
    lon: float | None


def get_fake_address(zip_code: str | None = None) -> Address:
    """Create an entirely made-up address."""
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


@ratelimit.sleep_and_retry
@ratelimit.limits(calls=600, period=60)
def get_random_realistic_address(zip_code: str) -> Address | None:
    """Find a random address within a provided zip code."""
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
