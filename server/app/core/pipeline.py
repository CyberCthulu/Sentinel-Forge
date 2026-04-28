# app/core/pipeline.py

from app.normalization.normalizer import normalize_events
from app.core.detection import detect, serialize_signal
from app.core.correlation import correlate
from app.core.interpreter import interpret
from app.core.map import build_map_state


def run_pipeline(events, previous_correlation=None):
    previous_correlation = previous_correlation or {}
    previous_history = previous_correlation.get("history", [])

    # -----------------------
    # Normalize
    # -----------------------
    normalized_events = normalize_events(events)

    # -----------------------
    # Detect signals
    # -----------------------
    signals = detect(normalized_events)

    # -----------------------
    # Correlate
    # -----------------------
    correlation = correlate(signals, previous_history=previous_history)

    # -----------------------
    # Interpret
    # -----------------------
    incident = interpret(correlation) if signals else None

    # -----------------------
    # Map state
    # -----------------------
    map_state = build_map_state(normalized_events)

    # -----------------------
    # Serialize signals
    # -----------------------
    serialized_signals = [serialize_signal(s) for s in signals]

    # -----------------------
    # Serialize correlation
    # -----------------------
    serialized_correlation = {
        "confidence": correlation["confidence"],
        "cyberCount": correlation["cyberCount"],
        "physicalCount": correlation["physicalCount"],
        "signals": [serialize_signal(s) for s in correlation["signals"]],
        "history": correlation.get("history", []),
    }

    # -----------------------
    # Final response
    # -----------------------
    return {
        "events": normalized_events,
        "signals": serialized_signals,
        "correlation": serialized_correlation,
        "incident": incident,
        "map_state": map_state,
    }