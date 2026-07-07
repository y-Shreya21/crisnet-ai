import os
import asyncio
import time
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
    concurrent agent execution, output aggregation, and final report verification.
    """

    def process(self, location: str, latitude: float = None, longitude: float = None, target_language: str = "en") -> dict:
        """
        Synchronous wrapper that executes the asynchronous pipeline.
        Defensively handles existing running event loops in web servers.
        """
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            import nest_asyncio
            nest_asyncio.apply()
            return loop.run_until_complete(
                self.process_async(location, latitude, longitude, target_language)
            )
        else:
            return asyncio.run(
                self.process_async(location, latitude, longitude, target_language)
            )

    async def process_async(self, location: str, latitude: float = None, longitude: float = None, target_language: str = "en") -> dict:
        """
        Asynchronously orchestrates multi-agent tasks concurrently.
        Logs latency metrics for execution profiling.
        """
        t_start = time.time()

        # 1. Input sanitization (Prompt injection and shell command check)
        sanitized_location = sanitize_input(location)

        # 2. Coordinate resolution via LocationAgent (Phase 0)
        t_loc_start = time.time()
        if latitude is None or longitude is None:
            loc_agent = LocationAgent()
            loc_result = await asyncio.to_thread(loc_agent.analyze, sanitized_location)
            latitude = loc_result["latitude"]
            longitude = loc_result["longitude"]
            resolved_location = loc_result["location"]
            country = loc_result["country"]
            is_fallback_loc = loc_result.get("is_fallback", False)
        else:
            resolved_location = sanitized_location
            country = "Unknown Country"
            is_fallback_loc = False
        t_loc = time.time() - t_loc_start

        # 3. Input validation (Type and coordinate boundary checks)
        validate_input(resolved_location, latitude, longitude)

        # 4. Concurrently run independent Stage 1 agents: Weather, News, Resource
        async def run_weather():
            t0 = time.time()
            res = await asyncio.to_thread(WeatherAgent().analyze, latitude, longitude)
            return res, time.time() - t0

        async def run_news():
            t0 = time.time()
            res = await asyncio.to_thread(NewsAgent().analyze, resolved_location)
            return res, time.time() - t0

        async def run_resources():
            t0 = time.time()
            res = await asyncio.to_thread(ResourceAgent().analyze, resolved_location, latitude, longitude)
            return res, time.time() - t0

        weather_task = run_weather()
        news_task = run_news()
        resources_task = run_resources()

        (weather, t_weather), (news, t_news), (resources, t_resources) = await asyncio.gather(
            weather_task, news_task, resources_task
        )

        # 5. Risk Agent Analysis (depends on weather & news)
        t_risk_start = time.time()
        risk = await asyncio.to_thread(RiskAgent().analyze, weather, news)
        t_risk = time.time() - t_risk_start

        # 6. Dynamic Disaster Type Detection
        disaster_type = "Flood"  # Default fallback
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

        # 7. Concurrently run independent Stage 2 agents: Planner, Alert, Contacts, Safety
        async def run_planner():
            t0 = time.time()
            res = await asyncio.to_thread(EmergencyPlanner().generate_plan, risk)
            return res, time.time() - t0

        async def run_alert():
            t0 = time.time()
            res = await asyncio.to_thread(AlertAgent().generate_alert, risk["risk_score"], risk["severity"], disaster_type)
            return res, time.time() - t0

        async def run_contacts():
            t0 = time.time()
            res = await asyncio.to_thread(EmergencyContactAgent().identify_contacts,
                resolved_location, latitude, longitude, resources.get("resources", [])
            )
            return res, time.time() - t0

        async def run_safety():
            t0 = time.time()
            res = await asyncio.to_thread(CitizenSafetyAgent().generate_guidance, disaster_type)
            return res, time.time() - t0

        planner_task = run_planner()
        alert_task = run_alert()
        contacts_task = run_contacts()
        safety_task = run_safety()

        (plan, t_planner), (alert, t_alert), (emergency_contacts, t_contacts), (safety_guidance, t_safety) = await asyncio.gather(
            planner_task, alert_task, contacts_task, safety_task
        )

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
            "safety_guidance": safety_guidance,
            "metrics": {
                "location_time": t_loc,
                "weather_time": t_weather,
                "news_time": t_news,
                "resource_time": t_resources,
                "risk_time": t_risk,
                "planner_time": t_planner,
                "alert_time": t_alert,
                "contacts_time": t_contacts,
                "safety_time": t_safety,
                "total_time": time.time() - t_start
            }
        }

        # 8. Output validation
        validate_output(result)

        # 9. Multilingual Translation
        if target_language and target_language != "en":
            t_trans_start = time.time()
            result = await asyncio.to_thread(LanguageAgent().translate_report, result, target_language)
            result["metrics"]["translation_time"] = time.time() - t_trans_start

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
