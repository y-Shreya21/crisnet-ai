import unittest
import asyncio
import os
import sys

# Add root folder to sys.path so we can import from streamlit_app.py / Agents
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Agents.coordinator import CoordinatorAgent

class TestAgentOrchestrationIntegration(unittest.TestCase):
    
    def setUp(self):
        self.coordinator = CoordinatorAgent()

    def test_parallel_orchestrator_execution(self):
        # Run process synchronously which internally executes asynchronously
        result = self.coordinator.process("Delhi", latitude=28.7041, longitude=77.1025)
        
        # Verify result contains all necessary agent outputs
        self.assertIn("resolved_location", result)
        self.assertIn("weather", result)
        self.assertIn("news", result)
        self.assertIn("resources", result)
        self.assertIn("risk", result)
        self.assertIn("plan", result)
        self.assertIn("alert", result)
        self.assertIn("emergency_contacts", result)
        self.assertIn("safety_guidance", result)
        
        # Verify latency profiling metrics are successfully logged
        self.assertIn("metrics", result)
        metrics = result["metrics"]
        self.assertIn("weather_time", metrics)
        self.assertIn("news_time", metrics)
        self.assertIn("resource_time", metrics)
        self.assertIn("total_time", metrics)
        
        # Confirm coordinates are correct
        self.assertEqual(result["resolved_location"]["latitude"], 28.7041)
        self.assertEqual(result["resolved_location"]["longitude"], 77.1025)

if __name__ == "__main__":
    unittest.main()
