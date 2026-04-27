# app/core/interpreter.py
import uuid
from datetime import datetime, timezone


def now():
    return datetime.now(timezone.utc).isoformat()


def interpret(correlation):
    if not correlation:
        return None

    confidence = correlation["confidence"]
    signals = correlation["signals"]
    kinds = [s.kind for s in signals]

    # -----------------------
    # Domain awareness (CRITICAL)
    # -----------------------
    has_cyber = any(s.domain == "cyber" for s in signals)
    has_physical = any(s.domain == "physical" for s in signals)

    # -----------------------
    # Build WHY dynamically
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
    # Threat classification (KEY UPGRADE)
    # -----------------------
    if confidence < 0.3:
        severity = "low"
        title = "Anomalous Activity Detected"
        summary = "Low-confidence anomalies detected across monitored systems"

    elif confidence < 0.5:
        severity = "medium"
        if has_cyber:
            title = "Intrusion Attempt Detected"
            summary = "Early indicators of unauthorized system access detected"
        else:
            title = "Suspicious Activity Detected"
            summary = "Unusual activity detected requiring monitoring"

    elif confidence < 0.7:
        severity = "high"
        title = "Escalating Intrusion Attempt"
        summary = "Multiple signals indicate an active intrusion attempt"

    else:
        severity = "critical"
        if has_cyber and has_physical:
            title = "Coordinated Intrusion Attempt"
            summary = "Cyber and physical signals confirm a coordinated threat"
        else:
            title = "Severe Intrusion Attempt"
            summary = "High-confidence intrusion activity detected"

    # -----------------------
    # Progressive actions (CLEANED)
    # -----------------------
    actions = []

    if "auth.failed_burst" in kinds:
        actions.append("Monitor authentication attempts")

    if "auth.anomalous_login" in kinds:
        actions.append("Review login source")

    if confidence >= 0.4:
        actions.append("Investigate affected systems")

    if "network.lateral_movement" in kinds:
        actions.append("Isolate compromised node")

    if confidence >= 0.7:
        actions.append("Lock affected accounts")
        actions.append("Increase surveillance")

    if has_physical:
        actions.append("Dispatch patrol to Sector B")

    # Remove duplicates while preserving order
    seen = set()
    actions = [a for a in actions if not (a in seen or seen.add(a))]

    # -----------------------
    # Final output
    # -----------------------
    return {
        "id": f"INC-{uuid.uuid4().hex[:6].upper()}",
        "type": title,
        "severity": severity,
        "confidence": confidence,
        "summary": summary,
        "signals": kinds,
        "recommended_actions": actions,
        "timestamp": now(),
        "why": why,
    }