import requests
import os

def geocode_location(location_name: str) -> tuple[float, float, str]:
    """
    Geocodes a textual location name to (latitude, longitude, formatted_address).
    Attempts to use Google Maps Geocoding API if GOOGLE_API_KEY is available.
    Falls back to OpenStreetMap Nominatim API if the Google call is unavailable or fails.
    Raises ValueError if geocoding fails to resolve the location.
    """
    if not isinstance(location_name, str) or not location_name.strip():
        raise ValueError("Invalid location name provided for geocoding.")

    # 1. Attempt Google Maps Geocoding API
    google_key = os.getenv("GOOGLE_API_KEY")
    if google_key:
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": location_name,
            "key": google_key
        }
        try:
            response = requests.get(url, params=params, timeout=8)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "OK" and data.get("results"):
                    result = data["results"][0]
                    geometry = result["geometry"]["location"]
                    lat = float(geometry["lat"])
                    lon = float(geometry["lng"])
                    address = result.get("formatted_address", location_name)
                    return lat, lon, address
        except Exception:
            # Silently pass to fallback on any exception
            pass

    # 2. Fallback to OpenStreetMap Nominatim API (Free, no credentials required)
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location_name,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "CrisisNetAI/1.0 (contact@crisisnet.ai; Kaggle Capstone Submission)"
    }
    try:
        response = requests.get(url, params=params, headers=headers, timeout=8)
        if response.status_code == 200:
            data = response.json()
            if data:
                lat = float(data[0]["lat"])
                lon = float(data[0]["lon"])
                address = data[0].get("display_name", location_name)
                return lat, lon, address
    except Exception as e:
        raise ValueError(f"Geocoding services are currently offline: {e}")

    raise ValueError(f"Could not resolve coordinates for location: '{location_name}'. Please enter coordinates manually.")
