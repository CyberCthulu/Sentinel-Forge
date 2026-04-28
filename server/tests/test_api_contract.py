# server/tests/test_api_contract.py

import unittest

from fastapi.testclient import TestClient

from app.main import app


class SimulationApiContractTest(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.client.post("/reset")

    def test_state_shape_contains_frontend_contract(self):
        response = self.client.post("/simulate/start")
        self.assertEqual(response.status_code, 200)

        payload = response.json()

        self.assertIn("events", payload)
        self.assertIn("signals", payload)
        self.assertIn("correlation", payload)
        self.assertIn("incident", payload)
        self.assertIn("map_state", payload)
        self.assertIn("meta", payload)

        self.assertEqual(payload["events"], [])
        self.assertEqual(payload["signals"], [])
        self.assertIsNone(payload["incident"])

        self.assertEqual(payload["correlation"]["confidence"], 0)
        self.assertEqual(payload["correlation"]["cyberCount"], 0)
        self.assertEqual(payload["correlation"]["physicalCount"], 0)
        self.assertEqual(payload["correlation"]["signals"], [])

        self.assertIn("tracks", payload["map_state"])
        self.assertIn("assets", payload["map_state"])
        self.assertIn("zones", payload["map_state"])
        self.assertIn("threat_paths", payload["map_state"])

    def test_normal_events_do_not_trigger_signals_immediately(self):
        self.client.post("/simulate/start")

        for _ in range(3):
            response = self.client.post("/simulate/step")
            self.assertEqual(response.status_code, 200)

        payload = response.json()

        self.assertEqual(len(payload["events"]), 3)
        self.assertEqual(payload["signals"], [])
        self.assertEqual(payload["correlation"]["confidence"], 0)
        self.assertIsNone(payload["incident"])

    def test_signals_progress_and_incident_triggers(self):
        self.client.post("/simulate/start")

        payload = None

        # Step through full richer scenario.
        for _ in range(18):
            response = self.client.post("/simulate/step")
            self.assertEqual(response.status_code, 200)
            payload = response.json()

        self.assertIsNotNone(payload)
        self.assertEqual(len(payload["events"]), 18)

        signal_kinds = {signal["kind"] for signal in payload["signals"]}

        self.assertIn("auth.failed_burst", signal_kinds)
        self.assertIn("auth.anomalous_login", signal_kinds)
        self.assertIn("network.lateral_movement", signal_kinds)
        self.assertIn("physical.drone_recon", signal_kinds)

        self.assertIsNotNone(payload["incident"])
        self.assertEqual(payload["incident"]["severity"], "critical")

        self.assertGreaterEqual(payload["correlation"]["confidence"], 0.9)
        self.assertGreaterEqual(len(payload["correlation"]["history"]), 1)

    def test_reset_clears_state(self):
        self.client.post("/simulate/start")
        self.client.post("/simulate/step")

        response = self.client.post("/reset")
        self.assertEqual(response.status_code, 200)

        payload = response.json()

        self.assertEqual(payload["events"], [])
        self.assertEqual(payload["signals"], [])
        self.assertEqual(payload["correlation"]["confidence"], 0)
        self.assertIsNone(payload["incident"])
        self.assertEqual(payload["map_state"]["tracks"], [])

    def test_events_are_normalized_after_step(self):
        self.client.post("/simulate/start")

        response = self.client.post("/simulate/step")
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(len(payload["events"]), 1)

        event = payload["events"][0]

        self.assertIn("id", event)
        self.assertIn("timestamp", event)
        self.assertIn("type", event)
        self.assertIn("source", event)
        self.assertIn("domain", event)
        self.assertIn("severity", event)
        self.assertIn("message", event)
        self.assertIn("raw", event)
        self.assertIn("metadata", event)

        self.assertIn(event["domain"], ["cyber", "physical", "osint", "unknown"])
        self.assertIn(event["severity"], ["low", "medium", "high", "critical", "unknown"])


if __name__ == "__main__":
    unittest.main()