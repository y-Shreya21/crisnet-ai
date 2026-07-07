import sys
import os

# Ensure the root of the project is in python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastmcp import FastMCP
from Tools.weather_tool import get_weather
from Tools.news_tool import get_disaster_news
from Agents.resource_agent import ResourceAgent

# Create FastMCP instance
mcp = FastMCP(
    "CrisisNet AI",
    dependencies=["requests", "pydantic"]
)


@mcp.tool()
def location_tool(location_name: str) -> str:
    """
    Converts a human-readable place name (city, district, state, country)
    into standardized coordinates (latitude, longitude, and country) via Nominatim geocoding.
    """
    try:
        from Agents.location_agent import LocationAgent
        agent = LocationAgent()
        result = agent.analyze(location_name)
        status = " (⚠️ Loaded Fallback coordinates due to API offline)" if result.get("is_fallback") else ""
        return (
            f"📍 Resolved location details for '{location_name}'{status}:\n"
            f"- Standardized Place: {result.get('location')}\n"
            f"- Country: {result.get('country')}\n"
            f"- Latitude: {result.get('latitude')}\n"
            f"- Longitude: {result.get('longitude')}"
        )
    except Exception as e:
        return f"Error resolving location coordinates: {e}"


@mcp.tool()
def weather_tool(latitude: float, longitude: float) -> str:
    """
    Fetches the current weather metrics (temperature, humidity, precipitation, wind speed)
    for the specified latitude and longitude coordinates.
    """
    try:
        data = get_weather(latitude, longitude)
        current = data.get("current", {})
        if not current:
            return "No weather data found for these coordinates."
        
        return (
            f"🌦️ Weather at ({latitude}, {longitude}):\n"
            f"- Temperature: {current.get('temperature_2m')}°C\n"
            f"- Relative Humidity: {current.get('relative_humidity_2m')}%\n"
            f"- Precipitation: {current.get('precipitation')} mm\n"
            f"- Wind Speed: {current.get('wind_speed_10m')} m/s"
        )
    except Exception as e:
        return f"Error retrieving weather metrics: {e}"


@mcp.tool()
def news_tool(location: str) -> str:
    """
    Fetches the latest disaster-related news headlines (floods, cyclones, earthquakes, wildfires)
    for the specified location.
    """
    try:
        from Agents.news_agent import NewsAgent
        agent = NewsAgent()
        result = agent.analyze(location)
        headlines = result.get("headlines", [])
        if not headlines:
            return f"No recent verified disaster news headlines found for location: {location}"

        formatted_headlines = [f"- {title}" for title in headlines]
        return f"📰 News headlines for {location}:\n" + "\n".join(formatted_headlines)
    except Exception as e:
        return f"Error retrieving news headlines: {e}"


@mcp.tool()
def maps_tool(location: str, latitude: float, longitude: float) -> str:
    """
    Finds real-world emergency infrastructure (hospitals, shelters, fire stations, police stations, relief centers)
    within a 25km radius of the given coordinates using OpenStreetMap's Overpass API.
    """
    try:
        agent = ResourceAgent()
        result = agent.analyze(location, latitude, longitude)
        
        output = [
            f"📋 Emergency resources mapped near {location} ({latitude}, {longitude}) within 25km:",
            f"- Hospitals: {result['hospital_count']}",
            f"- Shelters: {result['shelter_count']}",
            f"- Fire stations: {result['fire_station_count']}",
            f"- Police stations: {result['police_count']}",
            f"- Relief centers: {result['relief_center_count']}\n",
            "Discovered Facilities:"
        ]
        
        for idx, res in enumerate(result.get("resources", []), 1):
            output.append(f"{idx}. {res['name']} ({res['type'].replace('_', ' ').title()})")
            output.append(f"   Coordinates: ({res['lat']}, {res['lon']})")
            output.append(f"   Address: {res['address']}")

        return "\n".join(output)
    except Exception as e:
        return f"Error mapping emergency resources: {e}"


if __name__ == "__main__":
    # Start the MCP server using standard input/output transport protocol
    mcp.run()
