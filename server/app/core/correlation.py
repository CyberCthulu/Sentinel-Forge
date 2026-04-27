# app/core/correlation.py

def correlate(signals):
    """
    signals: list[Signal]
    """

    if not signals:
        return {
            "confidence": 0,
            "cyberCount": 0,
            "physicalCount": 0,
            "signals": [],
        }

    # -----------------------
    # Confidence scoring
    # -----------------------
    total_weight = sum(s.weight for s in signals)
    confidence = min(round(total_weight, 2), 0.99)

    # -----------------------
    # Counts
    # -----------------------
    cyber_count = sum(1 for s in signals if s.domain == "cyber")
    physical_count = sum(1 for s in signals if s.domain == "physical")

    # -----------------------
    # Return simple, consistent shape
    # -----------------------
    return {
        "confidence": confidence,
        "cyberCount": cyber_count,
        "physicalCount": physical_count,
        "signals": signals,
    }