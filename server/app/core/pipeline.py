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
    # Interpret (ALWAYS if signals exist)
    # -----------------------
    incident = interpret(correlation) if signals else None

    # -----------------------
    # Map state
    # -----------------------
    map_state = build_map_state(events)

    # -----------------------
    # Serialize signals
    # -----------------------
    serialized_signals = [serialize_signal(s) for s in signals]

    # -----------------------
    # Serialize correlation (safe)
    # -----------------------
    serialized_correlation = {
        "confidence": correlation["confidence"],
        "cyberCount": correlation["cyberCount"],
        "physicalCount": correlation["physicalCount"],
        "signals": [serialize_signal(s) for s in correlation["signals"]],
    } if correlation else {
        "confidence": 0,
        "cyberCount": 0,
        "physicalCount": 0,
        "signals": []
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