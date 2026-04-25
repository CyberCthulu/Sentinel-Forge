# app/core/correlation.py

def correlate(signals):
    """
    signals: list[Signal]
    """

    if not signals:
        return None

    # -----------------------
    # Confidence scoring
    # -----------------------
    total_weight = sum(s.weight for s in signals)
    score = min(round(total_weight, 2), 0.99)

    # -----------------------
    # Counts (used by frontend)
    # -----------------------
    cyber_count = len([s for s in signals if s.domain == "cyber"])
    physical_count = len([s for s in signals if s.domain == "physical"])

    # -----------------------
    # Return FRONTEND-ALIGNED SHAPE
    # -----------------------
    return {
        "score": score,
        "cyberCount": cyber_count,
        "physicalCount": physical_count,
        "signals": signals,  # raw Signal objects (pipeline will serialize)
    }