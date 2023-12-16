"""Multiple methods of faking addresses, some relying on API access."""

import random
from pathlib import Path
from faker import Faker
from mapbox import Geocoder
from ratelimit import limits, sleep_and_retry

fake = Faker()
geocoder = Geocoder(access_token=Path(".mapbox_token").read_text(encoding="UTF-8"))

# Geocoding API rate limit of 600 req/min https://docs.mapbox.com/api/overview/


def get_fake_address():
    """Create an entirely made-up address"""
    return {
        "address1": fake.building_number() + " " + fake.street_name(),
        "address2": fake.secondary_address(),
        "city": fake.city(),
        "state": fake.state_abbr(),
        "zip": fake.zipcode(),
        "country": "US",
    }


@sleep_and_retry
@limits(calls=600, period=60)
def get_random_business_address(zip_code, category="poi"):
    """Find the address of a random business within a provided zip code"""
    response = geocoder.forward(zip_code, types=[category], country=["us"])
    if response.status_code != 200:
        return None

    data = response.json()
    if ("features" not in data) or (len(data["features"]) == 0):
        return None

    place = data["features"][0]  # Retrieve the first business found
    properties = place["properties"]
    context = place.get("context", [])
    address = [item["text"] for item in context if item["id"].startswith("address")]

    # Constructing the address dictionary
    return {
        "address1": address[0] if len(address) > 0 else "",
        "address2": address[1] if len(address) > 1 else "",
        "city": properties.get("address", {}).get("city", ""),
        "state": properties.get("address", {}).get("state", ""),
        "zip": properties.get("address", {}).get("postcode", ""),
        "country": properties.get("address", {}).get("country", ""),
    }


@sleep_and_retry
@limits(calls=600, period=60)
def get_random_realistic_address(zip_code):
    """Find a random address within a provided zip code"""
    response = geocoder.forward(zip_code, country=["us"])

    if response.status_code != 200:
        return None

    data = response.json()
    if "features" not in data:
        return None

    random_location = random.choice(data["features"])
    longitude, latitude = random_location["center"]

    # Get a random realistic address based on the random coordinates
    response = geocoder.reverse(lon=longitude, lat=latitude)
    if response.status_code != 200:
        return None

    data = response.json()

    address_features = [
        feature for feature in data["features"] if "address" in feature["place_type"]
    ]
    if not address_features:
        return None

    random_location = random.choice(address_features)
    if "address" not in random_location:
        return None

    return {
        "address1": f"{random_location['address']} {random_location['text']}",
        "address2": "",
        "city": next(
            (
                item["text"]
                for item in random_location["context"]
                if item["id"].startswith("place.")
            ),
            "",
        ),
        "state": next(
            (
                item["text"]
                for item in random_location["context"]
                if item["id"].startswith("region.")
            ),
            "",
        ),
        "zip": next(
            (
                item["text"]
                for item in random_location["context"]
                if item["id"].startswith("postcode.")
            ),
            "",
        ),
        "lat": latitude,
        "lon": longitude,
    }
