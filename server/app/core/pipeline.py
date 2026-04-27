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
    incident = None

    if correlation and correlation["confidence"] >= 0.35:
        incident = interpret(correlation)
    # -----------------------
    # Map state
    # -----------------------
    map_state = build_map_state(events)

    # -----------------------
    # Serialize signals
    # -----------------------
    serialized_signals = [serialize_signal(s) for s in signals]

    # -----------------------
    # Serialize correlation (SAFE + SIMPLE)
    # -----------------------
    serialized_correlation = {
        "confidence": correlation["confidence"],
        "cyberCount": correlation["cyberCount"],
        "physicalCount": correlation["physicalCount"],
        "signals": [serialize_signal(s) for s in correlation["signals"]],
    }

    # -----------------------
    # Final response
    # -----------------------
    return {
        "signals": serialized_signals,
        "correlation": serialized_correlation,
        "incident": incident,
        "map_state": map_state,
    }