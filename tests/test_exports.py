import unittest
import os
import sys

# Add root folder to sys.path so we can import from streamlit_app.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from streamlit_app import generate_pdf_report, sanitize_for_pdf, get_unicode_font_path

class TestExportEngine(unittest.TestCase):
    
    def setUp(self):
        # Sample EOC disaster telemetry inputs
        self.loc_res = {
            "name": "Jalandhar",
            "country": "India",
            "latitude": 31.3260,
            "longitude": 75.5762
        }
        self.w = {
            "temperature": 28.5,
            "humidity": 65,
            "precipitation": 12.0,
            "wind_speed": 4.5
        }
        self.n = {
            "headlines": ["Verifying flood alerts in lower Punjab regions", "NDRF deployment on-site"],
            "articles": []
        }
        self.res_info = {
            "hospital_count": 5,
            "shelter_count": 2,
            "fire_station_count": 1,
            "police_count": 3,
            "relief_center_count": 2
        }
        self.r_list = [
            {"name": "Civil Hospital", "type": "hospital", "address": "GT Road Jalandhar", "lat": 31.32, "lon": 75.58},
            {"name": "EOC Shelter Alpha", "type": "shelter", "address": "Model Town", "lat": 31.31, "lon": 75.57}
        ]
        self.risk = {
            "risk_score": 6,
            "severity": "MEDIUM",
            "reasoning": "Substantial precipitation vectors detected in low-lying sectors."
        }
        self.plan = [
            "Evacuate vulnerable riverbank residences.",
            "Deploy emergency rescue vehicles to Jalandhar East."
        ]
        self.alert = {
            "headline": "🚨 FLOOD WATCH RED ALERT 🚨",
            "message": "Water levels exceeding normal thresholds."
        }
        self.contacts = {
            "ambulance": "108",
            "police": "100",
            "fire": "101",
            "disaster_management": "1078",
            "specialist_authority": "Jalandhar District Disaster Center",
            "nearest_hospital": {"name": "Civil Hospital", "distance_km": 1.2, "address": "GT Road"}
        }

    def test_sanitize_for_pdf(self):
        # Emojis should be stripped or converted
        raw = "🚨 Weather: 🌦️ 32 C, Location: 📍 Delhi"
        sanitized = sanitize_for_pdf(raw)
        self.assertNotIn("🚨", sanitized)
        self.assertNotIn("🌦️", sanitized)
        self.assertNotIn("📍", sanitized)
        self.assertIn("[ALERT]", sanitized)
        self.assertIn("[WEATHER]", sanitized)
        self.assertIn("[LOCATION]", sanitized)

    def test_english_pdf_generation(self):
        pdf_bytes = generate_pdf_report(
            self.loc_res, self.w, self.n, self.res_info, 
            self.r_list, self.risk, self.plan, self.alert, self.contacts
        )
        self.assertGreater(len(pdf_bytes), 0)
        self.assertEqual(pdf_bytes[:4], b"%PDF")

    def test_hindi_pdf_generation(self):
        # Hindi / Devanagari text input
        self.loc_res["name"] = "जलंधर"
        self.risk["reasoning"] = "बाढ़ की स्थिति का खतरा बना हुआ है।"
        self.plan = ["नदी के किनारे वाले क्षेत्रों से लोगों को सुरक्षित स्थानों पर पहुँचाएँ।"]
        
        pdf_bytes = generate_pdf_report(
            self.loc_res, self.w, self.n, self.res_info,
            self.r_list, self.risk, self.plan, self.alert, self.contacts
        )
        self.assertGreater(len(pdf_bytes), 0)
        self.assertEqual(pdf_bytes[:4], b"%PDF")

    def test_multilingual_unicode_pdf_generation(self):
        # Tamil, Telugu, and Sinhalese combined text
        self.loc_res["name"] = "சலந்தர் / జలంధర్ / ජලන්දර්"
        self.risk["reasoning"] = "ஆபத்து நிலைமை / ప్రమాద తీవ్రత / අනතුරුදායක තත්ත්වය"
        
        pdf_bytes = generate_pdf_report(
            self.loc_res, self.w, self.n, self.res_info,
            self.r_list, self.risk, self.plan, self.alert, self.contacts
        )
        self.assertGreater(len(pdf_bytes), 0)
        self.assertEqual(pdf_bytes[:4], b"%PDF")

    def test_empty_and_missing_optional_fields(self):
        # Alert and contacts are None
        pdf_bytes = generate_pdf_report(
            self.loc_res, self.w, self.n, self.res_info,
            self.r_list, self.risk, self.plan, alert=None, contacts=None
        )
        self.assertGreater(len(pdf_bytes), 0)
        self.assertEqual(pdf_bytes[:4], b"%PDF")

if __name__ == "__main__":
    unittest.main()
