# app/detection/engine.py
def detect(events):
    return {
        "failed_logins": detect_failed_logins(events),
        "suspicious_login": detect_suspicious_login(events),
        "lateral_movement": detect_lateral(events),
        "drone_activity": detect_drone(events),
    }