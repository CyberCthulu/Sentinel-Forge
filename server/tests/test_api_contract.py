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

    def test_signals_progress_and_incident_triggers(self):
        self.client.post("/simulate/start")

        payload = None

        for _ in range(6):
            response = self.client.post("/simulate/step")
            self.assertEqual(response.status_code, 200)
            payload = response.json()

        self.assertIsNotNone(payload)
        self.assertEqual(len(payload["events"]), 6)

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


if __name__ == "__main__":
    unittest.main()