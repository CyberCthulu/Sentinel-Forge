# app/core/scenario.py

from __future__ import annotations


def build_scenario_events() -> list[dict]:
    """
    Realistic coordinated intrusion scenario.

    Important:
    - Includes normal/background events.
    - Only certain events should trigger detection signals.
    - MockAdapter adds id/timestamp at runtime.
    """

    return [
        # -----------------------
        # Normal background noise
        # -----------------------
        {
            "type": "auth.success",
            "source": "AUTH-GW-01",
            "domain": "cyber",
            "severity": "low",
            "message": "Normal user login from known workstation",
            "metadata": {
                "user": "analyst01",
                "ip": "10.0.1.14",
                "known_source": True,
                "unfamiliar_ip": False,
            },
        },
        {
            "type": "system.heartbeat",
            "source": "EDR-01",
            "domain": "cyber",
            "severity": "low",
            "message": "Endpoint sensor heartbeat received",
            "metadata": {
                "host": "node-1",
                "status": "healthy",
            },
        },
        {
            "type": "network.connection",
            "source": "NET-GW-01",
            "domain": "cyber",
            "severity": "low",
            "message": "Routine internal service connection",
            "metadata": {
                "src": "node-1",
                "dst": "service-api",
                "port": 443,
                "known_pattern": True,
            },
        },

        # -----------------------
        # Suspicious auth pattern
        # -----------------------
        {
            "type": "auth.failed",
            "source": "AUTH-GW-01",
            "domain": "cyber",
            "severity": "low",
            "message": "Failed login for admin",
            "metadata": {
                "user": "admin",
                "ip": "185.199.110.12",
            },
        },
        {
            "type": "auth.failed",
            "source": "AUTH-GW-01",
            "domain": "cyber",
            "severity": "low",
            "message": "Failed login for admin",
            "metadata": {
                "user": "admin",
                "ip": "185.199.110.12",
            },
        },
        {
            "type": "auth.failed",
            "source": "AUTH-GW-01",
            "domain": "cyber",
            "severity": "low",
            "message": "Failed login for admin",
            "metadata": {
                "user": "admin",
                "ip": "185.199.110.12",
            },
        },

        # -----------------------
        # Normal event between signals
        # -----------------------
        {
            "type": "file.access",
            "source": "FILE-SRV-01",
            "domain": "cyber",
            "severity": "low",
            "message": "Routine file access by logistics user",
            "metadata": {
                "user": "logistics02",
                "path": "/shared/supply_manifest.csv",
                "known_pattern": True,
            },
        },

        # -----------------------
        # Suspicious login after failures
        # -----------------------
        {
            "type": "auth.success",
            "source": "AUTH-GW-01",
            "domain": "cyber",
            "severity": "medium",
            "message": "Successful login from unfamiliar IP",
            "metadata": {
                "user": "admin",
                "ip": "185.199.110.12",
                "known_source": False,
                "unfamiliar_ip": True,
                "after_failed_attempts": True,
            },
        },

        # -----------------------
        # More normal background
        # -----------------------
        {
            "type": "system.health",
            "source": "NET-GW-01",
            "domain": "cyber",
            "severity": "low",
            "message": "Network gateway health check passed",
            "metadata": {
                "status": "healthy",
            },
        },

        # -----------------------
        # Lateral movement chain
        # -----------------------
        {
            "type": "node.access",
            "source": "EDR-01",
            "domain": "cyber",
            "severity": "medium",
            "message": "Admin session accessed node-1",
            "metadata": {
                "user": "admin",
                "node": "node-1",
                "rapid_sequence": True,
            },
        },
        {
            "type": "node.access",
            "source": "EDR-01",
            "domain": "cyber",
            "severity": "medium",
            "message": "Admin session accessed node-2",
            "metadata": {
                "user": "admin",
                "node": "node-2",
                "rapid_sequence": True,
            },
        },
        {
            "type": "node.access",
            "source": "EDR-01",
            "domain": "cyber",
            "severity": "high",
            "message": "Admin session accessed node-3 in rapid sequence",
            "metadata": {
                "user": "admin",
                "node": "node-3",
                "rapid_sequence": True,
            },
        },

        # Keep old explicit event type for compatibility with current UI/detection.
        {
            "type": "network.lateral",
            "source": "EDR-01",
            "domain": "cyber",
            "severity": "high",
            "message": "Lateral movement detected across internal nodes",
            "metadata": {
                "user": "admin",
                "nodes": ["node-1", "node-2", "node-3"],
                "technique": "rapid_node_access",
            },
        },

        # -----------------------
        # Additional cyber escalation
        # Detection rules will use these in next pass.
        # -----------------------
        {
            "type": "identity.privilege_escalation",
            "source": "EDR-01",
            "domain": "cyber",
            "severity": "high",
            "message": "Privilege escalation attempt detected",
            "metadata": {
                "user": "admin",
                "target_role": "domain_admin",
            },
        },
        {
            "type": "network.exfiltration",
            "source": "NET-GW-01",
            "domain": "cyber",
            "severity": "high",
            "message": "Unusual outbound data transfer detected",
            "metadata": {
                "src": "node-3",
                "dst_ip": "203.0.113.77",
                "bytes": 82000000,
            },
        },

        # -----------------------
        # Physical / OSINT domain
        # -----------------------
        {
            "type": "physical.sensor_heartbeat",
            "source": "PERIMETER-SENSOR",
            "domain": "physical",
            "severity": "low",
            "message": "Perimeter sensor heartbeat received",
            "metadata": {
                "sector": "B",
                "status": "healthy",
            },
        },
        {
            "type": "physical.drone",
            "source": "UAS-SENSOR",
            "domain": "physical",
            "severity": "high",
            "message": "Drone detected near Sector B",
            "geospatial": {
                "lat": 37.7749,
                "lon": -122.4194,
                "alt": 120,
            },
            "metadata": {
                "sector": "B",
                "track_id": "uas-track-77",
                "distance_m": 420,
            },
        },
        {
            "type": "osint.ais_anomaly",
            "source": "AIS-FEED",
            "domain": "osint",
            "severity": "medium",
            "message": "AIS anomaly detected near restricted maritime corridor",
            "geospatial": {
                "lat": 37.8044,
                "lon": -122.4494,
            },
            "metadata": {
                "vessel_id": "unknown-vessel-19",
                "behavior": "loitering",
                "speed_knots": 2.1,
            },
        },
    ]


def run_scenario(step: int):
    """
    Backward-compatible helper.
    New code should prefer MockAdapter.fetch_next_event().
    """
    sequence = build_scenario_events()

    if step < len(sequence):
        return sequence[step]

    return None