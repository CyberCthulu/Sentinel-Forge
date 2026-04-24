# app/core/pipeline.py
from app.core.detection import detect
from app.core.correlation import correlate
from app.core.interpreter import interpret


def run_pipeline(events):
    signals = detect(events)
    incident_type = correlate(signals)

    incident = interpret(incident_type) if incident_type else None

    return signals, incident
