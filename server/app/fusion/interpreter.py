def interpret(type, signals):
    return {
        "severity": "CRITICAL",
        "confidence": score(signals),
        "summary": "Coordinated intrusion attempt detected",
        "narrative": "Multiple cyber and physical signals indicate coordinated probing.",
        "actions": [
            "Lock accounts",
            "Isolate node",
            "Dispatch patrol",
            "Increase surveillance"
        ]
    }