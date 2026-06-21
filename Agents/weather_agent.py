from Tools.weather_tool import get_weather

class WeatherAgent:

    def analyze(self, latitude, longitude):

        weather = get_weather(latitude, longitude)

        current = weather["current"]

        return {
            "temperature": current["temperature_2m"],
            "humidity": current["relative_humidity_2m"],
            "precipitation": current["precipitation"],
            "wind_speed": current["wind_speed_10m"]
        }