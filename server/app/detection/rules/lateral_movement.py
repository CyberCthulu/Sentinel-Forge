# app/detection/rules/lateral_movement.py

from app.models.signal import Signal


def detect_lateral_movement(events):
    explicit_lateral = [
        e for e in events
        if e["type"] == "network.lateral"
    ]

    node_access = [
        e for e in events
        if e["type"] == "node.access"
        and e.get("metadata", {}).get("rapid_sequence") is True
    ]

    unique_nodes = {
        e.get("metadata", {}).get("node")
        for e in node_access
        if e.get("metadata", {}).get("node")
    }

    if not explicit_lateral and len(unique_nodes) < 3:
        return None

    evidence = [e["id"] for e in explicit_lateral] or [e["id"] for e in node_access]

    return Signal(
        id="sig-lateral",
        kind="network.lateral_movement",
        domain="cyber",
        weight=0.26,
        evidence=evidence,
        label="Rapid Lateral Movement",
        description="Rapid access across internal nodes suggests active intrusion behavior.",
        source="rule.lateral_movement",
        metadata={
            "nodes": sorted(unique_nodes),
            "node_count": len(unique_nodes),
        },
    )