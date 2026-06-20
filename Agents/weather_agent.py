class WeatherAgent:

    def analyze(self, location):
        return {
            "location": location,
            "alert": "Red Alert",
            "rainfall": "Heavy",
            "risk": "High"
        }