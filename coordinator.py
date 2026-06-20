from Agents.weather_agent import WeatherAgent
from Agents.news_agent import NewsAgent
from Agents.resource_agent import ResourceAgent
from Agents.risk_agent import RiskAgent
from Agents.emergency_planner import EmergencyPlanner


class CoordinatorAgent:

    def process(self, location):

        weather = WeatherAgent().analyze(location)

        news = NewsAgent().analyze(location)

        resources = ResourceAgent().analyze(location)

        risk = RiskAgent().analyze(
            weather,
            news
        )

        report = EmergencyPlanner().generate_plan(
            weather,
            news,
            resources,
            risk
        )

        return report