import unittest

from fastapi.testclient import TestClient

from app.main import app


class SimulationApiContractTest(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.client.post("/reset")

    def test_state_shape_contains_events_signals_incident(self):
        response = self.client.post("/simulate/start")
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertIn("events", payload)
        self.assertIn("signals", payload)
        self.assertIn("incident", payload)

        self.assertEqual(payload["events"], [])
        self.assertIsNone(payload["incident"])

        self.assertEqual(
            payload["signals"],
            {
                "failed_logins": False,
                "suspicious_login": False,
                "lateral_movement": False,
                "drone_activity": False,
            },
        )

    def test_signals_progress_and_incident_triggers(self):
        self.client.post("/simulate/start")

        # Step through the entire scenario sequence.
        for _ in range(6):
            response = self.client.post("/simulate/step")
            self.assertEqual(response.status_code, 200)

        payload = response.json()

        self.assertEqual(len(payload["events"]), 6)
        self.assertTrue(all(payload["signals"].values()))
        self.assertEqual(payload["incident"]["severity"], "CRITICAL")


if __name__ == "__main__":
    unittest.main()
