import requests as r
import argparse
import random

class Brewery:

    @staticmethod
    def get_random() -> str:
        response = r.get('https://api.openbrewerydb.org/v1/breweries/random')
        return response.json()[0]['id']
    
    @staticmethod
    def get_by_city(city:str)->list:
        response = r.get(f'https://api.openbrewerydb.org/v1/breweries/search?query={city}&per_page=20')
        return random.choice(response.json())['id']

    def __init__(self, api_id):
        response = r.get(f"https://api.openbrewerydb.org/v1/breweries/{api_id}")
        data = response.json()

        self.id: str = data.get("id")
        self.name: str = data.get("name")
        self.brewery_type: str = data.get("brewery_type")
        self.address_1: str | None = data.get("address_1")
        self.address_2: str | None = data.get("address_2")
        self.address_3: str | None = data.get("address_3")
        self.city: str = data.get("city")
        self.state_province: str = data.get("state_province")
        self.postal_code: str = data.get("postal_code")
        self.country: str = data.get("country")
        self.longitude: float | None = data.get("longitude")
        self.latitude: float | None = data.get("latitude")
        self.phone: str | None = data.get("phone")
        self.website_url: str | None = data.get("website_url")
        self.state: str | None = data.get("state")
        self.street: str | None = data.get("street")

    def __repr__(self):
        return f"Brewery(name={self.name}, id={self.id})"
    
    def __str__(self):
        return f"{self.name} ({self.id})\t\t{self.city}"


parser = argparse.ArgumentParser()
parser.add_argument('--city', type=str)
args = parser.parse_args()

if args.city:
    print(args.city)
    breweries = [Brewery(Brewery.get_by_city(args.city)) for _ in range(0,20)]
else:
    breweries = [Brewery(Brewery.get_random()) for _ in range(0,20)]
for b in breweries:
    print(b)