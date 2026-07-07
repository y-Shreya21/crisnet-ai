import os
import requests
import xml.etree.ElementTree as ET
import urllib.parse
from Tools.retry_helper import execute_with_retry

class NewsToolError(Exception):
    """Exception raised for errors in the News API tool."""
    pass

def get_disaster_news(location: str) -> dict:
    """
    Fetches latest disaster-related news articles matching disaster keywords and target location.
    Queries the public Google News RSS endpoint for real-time search indexing.
    No API keys required, bypasses rate limits.
    """
    # Strict search query targeting disaster scenarios in combination with the location
    query = f"(flood OR cyclone OR earthquake OR landslide OR wildfire OR evacuation OR relief OR disaster) AND \"{location}\""
    encoded_query = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    def _fetch():
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        return res

    try:
        response = execute_with_retry(_fetch, retries=3, initial_delay=1.0)
        
        # Parse XML tree
        root = ET.fromstring(response.content)
        articles = []
        
        for item in root.findall(".//item")[:15]:
            title = item.find("title").text if item.find("title") is not None else ""
            link = item.find("link").text if item.find("link") is not None else "#"
            pub_date = item.find("pubDate").text if item.find("pubDate") is not None else "Recent"
            source_el = item.find("source")
            source = source_el.text if source_el is not None else "Google News"
            
            # Format to match NewsAPI schema for compatibility with NewsAgent
            articles.append({
                "title": title,
                "source": {"name": source},
                "publishedAt": pub_date,
                "url": link
            })
            
        return {
            "status": "ok",
            "articles": articles,
            "totalResults": len(articles)
        }
        
    except requests.RequestException as e:
        raise NewsToolError(f"Network error while connecting to News RSS Feed: {e}")
    except ET.ParseError as e:
        raise NewsToolError(f"Failed to parse XML response from News RSS Feed: {e}")
    except Exception as e:
        raise NewsToolError(f"News RSS Feed processing error: {e}")