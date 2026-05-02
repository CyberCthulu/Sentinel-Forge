# app/core/interpreter.py

import uuid
from datetime import datetime, timezone


def now():
    return datetime.now(timezone.utc).isoformat()


def interpret(correlation, action_status=None, previous_incident=None):
    if not correlation:
        return None

    confidence = correlation["confidence"]
    signals = correlation["signals"]
    kinds = [s.kind for s in signals]

    has_cyber = any(s.domain == "cyber" for s in signals)
    has_physical = any(s.domain == "physical" for s in signals)
    has_osint = any(s.domain == "osint" for s in signals)

    why = build_why(kinds)
    severity, title, summary = classify_threat(
        confidence=confidence,
        has_cyber=has_cyber,
        has_physical=has_physical,
        has_osint=has_osint,
    )
    actions = build_actions(kinds, confidence, has_physical, has_osint)
    action_status = action_status or {}
    completed_required = [action for action in actions if action_status.get(action)]

    incident_id = (
        previous_incident.get("id")
        if previous_incident and previous_incident.get("id")
        else f"INC-{uuid.uuid4().hex[:6].upper()}"
    )

    incident_status = "active"
    if actions and len(completed_required) == len(actions):
        incident_status = "resolved"
    elif completed_required:
        incident_status = "containment_in_progress"

    return {
        "id": incident_id,
        "type": title,
        "severity": severity,
        "confidence": confidence,
        "summary": summary,
        "narrative": build_narrative(severity, has_cyber, has_physical, has_osint),
        "signals": kinds,
        "recommended_actions": actions,
        "timestamp": now(),
        "why": why,
        "status": incident_status,
        "resolved_at": now() if incident_status == "resolved" else None,
    }


def build_why(kinds):
    why = []

    if "auth.failed_burst" in kinds:
        why.append("Repeated authentication failures detected")

    if "auth.anomalous_login" in kinds:
        why.append("Suspicious login from unfamiliar source")

    if "network.lateral_movement" in kinds:
        why.append("Rapid lateral movement across systems")

    if "identity.privilege_escalation" in kinds:
        why.append("Privilege escalation activity detected")

    if "network.data_exfiltration" in kinds:
        why.append("Unusual outbound data transfer suggests possible exfiltration")

    if "physical.drone_recon" in kinds:
        why.append("Drone activity detected near protected perimeter")

    if "osint.ais_anomaly" in kinds:
        why.append("AIS anomaly detected near restricted maritime corridor")

    return why


def classify_threat(confidence, has_cyber, has_physical, has_osint):
    if confidence < 0.3:
        return (
            "low",
            "Anomalous Activity Detected",
            "Low-confidence anomalies detected across monitored systems",
        )

    if confidence < 0.5:
        if has_cyber:
            return (
                "medium",
                "Intrusion Attempt Detected",
                "Early indicators of unauthorized system access detected",
            )

        return (
            "medium",
            "Suspicious Activity Detected",
            "Unusual activity detected requiring monitoring",
        )

    if confidence < 0.7:
        return (
            "high",
            "Escalating Intrusion Attempt",
            "Multiple signals indicate an active intrusion attempt",
        )

    if has_cyber and (has_physical or has_osint):
        return (
            "critical",
            "Coordinated Intrusion Attempt",
            "Cyber, physical, and/or OSINT signals confirm a coordinated threat pattern",
        )

    return (
        "critical",
        "Severe Intrusion Attempt",
        "High-confidence intrusion activity detected",
    )


def build_actions(kinds, confidence, has_physical, has_osint):
    actions = []

    if "auth.failed_burst" in kinds:
        actions.append("Monitor authentication attempts")

    if "auth.anomalous_login" in kinds:
        actions.append("Review login source")

    if confidence >= 0.4:
        actions.append("Investigate affected systems")

    if "network.lateral_movement" in kinds:
        actions.append("Isolate compromised node")

    if "identity.privilege_escalation" in kinds:
        actions.append("Revoke elevated privileges")

    if "network.data_exfiltration" in kinds:
        actions.append("Block suspicious outbound transfer")

    if confidence >= 0.7:
        actions.append("Lock affected accounts")
        actions.append("Increase surveillance")

    if has_physical:
        actions.append("Dispatch patrol to Sector B")

    if has_osint:
        actions.append("Review AIS/vessel intelligence feed")

    seen = set()
    return [action for action in actions if not (action in seen or seen.add(action))]


def build_narrative(severity, has_cyber, has_physical, has_osint):
    domains = []

    if has_cyber:
        domains.append("cyber")

    if has_physical:
        domains.append("physical")

    if has_osint:
        domains.append("OSINT")

    domain_text = ", ".join(domains) if domains else "monitored"

    return (
        f"Sentinel Forge correlated signals across {domain_text} domains. "
        f"The current assessment is classified as {severity.upper()} based on "
        "signal confidence, evidence count, and cross-domain escalation pattern."
    )