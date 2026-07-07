import sys
import requests

class ResourceAgent:
    """
    Agent responsible for finding emergency resources (hospitals, shelters,
    fire stations, police stations, and relief centers)
    using real-time OpenStreetMap data via the Overpass API.
    """

    def analyze(self, location: str, latitude: float = None, longitude: float = None) -> dict:
        """
        Queries OpenStreetMap's Overpass API around the given coordinates (10km radius)
        to discover emergency services. Falls back to realistic mock values on error.
        """
        # If coordinates are missing, map defaults for known locations or use default values
        if latitude is None or longitude is None:
            if "assam" in location.lower():
                latitude, longitude = 26.1445, 91.7362
            else:
                latitude, longitude = 20.5937, 78.9629  # Default center of India

        url = "https://overpass-api.de/api/interpreter"
        query = f"""
        [out:json][timeout:15];
        (
          node["amenity"="hospital"](around:25000, {latitude}, {longitude});
          way["amenity"="hospital"](around:25000, {latitude}, {longitude});
          node["amenity"="shelter"](around:25000, {latitude}, {longitude});
          way["amenity"="shelter"](around:25000, {latitude}, {longitude});
          node["amenity"="fire_station"](around:25000, {latitude}, {longitude});
          way["amenity"="fire_station"](around:25000, {latitude}, {longitude});
          node["amenity"="police"](around:25000, {latitude}, {longitude});
          way["amenity"="police"](around:25000, {latitude}, {longitude});
          node["amenity"="social_facility"](around:25000, {latitude}, {longitude});
          way["amenity"="social_facility"](around:25000, {latitude}, {longitude});
        );
        out body center;
        """
        
        headers = {
            "User-Agent": "CrisisNetAI/1.0 (contact@crisisnet.ai; Kaggle Capstone Submission)"
        }

        def _fetch():
            res = requests.post(url, data={"data": query}, headers=headers, timeout=12)
            res.raise_for_status()
            return res

        try:
            # Query real-time Overpass API with exponential retry
            from Tools.retry_helper import execute_with_retry
            response = execute_with_retry(_fetch, retries=3, initial_delay=1.0)
            data = response.json()
            elements = data.get("elements", [])

            resources = []
            hospital_count = 0
            shelter_count = 0
            fire_station_count = 0
            police_count = 0
            relief_center_count = 0

            for el in elements:
                tags = el.get("tags", {})
                amenity = tags.get("amenity")
                name = tags.get("name", f"Unnamed {amenity.replace('_', ' ').title()}")
                
                # Fetch element coordinates (from node, or center of way)
                lat = el.get("lat") or el.get("center", {}).get("lat")
                lon = el.get("lon") or el.get("center", {}).get("lon")
                
                if not lat or not lon:
                    continue

                if amenity == "hospital":
                    hospital_count += 1
                elif amenity == "shelter":
                    shelter_count += 1
                elif amenity == "fire_station":
                    fire_station_count += 1
                elif amenity == "police":
                    police_count += 1
                elif amenity == "social_facility":
                    relief_center_count += 1

                resources.append({
                    "name": name,
                    "type": amenity,
                    "lat": lat,
                    "lon": lon,
                    "address": tags.get("addr:full") or tags.get("addr:street", "Street info unavailable")
                })

            # If the API returned nothing (e.g. sparse area), populate basic defaults
            if not resources:
                return self._get_fallback_data(location, latitude, longitude, "No resources found in radius")

            return {
                "location": location,
                "latitude": latitude,
                "longitude": longitude,
                "hospital_count": hospital_count,
                "shelter_count": shelter_count,
                "fire_station_count": fire_station_count,
                "police_count": police_count,
                "relief_center_count": relief_center_count,
                "resources": resources,
                "is_fallback": False
            }

        except (requests.RequestException, ValueError, KeyError) as e:
            print(f"⚠️ Warning (ResourceAgent): OSM query failed ({e}). Returning fallback mapping.", file=sys.stderr)
            return self._get_fallback_data(location, latitude, longitude, str(e))

    def _get_fallback_data(self, location: str, latitude: float, longitude: float, reason: str) -> dict:
        """Returns realistic fallback emergency assets in case the API is down or empty."""
        return {
            "location": location,
            "latitude": latitude,
            "longitude": longitude,
            "hospital_count": 5,
            "shelter_count": 3,
            "fire_station_count": 2,
            "police_count": 2,
            "relief_center_count": 3,
            "resources": [
                {
                    "name": f"{location} Central Red Cross Hospital",
                    "type": "hospital",
                    "lat": latitude + 0.012,
                    "lon": longitude - 0.008,
                    "address": "Main Hospital Ring Road"
                },
                {
                    "name": f"{location} City Emergency Shelter",
                    "type": "shelter",
                    "lat": latitude - 0.005,
                    "lon": longitude + 0.014,
                    "address": "Community Sports Center"
                },
                {
                    "name": f"{location} District Fire Station",
                    "type": "fire_station",
                    "lat": latitude + 0.004,
                    "lon": longitude - 0.015,
                    "address": "Station House #3"
                },
                {
                    "name": f"{location} Regional Police Headquarters",
                    "type": "police",
                    "lat": latitude + 0.008,
                    "lon": longitude + 0.007,
                    "address": "Main Boulevard"
                },
                {
                    "name": f"{location} Disaster Relief Center",
                    "type": "social_facility",
                    "lat": latitude - 0.009,
                    "lon": longitude - 0.003,
                    "address": "Civic Plaza"
                }
            ],
            "is_fallback": True,
            "error_reason": reason
        }