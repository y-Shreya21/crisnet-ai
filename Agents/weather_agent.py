import sys
from Tools.weather_tool import get_weather, WeatherToolError

class WeatherAgent:

    def analyze(self, latitude, longitude):
        """
        Analyzes the weather for the given coordinates.
        If the Weather API call fails, returns a safe fallback weather profile.
        """
        try:
            weather = get_weather(latitude, longitude)
            current = weather.get("current", {})
            
            if not current:
                raise WeatherToolError("No current weather data found in response.")

            return {
                "temperature": current.get("temperature_2m", 20.0),
                "humidity": current.get("relative_humidity_2m", 50),
                "precipitation": current.get("precipitation", 0.0),
                "wind_speed": current.get("wind_speed_10m", 10.0),
                "is_fallback": False
            }
            
        except WeatherToolError as e:
            # Print warning to stderr or stdout
            print(f"⚠️ Warning (WeatherAgent): {e}. Using fallback safe weather profile.", file=sys.stderr)
            return {
                "temperature": 20.0,
                "humidity": 50,
                "precipitation": 0.0,
                "wind_speed": 10.0,
                "is_fallback": True,
                "error_message": str(e)
            }