import sys
from Tools.location_tool import get_geocoding_provider
from Security.prompt_guard import sanitize_input

class LocationAgent:
    """
    Location Intelligence Agent.
    Converts textual location inputs into standardized geographical coordinates
    before downstream analysis begins.
    """

    def analyze(self, location_name: str) -> dict:
        """
        Resolves textual location name to geographic coordinates using
        configured provider. Falls back to realistic defaults if services fail.
        """
        # 1. Sanitize location input to prevent prompt/script injection
        sanitized_name = sanitize_input(location_name)

        # 2. Query Geocoding Service via abstraction factory
        provider = get_geocoding_provider()
        
        try:
            resolved = provider.geocode(sanitized_name)
            return {
                "location": resolved["location"],
                "latitude": resolved["latitude"],
                "longitude": resolved["longitude"],
                "country": resolved["country"],
                "is_fallback": False
            }
        except Exception as e:
            print(f"⚠️ Warning (LocationAgent): Geocoding failed ({e}). Returning fallback location.", file=sys.stderr)
            return self._get_fallback_coordinates(sanitized_name, str(e))

    def _get_fallback_coordinates(self, location_name: str, error_reason: str) -> dict:
        """Fallback coordinates dictionary for standard emergency hubs when APIs are offline."""
        loc_lower = location_name.lower()
        
        # Check for known common disaster hubs & states across India
        if "assam" in loc_lower or "guwahati" in loc_lower:
            lat, lon, country = 26.2006, 92.9376, "India"
        elif "delhi" in loc_lower:
            lat, lon, country = 28.7041, 77.1025, "India"
        elif "mumbai" in loc_lower or "maharashtra" in loc_lower:
            lat, lon, country = 19.0760, 72.8777, "India"
        elif "bihar" in loc_lower or "patna" in loc_lower:
            lat, lon, country = 25.0961, 85.3131, "India"
        elif "odisha" in loc_lower or "bhubaneswar" in loc_lower:
            lat, lon, country = 20.9517, 85.0985, "India"
        elif "kerala" in loc_lower or "kochi" in loc_lower or "thiruvananthapuram" in loc_lower:
            lat, lon, country = 10.8505, 76.2711, "India"
        elif "uttarakhand" in loc_lower or "dehradun" in loc_lower:
            lat, lon, country = 30.0668, 79.0193, "India"
        elif "himachal" in loc_lower or "shimla" in loc_lower:
            lat, lon, country = 31.1048, 77.1734, "India"
        elif "jammu" in loc_lower or "kashmir" in loc_lower or "srinagar" in loc_lower:
            lat, lon, country = 33.7782, 76.5762, "India"
        elif "kolkata" in loc_lower or "bengal" in loc_lower:
            lat, lon, country = 22.5726, 88.3639, "India"
        elif "chennai" in loc_lower or "tamil" in loc_lower:
            lat, lon, country = 13.0827, 80.2707, "India"
        elif "bangalore" in loc_lower or "bengaluru" in loc_lower or "karnataka" in loc_lower:
            lat, lon, country = 12.9716, 77.5946, "India"
        elif "hyderabad" in loc_lower or "telangana" in loc_lower:
            lat, lon, country = 17.3850, 78.4867, "India"
        elif "gujarat" in loc_lower or "ahmedabad" in loc_lower:
            lat, lon, country = 22.2587, 71.1924, "India"
        elif "rajasthan" in loc_lower or "jaipur" in loc_lower:
            lat, lon, country = 27.0238, 74.2179, "India"
        elif "punjab" in loc_lower or "ludhiana" in loc_lower or "amritsar" in loc_lower:
            lat, lon, country = 30.9293211, 75.5004841, "India"
        elif "tokyo" in loc_lower:
            lat, lon, country = 35.6762, 139.6503, "Japan"
        elif "california" in loc_lower:
            lat, lon, country = 36.7783, -119.4179, "United States"
        else:
            lat, lon, country = 20.5937, 78.9629, "India"  # General center of India fallback

        return {
            "location": location_name,
            "latitude": lat,
            "longitude": lon,
            "country": country,
            "is_fallback": True,
            "error_reason": error_reason
        }
