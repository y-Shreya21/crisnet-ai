import os
import asyncio
from Agents.location_agent import LocationAgent
from Agents.weather_agent import WeatherAgent
from Agents.news_agent import NewsAgent
from Agents.risk_agent import RiskAgent
from Agents.emergency_planner import EmergencyPlanner
from Agents.resource_agent import ResourceAgent
from Agents.emergency_contact_agent import EmergencyContactAgent
from Agents.citizen_safety_agent import CitizenSafetyAgent
from Agents.alert_agent import AlertAgent
from Agents.language_agent import LanguageAgent
from Security.validator import validate_input, validate_output
from Security.prompt_guard import sanitize_input

# Import ADK modules if the user runs the live ADK workflow
try:
    from google.adk import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai import types
    from Agents.adk_agents import coordinator_agent
    ADK_AVAILABLE = True
except ImportError:
    ADK_AVAILABLE = False

class CoordinatorAgent:
    """
    Coordinator Agent that manages input sanitization, input validation,
    agent execution, output aggregation, and final report verification.
    """

    def process(self, location: str, latitude: float = None, longitude: float = None, target_language: str = "en") -> dict:
        """
        Executes the rule-based heuristic flow of agents synchronously.
        Resolves text location to coordinates via LocationAgent if not provided explicitly.
        """
        # 1. Input sanitization (Prompt injection and shell command check)
        sanitized_location = sanitize_input(location)

        # 2. Coordinate resolution via LocationAgent (Phase 0)
        if latitude is None or longitude is None:
            loc_agent = LocationAgent()
            loc_result = loc_agent.analyze(sanitized_location)
            latitude = loc_result["latitude"]
            longitude = loc_result["longitude"]
            resolved_location = loc_result["location"]
            country = loc_result["country"]
            is_fallback_loc = loc_result.get("is_fallback", False)
        else:
            resolved_location = sanitized_location
            country = "Unknown Country"
            is_fallback_loc = False

        # 3. Input validation (Type and coordinate boundary checks)
        validate_input(resolved_location, latitude, longitude)

        # 4. Weather Agent Analysis
        weather = WeatherAgent().analyze(latitude, longitude)

        # 5. News Agent Analysis
        news = NewsAgent().analyze(resolved_location)

        # 6. Resource Agent Analysis (OSM Integration using resolved coordinates)
        resources = ResourceAgent().analyze(resolved_location, latitude, longitude)

        # 7. Risk Agent Analysis
        risk = RiskAgent().analyze(weather, news)

        # 8. Plan Generation
        plan = EmergencyPlanner().generate_plan(risk)

        # 9. Dynamic Disaster Type Detection
        disaster_type = "Flood"  # Default
        news_headlines_lower = " ".join(news.get("headlines", [])).lower()
        if "earthquake" in news_headlines_lower or "quake" in news_headlines_lower:
            disaster_type = "Earthquake"
        elif any(w in news_headlines_lower for w in ["cyclone", "hurricane", "typhoon", "storm"]):
            disaster_type = "Cyclone"
        elif any(w in news_headlines_lower for w in ["wildfire", "bushfire", "forest fire"]):
            disaster_type = "Wildfire"
        elif any(w in news_headlines_lower for w in ["landslide", "mudslide"]):
            disaster_type = "Landslide"
        elif weather.get("precipitation", 0.0) > 10.0:
            disaster_type = "Flood"
        elif weather.get("wind_speed", 0.0) > 25.0:
            disaster_type = "Cyclone"

        # 10. Emergency Alert Generation
        alert = AlertAgent().generate_alert(risk["risk_score"], risk["severity"], disaster_type)

        # 11. Emergency Contact Mapping (includes nearest hospital Haversine resolution)
        emergency_contacts = EmergencyContactAgent().identify_contacts(
            resolved_location, latitude, longitude, resources.get("resources", [])
        )

        # 12. Citizen Safety Instructions Generation
        safety_guidance = CitizenSafetyAgent().generate_guidance(disaster_type)

        result = {
            "resolved_location": {
                "name": resolved_location,
                "latitude": latitude,
                "longitude": longitude,
                "country": country,
                "is_fallback": is_fallback_loc
            },
            "weather": weather,
            "news": news,
            "resources": resources,
            "risk": risk,
            "plan": plan,
            "alert": alert,
            "emergency_contacts": emergency_contacts,
            "safety_guidance": safety_guidance
        }

        # 13. Output validation
        validate_output(result)

        # 14. Multilingual Translation
        if target_language and target_language != "en":
            result = LanguageAgent().translate_report(result, target_language)

        return result

    async def process_adk(self, location: str, latitude: float = None, longitude: float = None) -> str:
        """
        Executes the orchestrator using Google ADK Runner (LLM-based multi-agent flow).
        Requires GOOGLE_API_KEY environment variable.
        Falls back gracefully with a flag if it fails or if ADK is unavailable.
        """
        if not ADK_AVAILABLE:
            return "⚠️ ADK unavailable: Google ADK libraries are not configured correctly. Switching to Local Multi-Agent Workflow."

        if not os.getenv("GOOGLE_API_KEY"):
            return "⚠️ ADK unavailable: GOOGLE_API_KEY environment variable is missing. Switching to Local Multi-Agent Workflow."

        try:
            # Ensure coordinates are resolved first
            if latitude is None or longitude is None:
                loc_res = LocationAgent().analyze(location)
                latitude = loc_res["latitude"]
                longitude = loc_res["longitude"]

            session_service = InMemorySessionService()
            runner = Runner(
                agent=coordinator_agent,
                app_name="CrisisNetAI",
                session_service=session_service
            )

            prompt = f"Analyze disaster threat in {location} at Coordinates: Lat {latitude}, Lon {longitude}."
            user_message = types.Content(
                role="user",
                parts=[types.Part(text=prompt)]
            )

            output_text = ""
            for attempt in range(4):
                try:
                    session_id = f"session_{location.lower().replace(' ', '_')}_{attempt}"
                    await session_service.create_session(
                        app_name="CrisisNetAI",
                        user_id="incident_commander",
                        session_id=session_id
                    )

                    output_text = ""
                    async for event in runner.run_async(
                        user_id="incident_commander",
                        session_id=session_id,
                        new_message=user_message
                    ):
                        if hasattr(event, "content") and event.content:
                            output_text += str(event.content)
                        elif hasattr(event, "text") and event.text:
                            output_text += str(event.text)
                    
                    if output_text:
                        break
                except Exception as e:
                    if ("429" in str(e) or "RESOURCE_EXHAUSTED" in str(e)) and attempt < 3:
                        import sys
                        print(f"⚠️ ADK hit 429 rate limit. Retrying attempt {attempt+1} in 25 seconds...", file=sys.stderr)
                        await asyncio.sleep(25)
                    else:
                        raise

            return output_text if output_text else "No output generated by ADK agents."
        except Exception as e:
            import sys
            print(f"⚠️ ADK Workflow failure: {e}", file=sys.stderr)
            return f"⚠️ ADK unavailable: {e}. Switching to Local Multi-Agent Workflow."
