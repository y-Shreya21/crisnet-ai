import os
import requests

class NewsToolError(Exception):
    """Exception raised for errors in the News API tool."""
    pass

API_KEY = os.getenv("NEWS_API_KEY", "e5de58fcd7614443ab5365a0c13eb20b")

def get_disaster_news(location: str) -> dict:
    """
    Fetches latest disaster-related news articles matching disaster keywords and target location.
    Raises NewsToolError on failure.
    """
    url = "https://newsapi.org/v2/everything"

    # Strict search query targeting disaster scenarios in combination with the location
    query = f"(flood OR cyclone OR earthquake OR landslide OR wildfire OR evacuation OR relief OR hurricane OR typhoon OR storm) AND \"{location}\""

    params = {
        "q": query,
        "language": "en",
        "sortBy": "relevance",
        "pageSize": 15,  # Fetch slightly larger set to filter down in the NewsAgent
        "apiKey": API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if isinstance(data, dict) and data.get("status") == "error":
            message = data.get("message", "Unknown News API error")
            code = data.get("code", "unknown_code")
            raise NewsToolError(f"News API error ({code}): {message}")
            
        response.raise_for_status()
        return data
        
    except requests.RequestException as e:
        raise NewsToolError(f"Network error while connecting to News API: {e}")
    except ValueError as e:
        raise NewsToolError(f"Invalid JSON response from News API: {e}")