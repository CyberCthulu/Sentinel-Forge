#app/core/pipeline.py
from app.core.detection import detect
from app.core.correlation import correlate
from app.core.interpreter import interpret
from app.core.detection import serialize_signal
from app.core.map import build_map_state


def run_pipeline(events):
    signals = detect(events)

    correlation = correlate(signals)
    incident = interpret(correlation)
    map_state = build_map_state(events)


    return {
        "signals": [serialize_signal(s) for s in signals],
        "correlation": correlation,
        "incident": incident,
        "map_state": map_state,

    }