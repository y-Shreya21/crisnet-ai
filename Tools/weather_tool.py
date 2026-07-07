import requests
from Tools.retry_helper import execute_with_retry

class WeatherToolError(Exception):
    """Exception raised for errors in the Weather API tool."""
    pass

def get_weather(latitude, longitude):
    """
    Fetches the current weather for the given coordinates.
    Raises WeatherToolError on failure.
    """
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m"
        ]
    }

    def _fetch():
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response

    try:
        response = execute_with_retry(_fetch, retries=3, initial_delay=1.0)
        data = response.json()
        
        # Check if the API returned an error payload in standard JSON format
        if isinstance(data, dict) and data.get("error") is True:
            reason = data.get("reason", "Unknown API error")
            raise WeatherToolError(f"Weather API returned an error: {reason}")
            
        return data
        
    except requests.RequestException as e:
        raise WeatherToolError(f"Network error while connecting to Weather API: {e}")
    except ValueError as e:
        raise WeatherToolError(f"Invalid JSON response from Weather API: {e}")