import os
import asyncio
from google.adk import Agent, Workflow
from google.adk.workflow import START

# Import the core engine functions/agents
from Tools.weather_tool import get_weather
from Tools.news_tool import get_disaster_news
from Agents.location_agent import LocationAgent
from Agents.resource_agent import ResourceAgent
from Agents.risk_agent import RiskAgent
from Agents.emergency_planner import EmergencyPlanner

# 1. Define the Python helper functions to register as ADK Tools
def location_tool(location_name: str) -> dict:
    """
    Resolves a human-readable location name into geographic latitude, longitude, and country.
    """
    agent = LocationAgent()
    return agent.analyze(location_name)

def weather_tool(latitude: float, longitude: float) -> dict:
    """
    Retrieves current weather details (temperature, humidity, wind speed, precipitation) 
    for the specified coordinates.
    """
    return get_weather(latitude, longitude)

def news_tool(location: str) -> dict:
    """
    Retrieves recent disaster-related news articles and counts for a specific location.
    """
    return get_disaster_news(location)

def resource_tool(location: str, latitude: float, longitude: float) -> dict:
    """
    Finds real-world emergency infrastructure (hospitals, shelters, fire stations) 
    in a 10km radius using OpenStreetMap data.
    """
    agent = ResourceAgent()
    return agent.analyze(location, latitude, longitude)

def risk_tool(weather_data: dict, news_data: dict) -> dict:
    """
    Evaluates weather factors and news article volume to calculate a risk score (0-10) 
    and classifies severity (LOW, MEDIUM, HIGH).
    """
    agent = RiskAgent()
    return agent.analyze(weather_data, news_data)

def plan_tool(risk_data: dict) -> list:
    """
    Generates recommended action lists for emergency responders based on the risk score and severity.
    """
    planner = EmergencyPlanner()
    return planner.generate_plan(risk_data)


# 2. Get LLM Model Config from environment (Default to gemini-2.5-flash for Vertex/GenAI SDK)
model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


# 3. Define the 6 Google ADK Agents
location_agent = Agent(
    name="location_agent",
    description="Resolves textual place names into standard latitude/longitude coordinates.",
    model=model_name,
    instruction="Given a text location, call the location_tool to retrieve resolved coordinates.",
    tools=[location_tool],
    mode="single_turn"
)

weather_agent = Agent(
    name="weather_agent",
    description="Queries and parses environmental metrics (temperature, wind, precipitation).",
    model=model_name,
    instruction="Given coordinates (latitude, longitude), call the weather_tool to retrieve raw weather data and summarize it.",
    tools=[weather_tool],
    mode="single_turn"
)

news_agent = Agent(
    name="news_agent",
    description="Analyzes local media articles for ongoing natural disasters.",
    model=model_name,
    instruction="Given a location, call the news_tool to retrieve recent headlines, count articles, and summarize key hazards.",
    tools=[news_tool],
    mode="single_turn"
)

resource_agent = Agent(
    name="resource_agent",
    description="Discovers active hospitals, fire stations, and emergency shelters nearby.",
    model=model_name,
    instruction="Given a location name and its latitude/longitude, call the resource_tool to fetch coordinates of active emergency services.",
    tools=[resource_tool],
    mode="single_turn"
)

risk_agent = Agent(
    name="risk_agent",
    description="Applies heuristics to formulate the risk threat level.",
    model=model_name,
    instruction="Given weather summaries and news article data, run the risk_tool to calculate the risk score and severity.",
    tools=[risk_tool],
    mode="single_turn"
)

emergency_planner_agent = Agent(
    name="emergency_planner_agent",
    description="Generates actionable steps and safety protocols for responders.",
    model=model_name,
    instruction="Given a risk assessment (severity level), call the plan_tool to get the list of emergency actions.",
    tools=[plan_tool],
    mode="single_turn"
)

# Coordinator Agent coordinates and aggregates reports
coordinator_agent = Agent(
    name="coordinator_agent",
    description="Aggregates and compiles the final disaster intelligence report.",
    model=model_name,
    instruction=(
        "You are the main incident commander. Analyze inputs, dispatch sub-agents (location, weather, news, resources, risk, planning) "
        "or combine their outputs to build the final CRISISNET AI DISASTER REPORT."
    ),
    sub_agents=[location_agent, weather_agent, news_agent, resource_agent, risk_agent, emergency_planner_agent]
)


# 4. Orchestrate using ADK Graph Workflow (ADK 2.0 feature)
disaster_workflow = Workflow(
    name="crisisnet_disaster_workflow",
    description="Chains the disaster assessment steps in sequence.",
    edges=[
        (START, location_agent),
        (location_agent, weather_agent),
        (weather_agent, news_agent),
        (news_agent, resource_agent),
        (resource_agent, risk_agent),
        (risk_agent, emergency_planner_agent),
        (emergency_planner_agent, coordinator_agent)
    ]
)
