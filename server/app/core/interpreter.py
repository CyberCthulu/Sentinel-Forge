# app/core/interpreter.py

from app.models.incident import Incident


def interpret(incident_type, signals):
    if not incident_type:
        return None

    why = []

    if signals["failed_logins"].active:
        why.append("Repeated failed logins")

    if signals["suspicious_login"].active:
        why.append("Successful login from unfamiliar source")

    if signals["lateral_movement"].active:
        why.append("Rapid lateral movement")

    if signals["drone_activity"].active:
        why.append("Drone activity near perimeter")

    location = None

    drone_signal = signals.get("drone_activity")
    if drone_signal and drone_signal.active:
        for e in drone_signal.evidence:
            if "metadata" in e and "lat" in e["metadata"]:
                location = e["metadata"]
                break

    if incident_type == "COORDINATED_INTRUSION":
        return Incident(
            type=incident_type,
            severity="CRITICAL",
            confidence=0.91,
            summary="Coordinated intrusion attempt detected",
            signals=list(signals.keys()),
            actions=[
                "Lock affected accounts",
                "Isolate compromised node",
                "Dispatch patrol to Sector B",
                "Increase surveillance"
            ],
            location=location
        )

    return None