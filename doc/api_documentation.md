# 📖 CrisisNet AI - API & MCP Tool Reference

This document provides a comprehensive reference of all tools, API connections, validation schemas, and the Model Context Protocol (FastMCP) server specifications.

---

## ⚡ Model Context Protocol (MCP) Server

CrisisNet AI registers its core capabilities as MCP tools, allowing third-party LLMs, clients (e.g. Cursor, VSCode), and custom agents to access real-time disaster information securely.

The FastMCP server is defined in [mcp_server.py](file:///Users/shreyayadav/crisenet/crisnet-ai/mcp_server.py).

### Registered Tools

#### 1. `get_coordinates_tool`
* **Description:** Resolves place names (cities, districts, states, countries) into latitude and longitude coordinates.
* **Input Arguments:**
  * `location` (string, required): Place name to resolve.
* **Output Format:**
  ```json
  {
    "location": "Guwahati, Assam",
    "latitude": 26.1445,
    "longitude": 91.7362,
    "country": "India"
  }
  ```

#### 2. `get_weather_tool`
* **Description:** Fetches current temperature, humidity, wind speed, and precipitation levels for a coordinate point.
* **Input Arguments:**
  * `latitude` (float, required): Latitude of target location.
  * `longitude` (float, required): Longitude of target location.
* **Output Format:**
  ```json
  {
    "temperature": 29.5,
    "humidity": 88.0,
    "precipitation": 4.5,
    "wind_speed": 12.2,
    "is_fallback": false
  }
  ```

#### 3. `get_disaster_news_tool`
* **Description:** Queries live disaster-related news headlines matching the specified location name.
* **Input Arguments:**
  * `location` (string, required): Location query string.
* **Output Format:**
  ```json
  {
    "articles": [
      {
        "title": "Severe Flood Alert Issued for Guwahati Metro Area",
        "source": "The Times of India",
        "date": "2026-07-04",
        "url": "https://timesofindia.indiatimes.com/floods-guwahati"
      }
    ],
    "article_count": 1
  }
  ```

#### 4. `get_emergency_resources_tool`
* **Description:** Queries OpenStreetMap (OSM) via the Overpass API for emergency facilities (hospitals, shelters, police, relief centers) within a 25km radius.
* **Input Arguments:**
  * `latitude` (float, required): Latitude of target center.
  * `longitude` (float, required): Longitude of target center.
* **Output Format:**
  ```json
  {
    "hospital_count": 8,
    "shelter_count": 3,
    "fire_station_count": 2,
    "police_count": 4,
    "relief_center_count": 5,
    "resources": [
      {
        "name": "Guwahati Medical College & Hospital",
        "type": "hospital",
        "lat": 26.1554,
        "lon": 91.7820,
        "address": "Bhangagarh, Guwahati"
      }
    ]
  }
  ```

---

## 🔒 Input & Output Validation Schemas

To maintain structural integrity, all agent communications are validated against rigorous schemas implemented in [validator.py](file:///Users/shreyayadav/crisenet/crisnet-ai/Security/validator.py).

### Coordinate Limits Checks
Coordinates must satisfy the following bounds:
- **Latitude:** \([-90.0, 90.0]\)
- **Longitude:** \([-180.0, 180.0]\)

### Output Validation Specs
The final compiled disaster report must match the following dictionary structure:
```json
{
  "resolved_location": {
    "name": "string",
    "latitude": "float",
    "longitude": "float",
    "country": "string",
    "is_fallback": "bool"
  },
  "weather": {
    "temperature": "float",
    "humidity": "int/float",
    "precipitation": "float",
    "wind_speed": "float",
    "is_fallback": "bool"
  },
  "news": {
    "location": "string",
    "headlines": ["string"],
    "articles": [
      {
        "title": "string",
        "source": "string",
        "date": "string",
        "url": "string"
      }
    ],
    "article_count": "int"
  },
  "resources": {
    "hospital_count": "int",
    "shelter_count": "int",
    "fire_station_count": "int",
    "police_count": "int",
    "relief_center_count": "int",
    "resources": [
      {
        "name": "string",
        "type": "string",
        "lat": "float",
        "lon": "float",
        "address": "string"
      }
    ]
  },
  "risk": {
    "risk_score": "float",
    "severity": "string (LOW / MEDIUM / HIGH / CRITICAL)",
    "reasoning": "string"
  },
  "plan": ["string"]
}
```
If any agent response fails to match this schema type, an exception is thrown, preventing downstream tool pollution or crashing.
