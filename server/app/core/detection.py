# app/core/detection.py
from app.models.signal import Signal


def detect(events):
    signals = {
        "failed_logins": Signal("failed_logins", False, []),
        "suspicious_login": Signal("suspicious_login", False, []),
        "lateral_movement": Signal("lateral_movement", False, []),
        "drone_activity": Signal("drone_activity", False, []),
    }

    failed_events = [e for e in events if e["type"] == "failed_login"]

    if len(failed_events) >= 3:
        signals["failed_logins"] = Signal(
            name="failed_logins",
            active=True,
            evidence=failed_events
        )

    for e in events:
        if e["type"] == "successful_login":
            signals["suspicious_login"] = Signal(
                "suspicious_login", True, [e]
            )

        if e["type"] == "lateral_movement":
            signals["lateral_movement"] = Signal(
                "lateral_movement", True, [e]
            )

        if e["type"] == "drone_activity":
            signals["drone_activity"] = Signal(
                "drone_activity", True, [e]
            )

    return signals