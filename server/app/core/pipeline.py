# app/core/pipeline.py

from app.core.detection import detect, serialize_signal
from app.core.correlation import correlate
from app.core.interpreter import interpret
from app.core.map import build_map_state


def run_pipeline(events):
    # -----------------------
    # Detect signals
    # -----------------------
    signals = detect(events)

    # -----------------------
    # Correlate
    # -----------------------
    correlation = correlate(signals)

    # -----------------------
    # Interpret
    # -----------------------
    incident = interpret(correlation)

    # -----------------------
    # Map state (leave as-is)
    # -----------------------
    map_state = build_map_state(events)

    # -----------------------
    # Serialize signals
    # -----------------------
    serialized_signals = [serialize_signal(s) for s in signals]

    serialized_correlation = None
    if correlation:
        serialized_correlation = {
            "score": correlation["score"],
            "cyberCount": correlation["cyberCount"],
            "physicalCount": correlation["physicalCount"],
            "signals": [serialize_signal(s) for s in correlation["signals"]],
        }

    # -----------------------
    # Final response (UI-ready)
    # -----------------------
    return {
        "signals": serialized_signals,
        "correlation": serialized_correlation,
        "incident": incident,
        "map_state": map_state,
    }