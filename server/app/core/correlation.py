def correlate(signals):
    if all([
        signals["failed_logins"],
        signals["suspicious_login"],
        signals["lateral_movement"],
        signals["drone_activity"]
    ]):
        return "COORDINATED_INTRUSION"
    return None