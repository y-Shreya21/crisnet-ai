import re
from typing import Any

def validate_input(location: str, latitude: float, longitude: float) -> None:
    """
    Comprehensive input validation for coordinates and location parameters.
    Checks data types, range bounds, and identifies suspicious input characteristics.
    Raises TypeError or ValueError on validation failure.
    """
    # 1. Location Validation
    if not isinstance(location, str):
        raise TypeError(f"Location must be a string. Given type: {type(location).__name__}")
    
    location_stripped = location.strip()
    if not location_stripped:
        raise ValueError("Location must not be empty or whitespace-only.")
    
    if len(location_stripped) > 100:
        raise ValueError(f"Location string exceeds maximum allowed limit (100 characters). Length: {len(location_stripped)}")

    # Reject standard SQL/script special characters in the location input string
    dangerous_chars = r"[;<>\n\r\"'\\]"
    if re.search(dangerous_chars, location_stripped):
        raise ValueError("Location contains dangerous characters suggesting command or SQL injection.")

    # 2. Coordinates Validation
    if not isinstance(latitude, (int, float)):
        raise TypeError(f"Latitude must be a float or integer. Given type: {type(latitude).__name__}")
    if not (-90.0 <= latitude <= 90.0):
        raise ValueError(f"Latitude must be between -90.0 and 90.0 degrees. Given: {latitude}")

    if not isinstance(longitude, (int, float)):
        raise TypeError(f"Longitude must be a float or integer. Given type: {type(longitude).__name__}")
    if not (-180.0 <= longitude <= 180.0):
        raise ValueError(f"Longitude must be between -180.0 and 180.0 degrees. Given: {longitude}")


def validate_output(result: dict) -> None:
    """
    Verifies structural and semantic integrity of the final multi-agent assessment report.
    Raises ValueError or TypeError on structural validation failure.
    """
    if not isinstance(result, dict):
        raise TypeError(f"Workflow result must be a dictionary. Given type: {type(result).__name__}")

    required_keys = ["weather", "news", "resources", "risk", "plan", "alert", "emergency_contacts", "safety_guidance"]
    for key in required_keys:
        if key not in result:
            raise ValueError(f"Workflow response is missing critical component: '{key}'")

    # Validate Weather Structure
    weather = result["weather"]
    if not isinstance(weather, dict):
        raise TypeError("Weather component must be a dictionary.")
    for k in ["temperature", "humidity", "precipitation", "wind_speed"]:
        if k not in weather:
            raise ValueError(f"Weather component is missing sub-key: '{k}'")
        if not isinstance(weather[k], (int, float)):
            raise TypeError(f"Weather sub-key '{k}' must be a number.")

    # Validate News Structure
    news = result["news"]
    if not isinstance(news, dict):
        raise TypeError("News component must be a dictionary.")
    if "article_count" not in news or not isinstance(news["article_count"], int):
        raise ValueError("News component must contain an integer 'article_count'.")
    if "headlines" not in news or not isinstance(news["headlines"], list):
        raise ValueError("News component must contain a list of 'headlines'.")
    if "articles" not in news or not isinstance(news["articles"], list):
        raise ValueError("News component must contain a list of 'articles'.")

    # Validate Resources Structure
    resources = result["resources"]
    if not isinstance(resources, dict):
        raise TypeError("Resources component must be a dictionary.")
    for k in ["hospital_count", "shelter_count", "fire_station_count", "police_count", "relief_center_count", "resources"]:
        if k not in resources:
            raise ValueError(f"Resources component is missing sub-key: '{k}'")
    if not isinstance(resources["resources"], list):
        raise TypeError("Resources element list must be a list.")

    # Validate Risk Structure
    risk = result["risk"]
    if not isinstance(risk, dict):
        raise TypeError("Risk component must be a dictionary.")
    if "risk_score" not in risk or not isinstance(risk["risk_score"], (int, float)):
        raise ValueError("Risk component must contain a numerical 'risk_score'.")
    if "severity" not in risk or risk["severity"] not in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]:
        raise ValueError("Risk component must contain a 'severity' classified as LOW, MEDIUM, HIGH, or CRITICAL.")

    # Validate Plan Structure
    plan = result["plan"]
    if not isinstance(plan, list):
        raise TypeError("Plan component must be a list of action items.")
    if not all(isinstance(item, str) for item in plan):
        raise TypeError("Plan component must contain only string recommendations.")

    # Validate Alert Structure
    alert = result["alert"]
    if not isinstance(alert, dict):
        raise TypeError("Alert component must be a dictionary.")
    for k in ["level", "color", "headline", "message"]:
        if k not in alert:
            raise ValueError(f"Alert component is missing sub-key: '{k}'")

    # Validate Emergency Contacts Structure
    contacts = result["emergency_contacts"]
    if not isinstance(contacts, dict):
        raise TypeError("Emergency contacts component must be a dictionary.")
    for k in ["police", "ambulance", "fire", "nearest_hospital"]:
        if k not in contacts:
            raise ValueError(f"Emergency contacts is missing sub-key: '{k}'")

    # Validate Safety Guidance Structure
    guidance = result["safety_guidance"]
    if not isinstance(guidance, dict):
        raise TypeError("Safety guidance component must be a dictionary.")
    for k in ["type", "immediate_actions", "evacuation_instructions"]:
        if k not in guidance:
            raise ValueError(f"Safety guidance is missing sub-key: '{k}'")

