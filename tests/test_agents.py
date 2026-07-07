import unittest
from unittest.mock import patch
from Agents.weather_agent import WeatherAgent
from Agents.news_agent import NewsAgent
from Agents.resource_agent import ResourceAgent
from Agents.risk_agent import RiskAgent
from Agents.emergency_planner import EmergencyPlanner
from Agents.coordinator import CoordinatorAgent
from Agents.location_agent import LocationAgent
from Tools.weather_tool import WeatherToolError
from Tools.news_tool import NewsToolError

class TestWeatherAgent(unittest.TestCase):

    @patch('Agents.weather_agent.get_weather')
    def test_analyze_success(self, mock_get_weather):
        mock_get_weather.return_value = {
            "current": {
                "temperature_2m": 25.5,
                "relative_humidity_2m": 85,
                "precipitation": 5.0,
                "wind_speed_10m": 12.0
            }
        }
        agent = WeatherAgent()
        result = agent.analyze(10.0, 20.0)
        self.assertEqual(result["temperature"], 25.5)
        self.assertEqual(result["humidity"], 85)
        self.assertEqual(result["precipitation"], 5.0)
        self.assertEqual(result["wind_speed"], 12.0)
        self.assertFalse(result["is_fallback"])

    @patch('Agents.weather_agent.get_weather')
    def test_analyze_fallback(self, mock_get_weather):
        mock_get_weather.side_effect = WeatherToolError("API offline")
        agent = WeatherAgent()
        result = agent.analyze(10.0, 20.0)
        self.assertEqual(result["temperature"], 20.0)
        self.assertEqual(result["humidity"], 50)
        self.assertEqual(result["precipitation"], 0.0)
        self.assertEqual(result["wind_speed"], 10.0)
        self.assertTrue(result["is_fallback"])
        self.assertIn("API offline", result["error_message"])


class TestNewsAgent(unittest.TestCase):

    @patch('Agents.news_agent.get_disaster_news')
    def test_analyze_success(self, mock_get_news):
        mock_get_news.return_value = {
            "articles": [
                {"title": "Flood in Region A"},
                {"title": "Cyclone warning issued"}
            ]
        }
        agent = NewsAgent()
        result = agent.analyze("Region A")
        self.assertEqual(result["location"], "Region A")
        self.assertEqual(result["article_count"], 2)
        self.assertIn("Flood in Region A", result["headlines"])
        self.assertFalse(result["is_fallback"])

    @patch('Agents.news_agent.get_disaster_news')
    def test_analyze_fallback(self, mock_get_news):
        mock_get_news.side_effect = NewsToolError("Invalid key")
        agent = NewsAgent()
        result = agent.analyze("Region A")
        self.assertEqual(result["article_count"], 0)
        self.assertEqual(result["headlines"], [])
        self.assertTrue(result["is_fallback"])


class TestResourceAgent(unittest.TestCase):

    @patch('Agents.resource_agent.requests.post')
    def test_analyze(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "elements": [
                {"type": "node", "id": 1, "lat": 10.0, "lon": 20.0, "tags": {"amenity": "hospital", "name": "Hosp A"}},
                {"type": "node", "id": 2, "lat": 10.1, "lon": 20.1, "tags": {"amenity": "hospital", "name": "Hosp B"}},
                {"type": "node", "id": 3, "lat": 10.2, "lon": 20.2, "tags": {"amenity": "shelter", "name": "Shelt A"}},
                {"type": "node", "id": 4, "lat": 10.3, "lon": 20.3, "tags": {"amenity": "fire_station", "name": "Fire A"}},
                {"type": "node", "id": 5, "lat": 10.4, "lon": 20.4, "tags": {"amenity": "police", "name": "Police A"}},
                {"type": "node", "id": 6, "lat": 10.5, "lon": 20.5, "tags": {"amenity": "social_facility", "name": "Relief A"}}
            ]
        }
        agent = ResourceAgent()
        result = agent.analyze("Test Location", 10.0, 20.0)
        self.assertEqual(result["hospital_count"], 2)
        self.assertEqual(result["shelter_count"], 1)
        self.assertEqual(result["fire_station_count"], 1)
        self.assertEqual(result["police_count"], 1)
        self.assertEqual(result["relief_center_count"], 1)
        self.assertFalse(result["is_fallback"])


