def interpret(incident_type):
    if incident_type == "COORDINATED_INTRUSION":
        return {
            "severity": "CRITICAL",
            "confidence": 0.91,
            "summary": "Coordinated intrusion attempt detected",
            "why": [
                "Repeated failed logins",
                "Successful login from unfamiliar source",
                "Rapid lateral movement",
                "Drone activity near perimeter"
            ],
            "actions": [
                "Lock affected accounts",
                "Isolate compromised node",
                "Dispatch patrol to Sector B",
                "Increase surveillance"
            ]
        }
    return None