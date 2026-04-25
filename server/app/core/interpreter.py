# app/core/interpreter.py
def interpret(correlation):
    if not correlation:
        return None

    if correlation["type"] == "COORDINATED_INTRUSION":
        return {
            "type": "COORDINATED_INTRUSION",
            "severity": "CRITICAL",
            "confidence": correlation["confidence"],
            "summary": "Coordinated intrusion attempt detected",
            "signals": correlation["contributing_signals"],
            "recommended_actions": [
                "Lock affected accounts",
                "Isolate compromised node",
                "Dispatch patrol",
                "Increase surveillance"
            ],
        }

    if correlation["type"] == "SUSPICIOUS_ACTIVITY":
        return {
            "type": "SUSPICIOUS_ACTIVITY",
            "severity": "HIGH",
            "confidence": correlation["confidence"],
            "summary": "Suspicious multi-domain activity detected",
            "signals": correlation["contributing_signals"],
            "recommended_actions": [
                "Monitor system activity",
                "Review authentication logs",
                "Increase alert level"
            ],
        }

    return None