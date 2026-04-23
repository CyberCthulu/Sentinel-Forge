def detect(events):
    signals = {
        "failed_logins": False,
        "suspicious_login": False,
        "lateral_movement": False,
        "drone_activity": False,
    }

    failed_count = sum(1 for e in events if e["type"] == "failed_login")

    if failed_count >= 3:
        signals["failed_logins"] = True

    for e in events:
        if e["type"] == "successful_login":
            signals["suspicious_login"] = True
        if e["type"] == "lateral_movement":
            signals["lateral_movement"] = True
        if e["type"] == "drone_activity":
            signals["drone_activity"] = True

    return signals