# app/core/interpreter.py

import uuid
from datetime import datetime, timezone


def now():
    return datetime.now(timezone.utc).isoformat()


def interpret(correlation):
    if not correlation:
        return None

    signals = correlation["signals"]
    kinds = [s.kind for s in signals]

    # -----------------------
    # Determine severity
    # -----------------------
    severity = "critical" if correlation["score"] >= 0.7 else "high"

    # -----------------------
    # Build narrative
    # -----------------------
    narrative = (
        "Multiple weak signals across cyber and physical domains have been "
        "correlated into a single coordinated threat pattern. "
        "This indicates a likely intrusion attempt involving both digital access "
        "and physical reconnaissance."
    )

    # -----------------------
    # Explanation (WHY)
    # -----------------------
    why = []

    if "auth.failed_burst" in kinds:
        why.append("Repeated authentication failures detected")

    if "auth.anomalous_login" in kinds:
        why.append("Suspicious login from unfamiliar source")

    if "network.lateral_movement" in kinds:
        why.append("Rapid lateral movement across systems")

    if "physical.drone_recon" in kinds:
        why.append("Drone activity detected near protected perimeter")

    # -----------------------
    # Final Incident Object
    # -----------------------
    return {
        "id": f"INC-{uuid.uuid4().hex[:6].upper()}",
        "type": "Coordinated Intrusion Attempt",
        "severity": severity,
        "confidence": correlation["score"],
        "summary": "Multiple cyber and physical indicators suggest a coordinated intrusion attempt",
        "narrative": narrative,
        "signals": kinds,
        "recommended_actions": [
            "Lock affected accounts",
            "Isolate compromised node",
            "Dispatch patrol to Sector B",
            "Increase surveillance",
        ],
        "timestamp": now(),
        "why": why,
    }