class TestRiskAgent(unittest.TestCase):

    def test_risk_calculation(self):
        agent = RiskAgent()
        
        # CRITICAL Risk configuration:
        # humidity 95 (>90, +1.0), precip 55 (>50, +2.5), wind 27 (>25, +1.5), articles 6 (>=5, +3.0), resource scarcity (+2.0) -> total 10.0
        weather_high = {"humidity": 95, "precipitation": 55.0, "wind_speed": 27.0}
        news_high = {"article_count": 6}
        resource_high = {"hospital_count": 0, "shelter_count": 0}
        res_high = agent.analyze(weather_high, news_high, resource_high)
        self.assertEqual(res_high["risk_score"], 10.0)
        self.assertEqual(res_high["severity"], "CRITICAL")
        self.assertIn("reasoning", res_high)

        # Medium Risk configuration:
        # humidity 85 (+0.5), precip 2 (+1.0), wind 10 (+0.5), articles 3 (+2.0), resources normal -> total 4.0
        weather_med = {"humidity": 85, "precipitation": 2.0, "wind_speed": 10.0}
        news_med = {"article_count": 3}
        resource_med = {"hospital_count": 5, "shelter_count": 3}
        res_med = agent.analyze(weather_med, news_med, resource_med)
        self.assertEqual(res_med["risk_score"], 4.0)
        self.assertEqual(res_med["severity"], "MEDIUM")

        # Low Risk configuration:
        weather_low = {"humidity": 50, "precipitation": 0.0, "wind_speed": 5.0}
        news_low = {"article_count": 0}
        resource_low = {"hospital_count": 5, "shelter_count": 3}
        res_low = agent.analyze(weather_low, news_low, resource_low)
        self.assertEqual(res_low["risk_score"], 0.0)
        self.assertEqual(res_low["severity"], "LOW")


class TestEmergencyPlanner(unittest.TestCase):

    def test_plan_generation(self):
        planner = EmergencyPlanner()
        
        plan_critical = planner.generate_plan({"severity": "CRITICAL"})
        self.assertTrue(any("mandatory" in action.lower() for action in plan_critical))
        self.assertEqual(len(plan_critical), 5)

        plan_high = planner.generate_plan({"severity": "HIGH"})
        self.assertTrue(any("shelters" in action.lower() for action in plan_high))
        self.assertEqual(len(plan_high), 5)

        plan_med = planner.generate_plan({"severity": "MEDIUM"})
        self.assertEqual(len(plan_med), 4)

        plan_low = planner.generate_plan({"severity": "LOW"})
        self.assertEqual(len(plan_low), 2)


class TestCoordinatorAgent(unittest.TestCase):

    @patch('Agents.coordinator.ResourceAgent.analyze')
    @patch('Agents.weather_agent.get_weather')
    @patch('Agents.news_agent.get_disaster_news')
    def test_process_end_to_end(self, mock_get_news, mock_get_weather, mock_resource):
        mock_resource.return_value = {
            "location": "Assam",
            "latitude": 26.1445,
            "longitude": 91.7362,
            "hospital_count": 5,
            "shelter_count": 3,
            "fire_station_count": 2,
            "police_count": 2,
            "relief_center_count": 3,
            "resources": [],
            "is_fallback": False
        }
        mock_get_weather.return_value = {
            "current": {
                "temperature_2m": 28.0,
                "relative_humidity_2m": 85,
                "precipitation": 0.0,
                "wind_speed_10m": 5.0
            }
        }
        mock_get_news.return_value = {
            "articles": [
                {"title": "Flooding alerts in Assam"},
                {"title": "Storm damage in Assam"}
            ]
        }
        
        coordinator = CoordinatorAgent()
        result = coordinator.process("Assam", 26.1445, 91.7362)
        
        self.assertIn("weather", result)
        self.assertIn("news", result)
        self.assertIn("resources", result)
        self.assertIn("risk", result)
        self.assertIn("plan", result)
        self.assertIn("alert", result)
        self.assertIn("emergency_contacts", result)
        self.assertIn("safety_guidance", result)
        
        # humidity 85: +0.5, news articles 2: +1.0 -> total 1.5 (LOW)
        self.assertEqual(result["risk"]["risk_score"], 1.5)
        self.assertEqual(result["risk"]["severity"], "LOW")
        self.assertEqual(result["resources"]["shelter_count"], 3)
        self.assertEqual(len(result["plan"]), 2)
        
        # Check alerts and safety defaults
        self.assertEqual(result["alert"]["level"], "LOW")
        self.assertEqual(result["emergency_contacts"]["police"], "112 / 100")
        self.assertEqual(result["safety_guidance"]["type"], "CYCLONE SAFETY PROTOCOLS")


class TestLocationAgent(unittest.TestCase):

    @patch('Tools.location_tool.NominatimGeocodingProvider.geocode')
    def test_analyze_success(self, mock_geocode):
        mock_geocode.return_value = {
            "location": "Assam",
            "latitude": 26.2,
            "longitude": 92.9,
            "country": "India"
        }
        agent = LocationAgent()
        result = agent.analyze("Assam")
        self.assertEqual(result["location"], "Assam")
        self.assertEqual(result["latitude"], 26.2)
        self.assertEqual(result["longitude"], 92.9)
        self.assertEqual(result["country"], "India")
        self.assertFalse(result["is_fallback"])

    @patch('Tools.location_tool.NominatimGeocodingProvider.geocode')
    def test_analyze_fallback(self, mock_geocode):
        mock_geocode.side_effect = ValueError("API is rate-limited")
        agent = LocationAgent()
        result = agent.analyze("Assam")
        self.assertEqual(result["location"], "Assam")
        # Check fallback value
        self.assertEqual(result["latitude"], 26.2006)
        self.assertEqual(result["longitude"], 92.9376)
        self.assertEqual(result["country"], "India")
        self.assertTrue(result["is_fallback"])


