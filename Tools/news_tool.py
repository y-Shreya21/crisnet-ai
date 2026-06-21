import requests

API_KEY = "e5de58fcd7614443ab5365a0c13eb20b"

def get_disaster_news(location):

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": f"flood OR cyclone OR earthquake OR wildfire {location}",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)

    return response.json()