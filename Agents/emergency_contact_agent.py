import math
import sys

class EmergencyContactAgent:
    """
    Emergency Contact Agent identifies relevant emergency numbers, 
    disaster-specific dispatch lines, and computes the geodetic distance 
    to the closest mapped healthcare facility using the Haversine formula.
    """

    def haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculates distance between two coordinate pairs in kilometers."""
        # Earth radius in km
        R = 6371.0
        
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_phi / 2.0) ** 2 +
             math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda / 2.0) ** 2))
        
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return R * c

    def identify_contacts(self, location_name: str, latitude: float, longitude: float, resources: list) -> dict:
        """
        Returns localized contacts and evaluates the nearest hospital from the resources payload.
        """
        loc_lower = location_name.lower()
        is_india = "india" in loc_lower or any(state in loc_lower for state in [
            "assam", "guwahati", "delhi", "mumbai", "bihar", "odisha", "kerala", "kolkata",
            "chennai", "bangalore", "hyderabad", "gujarat", "rajasthan", "punjab"
        ])

        # Localized contacts dictionary
        if is_india:
            contacts = {
                "police": "112 / 100",
                "ambulance": "102 / 108",
                "fire": "101",
                "disaster_management": "1078 (National Disaster Helpline)",
                "specialist_authority": "NDRF National Rescue Force (011-23438084)"
            }
        else:
            contacts = {
                "police": "911",
                "ambulance": "911",
                "fire": "911",
                "disaster_management": "Emergency Management Agency / Red Cross",
                "specialist_authority": "National Operations Command Center"
            }

        # Scan for closest hospital using Haversine
        nearest_hospital = None
        min_distance = float('inf')

        hospitals = [res for res in resources if res.get("type") == "hospital"]

        for hosp in hospitals:
            h_lat = hosp.get("lat")
            h_lon = hosp.get("lon")
            if h_lat is not None and h_lon is not None:
                dist = self.haversine_distance(latitude, longitude, h_lat, h_lon)
                if dist < min_distance:
                    min_distance = dist
                    nearest_hospital = hosp

        if nearest_hospital:
            contacts["nearest_hospital"] = {
                "name": nearest_hospital.get("name", "Local Health Facility"),
                "distance_km": round(min_distance, 2),
                "address": nearest_hospital.get("address", "Emergency Clinic Area"),
                "lat": nearest_hospital.get("lat"),
                "lon": nearest_hospital.get("lon")
            }
        else:
            # Fallback estimation if no hospital was discovered in OSM Overpass radius
            contacts["nearest_hospital"] = {
                "name": "District General Hospital (Fallback)",
                "distance_km": 15.0,
                "address": "State Capital Main Road",
                "lat": latitude + 0.1,
                "lon": longitude + 0.1
            }

        return contacts
