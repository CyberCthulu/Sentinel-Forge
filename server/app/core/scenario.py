# app/core/scenario.py
import uuid
from datetime import datetime, timezone


def now():
    return datetime.now(timezone.utc).isoformat()


def run_scenario(step):
    sequence = [
        {
            "id": f"log-{uuid.uuid4()}",
            "timestamp": now(),
            "type": "auth.failed",
            "source": "AUTH-GW-01",
            "message": "Failed login for admin",
            "severity": "low",
            "domain": "cyber",
        },
        {
            "id": f"log-{uuid.uuid4()}",
            "timestamp": now(),
            "type": "auth.failed",
            "source": "AUTH-GW-01",
            "message": "Failed login for admin",
            "severity": "low",
            "domain": "cyber",
        },
        {
            "id": f"log-{uuid.uuid4()}",
            "timestamp": now(),
            "type": "auth.failed",
            "source": "AUTH-GW-01",
            "message": "Failed login for admin",
            "severity": "low",
            "domain": "cyber",
        },
        {
            "id": f"log-{uuid.uuid4()}",
            "timestamp": now(),
            "type": "auth.success",
            "source": "AUTH-GW-01",
            "message": "Successful login from unfamiliar IP",
            "severity": "medium",
            "domain": "cyber",
        },
        {
            "id": f"log-{uuid.uuid4()}",
            "timestamp": now(),
            "type": "network.lateral",
            "source": "EDR-01",
            "message": "Lateral movement detected to node-2",
            "severity": "high",
            "domain": "cyber",
        },
        {
            "id": f"log-{uuid.uuid4()}",
            "timestamp": now(),
            "type": "physical.drone",
            "source": "UAS-SENSOR",
            "message": "Drone detected near Sector B",
            "severity": "high",
            "domain": "physical",
            "geospatial": {
                "lat": 37.7749,
                "lon": -122.4194,
                "alt": 120,
            },
        },
    ]

    if step < len(sequence):
        return sequence[step]
    return None