import os
import requests
from abc import ABC, abstractmethod

def get_timezone_for_country(country_name: str) -> str:
    c = country_name.lower()
    if "india" in c:
        return "Asia/Kolkata"
    elif "nepal" in c:
        return "Asia/Kathmandu"
    elif "bangladesh" in c:
        return "Asia/Dhaka"
    elif "sri lanka" in c:
        return "Asia/Colombo"
    elif "pakistan" in c:
        return "Asia/Karachi"
    elif "bhutan" in c:
        return "Asia/Thimphu"
    elif "maldives" in c:
        return "Indian/Maldives"
    elif "united states" in c or "usa" in c:
        return "America/Los_Angeles"
    elif "japan" in c:
        return "Asia/Tokyo"
    return "UTC"

class BaseGeocodingProvider(ABC):
    """
    Abstract interface for location geocoding services.
    Enables swapping backends (e.g. OpenStreetMap to Google Maps) seamlessly.
    """
    
    @abstractmethod
    def geocode(self, location_name: str) -> dict:
        """
        Geocodes a textual location name.
        Returns:
            dict containing:
                "location": str (standardized name/place)
                "latitude": float
                "longitude": float
                "country": str
        Raises:
            ValueError if the location cannot be resolved.
        """
        pass

    @abstractmethod
    def reverse_geocode(self, lat: float, lon: float) -> dict:
        """
        Reverse geocodes coordinate values to textual location metadata.
        Returns:
            dict containing:
                "location": str (city/state description)
                "country": str
                "city": str
                "district": str
                "state": str
                "postal_code": str
                "timezone": str
        Raises:
            ValueError if the coordinates cannot be resolved.
        """
        pass


class NominatimGeocodingProvider(BaseGeocodingProvider):
    """
    OpenStreetMap Nominatim Geocoding API implementation.
    No API keys required, open source and free.
    """

    def geocode(self, location_name: str) -> dict:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": location_name,
            "format": "json",
            "addressdetails": 1,
            "limit": 1
        }
        headers = {
            "User-Agent": "CrisisNetAI/1.0 (contact@crisisnet.ai; Kaggle Capstone Submission)"
        }
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=8)
            response.raise_for_status()
            results = response.json()
            
            if not results:
                raise ValueError(f"Could not resolve place name: '{location_name}'")
                
            place = results[0]
            lat = float(place["lat"])
            lon = float(place["lon"])
            
            address = place.get("address", {})
            country = address.get("country", "Unknown Country")
            
            resolved_name = (
                address.get("city") or 
                address.get("town") or 
                address.get("state") or 
                place.get("name") or 
                location_name
            )

            return {
                "location": resolved_name,
                "latitude": lat,
                "longitude": lon,
                "country": country
            }
            
        except requests.RequestException as e:
            raise ValueError(f"Nominatim API request error: {e}")
        except (KeyError, IndexError, TypeError, ValueError) as e:
            raise ValueError(f"Nominatim parser error: {e}")

    def reverse_geocode(self, lat: float, lon: float) -> dict:
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            "lat": lat,
            "lon": lon,
            "format": "json",
            "addressdetails": 1
        }
        headers = {
            "User-Agent": "CrisisNetAI/1.0 (contact@crisisnet.ai; Kaggle Capstone Submission)"
        }
        try:
            response = requests.get(url, params=params, headers=headers, timeout=8)
            response.raise_for_status()
            result = response.json()
            
            if not result or "error" in result:
                raise ValueError(f"Could not reverse geocode coordinates: {lat}, {lon}")
                
            address = result.get("address", {})
            country = address.get("country", "Unknown Country")
            city = address.get("city") or address.get("town") or address.get("village") or address.get("suburb") or "Unknown City"
            district = address.get("county") or address.get("district") or address.get("state_district") or city
            state = address.get("state", "Unknown State")
            postcode = address.get("postcode", "Unknown PIN")
            timezone = get_timezone_for_country(country)
            
            resolved_name = f"{city}, {country}" if city != "Unknown City" else country
            return {
                "location": resolved_name,
                "country": country,
                "city": city,
                "district": district,
                "state": state,
                "postal_code": postcode,
                "timezone": timezone
            }
        except Exception as e:
            raise ValueError(f"Nominatim reverse geocode error: {e}")


class GoogleMapsGeocodingProvider(BaseGeocodingProvider):
    """
    Google Maps Platform Geocoding API implementation.
    Requires GOOGLE_API_KEY environment variable.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key

    def geocode(self, location_name: str) -> dict:
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": location_name,
            "key": self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=8)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != "OK" or not data.get("results"):
                reason = data.get("error_message") or data.get("status") or "Unknown error"
                raise ValueError(f"Google Geocoding failed: {reason}")
                
            result = data["results"][0]
            geometry = result["geometry"]["location"]
            lat = float(geometry["lat"])
            lon = float(geometry["lng"])
            
            country = "Unknown Country"
            address_components = data["results"][0].get("address_components", [])
            for component in address_components:
                if "country" in component.get("types", []):
                    country = component.get("long_name", "Unknown Country")
                    break
            
            resolved_name = result.get("formatted_address", location_name).split(",")[0]

            return {
                "location": resolved_name,
                "latitude": lat,
                "longitude": lon,
                "country": country
            }
            
        except requests.RequestException as e:
            raise ValueError(f"Google Geocoding API request error: {e}")
        except (KeyError, IndexError, TypeError, ValueError) as e:
            raise ValueError(f"Google Geocoding parser error: {e}")

    def reverse_geocode(self, lat: float, lon: float) -> dict:
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "latlng": f"{lat},{lon}",
            "key": self.api_key
        }
        try:
            response = requests.get(url, params=params, timeout=8)
            response.raise_for_status()
            data = response.json()
            if data.get("status") != "OK" or not data.get("results"):
                reason = data.get("error_message") or data.get("status") or "Unknown error"
                raise ValueError(f"Google Reverse Geocoding failed: {reason}")
            result = data["results"][0]
            country = "Unknown Country"
            city = ""
            district = ""
            state = ""
            postcode = ""
            for component in result.get("address_components", []):
                types = component.get("types", [])
                if "country" in types:
                    country = component.get("long_name", "Unknown Country")
                elif "locality" in types:
                    city = component.get("long_name", "")
                elif "administrative_area_level_2" in types:
                    district = component.get("long_name", "")
                elif "administrative_area_level_1" in types:
                    state = component.get("long_name", "")
                elif "postal_code" in types:
                    postcode = component.get("long_name", "")
            
            if not city:
                city = "Unknown City"
            if not district:
                district = city
            timezone = get_timezone_for_country(country)
            resolved_name = f"{city}, {country}" if city != "Unknown City" else country
            return {
                "location": resolved_name,
                "country": country,
                "city": city,
                "district": district,
                "state": state,
                "postal_code": postcode,
                "timezone": timezone
            }
        except Exception as e:
            raise ValueError(f"Google reverse geocode error: {e}")


def get_geocoding_provider() -> BaseGeocodingProvider:
    """
    Dependency Abstraction Factory.
    If GOOGLE_MAPS_API_KEY is present in the environment, upgrades to Google Maps Geocoding.
    Otherwise, returns the free Nominatim provider.
    """
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if api_key:
        return GoogleMapsGeocodingProvider(api_key)
    return NominatimGeocodingProvider()
