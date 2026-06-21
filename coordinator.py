from Agents.weather_agent import WeatherAgent
from Agents.news_agent import NewsAgent
from Agents.risk_agent import RiskAgent

class CoordinatorAgent:

    def process(self, location, latitude, longitude):

        weather = WeatherAgent().analyze(
            latitude,
            longitude
        )

        news = NewsAgent().analyze(location)

        risk = RiskAgent().analyze(
            weather,
            news
        )

        return {
            "weather": weather,
            "news": news,
            "risk": risk
        }