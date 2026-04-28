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
    # Correlate / Fuse
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
    serialized_signals = [serialize_signal(signal) for signal in signals]

    # -----------------------
    # Serialize correlation
    # -----------------------
    serialized_correlation = {
        "confidence": correlation["confidence"],
        "level": correlation.get("level", "low"),
        "cyberCount": correlation["cyberCount"],
        "physicalCount": correlation["physicalCount"],
        "osintCount": correlation.get("osintCount", 0),
        "signals": [serialize_signal(signal) for signal in correlation["signals"]],
        "history": correlation.get("history", []),
        "explanation": correlation.get("explanation", []),
        "scoreBreakdown": correlation.get(
            "scoreBreakdown",
            {
                "base": 0,
                "evidenceBonus": 0,
                "diversityBonus": 0,
                "crossDomainBonus": 0,
                "escalationBonus": 0,
                "raw": 0,
            },
        ),
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