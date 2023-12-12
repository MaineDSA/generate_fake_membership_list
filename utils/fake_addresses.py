import requests
import random
from faker import Faker

fake = Faker()

# Geocoding API rate limit of 600 req/min https://docs.mapbox.com/api/overview/

def get_fake_address():
    return {
        "address1": fake.building_number() + " " + fake.street_name(),
        "address2": fake.secondary_address(),
        "city": fake.city(),
        "state": fake.state_abbr(),
        "zip": fake.zipcode(),
        "country": "US"
    }

def get_random_business_address(zip_code, mapbox_access_token, category='poi'):
    poi_url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{zip_code}.json?country=US&types={category}&access_token={mapbox_access_token}"
    print(poi_url)
    response = requests.get(poi_url)
    print("response: ", response.json())
    if response.status_code == 200:
        data = response.json()
        features = data['features']
        
        if features:
            place = features[0]  # Retrieve the first business found
            properties = place['properties']
            context = place.get('context', [])
            address = [item['text'] for item in context if item['id'].startswith('address')]

            # Constructing the address dictionary
            business_address = {
                "address1": address[0] if len(address) > 0 else "",
                "address2": address[1] if len(address) > 1 else "",
                "city": properties.get('address', {}).get('city', ""),
                "state": properties.get('address', {}).get('state', ""),
                "zip": properties.get('address', {}).get('postcode', ""),
                "country": properties.get('address', {}).get('country', "")
            }
            
            return business_address
    
    return None

def get_random_realistic_address(zip_code, mapbox_token):
    # Get coordinates within the provided ZIP code
    geocoding_url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{zip_code}.json?country=US&types=postcode&access_token={mapbox_token}"
    response = requests.get(geocoding_url)

    if response.status_code == 200:
        data = response.json()
        features = data['features']

        if features:
            random_location = random.choice(features)
            latitude, longitude = random_location['center']
            print("latitude: ", latitude)
            print("longitude: ", longitude)

            # Get a random realistic address based on the random coordinates
            reverse_geocoding_url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{latitude},{longitude}.json?access_token={mapbox_token}"
            response = requests.get(reverse_geocoding_url)
            print("reverse_geocoding_request: ", response.status_code)
            if response.status_code == 200:
                data = response.json()
                features = data['features']
                address_features = [feature for feature in features if 'address' in feature['place_type']]

                if address_features:
                    random_location = random.choice(address_features)
                    print(random_location)
                    address = {
                        "address1": f"{random_location['address']} {random_location['text']}",
                        "address2": "",
                        "city": next((item['text'] for item in random_location['context'] if item['id'].startswith('place.')), ""),
                        "state": next((item['text'] for item in random_location['context'] if item['id'].startswith('region.')), ""),
                        "zip": next((item['text'] for item in random_location['context'] if item['id'].startswith('postcode.')), ""),
                    }
                    return address

    return None
