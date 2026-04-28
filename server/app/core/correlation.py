# app/core/correlation.py

from datetime import datetime, timezone


def now():
    return datetime.now(timezone.utc).isoformat()


def correlate(signals, previous_history=None):
    """
    signals: list[Signal]

    Returns frontend-safe correlation object.

    This keeps confidence scoring backend-derived and tracks confidence history
    so the frontend correlation graph can become real instead of locally simulated.
    """

    previous_history = previous_history or []

    if not signals:
        return {
            "confidence": 0,
            "cyberCount": 0,
            "physicalCount": 0,
            "signals": [],
            "history": previous_history,
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
    # Correlation history
    # -----------------------
    last = previous_history[-1] if previous_history else None

    if not last or last.get("confidence") != confidence:
        history = [
            *previous_history,
            {
                "timestamp": now(),
                "confidence": confidence,
            },
        ][-12:]
    else:
        history = previous_history

    return {
        "confidence": confidence,
        "cyberCount": cyber_count,
        "physicalCount": physical_count,
        "signals": signals,
        "history": history,
    }