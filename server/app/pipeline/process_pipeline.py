# app/pipeline/process_pipeline.py
def process(adapter):
    events = adapter.fetch_events()

    normalized = normalize(events)
    signals = detect(normalized)

    incident_type = correlate(signals)

    if incident_type:
        return interpret(incident_type, signals)

    return None