class TestEmergencyContactAgent(unittest.TestCase):
    def test_haversine_distance(self):
        from Agents.emergency_contact_agent import EmergencyContactAgent
        agent = EmergencyContactAgent()
        # Test distance from New Delhi (28.6139, 77.2090) to Mumbai (19.0760, 72.8777) ~ 1148 km
        dist = agent.haversine_distance(28.6139, 77.2090, 19.0760, 72.8777)
        self.assertTrue(1100 <= dist <= 1200)

    def test_identify_contacts_with_hospital(self):
        from Agents.emergency_contact_agent import EmergencyContactAgent
        agent = EmergencyContactAgent()
        resources = [
            {"name": "Distant Hospital", "type": "hospital", "lat": 26.5, "lon": 91.5},
            {"name": "Nearby Hospital", "type": "hospital", "lat": 26.15, "lon": 91.73}
        ]
        contacts = agent.identify_contacts("Guwahati, Assam", 26.14, 91.73, resources)
        self.assertEqual(contacts["police"], "112 / 100")
        self.assertEqual(contacts["nearest_hospital"]["name"], "Nearby Hospital")
        self.assertTrue(contacts["nearest_hospital"]["distance_km"] < 10)


class TestCitizenSafetyAgent(unittest.TestCase):
    def test_generate_guidance_flood(self):
        from Agents.citizen_safety_agent import CitizenSafetyAgent
        agent = CitizenSafetyAgent()
        guidance = agent.generate_guidance("Flood")
        self.assertEqual(guidance["type"], "FLOOD SAFETY PROTOCOLS")
        self.assertIn("Move immediately to higher ground; do not wait for instruction.", guidance["immediate_actions"])

    def test_generate_guidance_earthquake(self):
        from Agents.citizen_safety_agent import CitizenSafetyAgent
        agent = CitizenSafetyAgent()
        guidance = agent.generate_guidance("Earthquake")
        self.assertEqual(guidance["type"], "EARTHQUAKE SAFETY PROTOCOLS")
        self.assertIn("DROP down onto your hands and knees.", guidance["immediate_actions"])


class TestAlertAgent(unittest.TestCase):
    def test_generate_alert_critical(self):
        from Agents.alert_agent import AlertAgent
        agent = AlertAgent()
        alert = agent.generate_alert(9.5, "CRITICAL", "Flood")
        self.assertEqual(alert["level"], "CRITICAL")
        self.assertEqual(alert["color"], "#ff0000")
        self.assertIn("🔴 CRITICAL FLOOD WARNING", alert["headline"])


class TestLanguageAgent(unittest.TestCase):
    def test_translate_term(self):
        from Agents.language_agent import LanguageAgent
        agent = LanguageAgent()
        self.assertEqual(agent.translate_term("CRITICAL", "hi"), "गंभीर")
        self.assertEqual(agent.translate_term("police", "pa"), "ਪੁਲਿਸ")
        self.assertEqual(agent.translate_term("NON_EXISTENT", "hi"), "NON_EXISTENT")

    def test_translate_report(self):
        from Agents.language_agent import LanguageAgent
        agent = LanguageAgent()
        report = {
            "alert": {"level": "CRITICAL", "headline": "🔴 CRITICAL FLOOD WARNING", "message": "Evacuate", "color": "red"},
            "risk": {"severity": "HIGH", "risk_score": 8.0, "reasoning": "High flood danger"},
            "emergency_contacts": {
                "police": "112", "ambulance": "102", "fire": "101",
                "disaster_management": "Disaster Help",
                "specialist_authority": "Authority",
                "nearest_hospital": {"name": "General Hospital", "distance_km": 2.5, "address": "Ring Road"}
            },
            "safety_guidance": {
                "type": "FLOOD SAFETY PROTOCOLS",
                "immediate_actions": ["Move to high ground"],
                "evacuation_instructions": ["Obey orders"],
                "what_to_avoid": []
            },
            "plan": ["Evacuate now"]
        }
        translated = agent.translate_report(report, "hi")
        self.assertEqual(translated["alert"]["level"], "गंभीर")
        self.assertEqual(translated["risk"]["severity"], "उच्च")
        self.assertEqual(translated["emergency_contacts"]["nearest_hospital"]["name"], "General Hospital")


if __name__ == "__main__":
    unittest.main()
