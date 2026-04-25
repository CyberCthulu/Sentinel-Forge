#app/core/correlation.py
def correlate(signals):
    """
    signals: list[Signal]
    """

    if not signals:
        return None

    # Total confidence score from signal weights
    total_weight = sum(s.weight for s in signals)
    total_weight = min(round(total_weight, 2), 1.0)


    # Extract signal kinds for output
    contributing = [s.kind for s in signals]

    # -----------------------
    # Detection logic
    # -----------------------

    kinds = set(contributing)

    is_intrusion = all([
        "auth.failed_burst" in kinds,
        "auth.anomalous_login" in kinds,
        "network.lateral_movement" in kinds,
        "physical.drone_recon" in kinds,
    ])

    if is_intrusion:
        return {
            "type": "COORDINATED_INTRUSION",
            "confidence": round(total_weight, 2),
            "contributing_signals": contributing,
        }

    # Optional: partial correlation (nice upgrade)
    if total_weight >= 0.4:
        return {
            "type": "SUSPICIOUS_ACTIVITY",
            "confidence": round(total_weight, 2),
            "contributing_signals": contributing,
        }

    return None