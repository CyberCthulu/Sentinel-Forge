# app/core/detection.py

from app.detection.engine import detect


def serialize_signal(signal):
    if hasattr(signal, "to_dict"):
        return signal.to_dict()

    return {
        "id": signal.id,
        "kind": signal.kind,
        "domain": signal.domain,
        "weight": signal.weight,
        "evidence": signal.evidence,
        "label": signal.label,
    }