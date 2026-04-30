# app/core/pipeline.py

from app.normalization.normalizer import normalize_events
from app.core.detection import detect, serialize_signal
from app.core.correlation import correlate
from app.core.interpreter import interpret
from app.core.map import build_map_state
from app.agent.context_builder import build_agent_context
from app.agent.agent import run_agent


def fallback_guidance(incident):
    return {
        "assessment": "High-confidence intrusion detected",
        "priority": "Contain immediately",
        "next_steps": incident.get("recommended_actions", []) if incident else [],
        "operator_note": "Fallback guidance generated because the live AI agent was unavailable.",
    }


def run_pipeline(events, previous_correlation=None):
    previous_correlation = previous_correlation or {}
    previous_history = previous_correlation.get("history", [])

    normalized_events = normalize_events(events)

    signals = detect(normalized_events)

    correlation = correlate(signals, previous_history=previous_history)

    incident = interpret(correlation) if signals else None

    map_state = build_map_state(normalized_events, signals=signals)

    serialized_signals = [serialize_signal(signal) for signal in signals]

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

    agent_output = None

    if incident:
        agent_context = build_agent_context(serialized_correlation, incident)
        agent_output = run_agent(agent_context)

    return {
        "events": normalized_events,
        "signals": serialized_signals,
        "correlation": serialized_correlation,
        "incident": incident,
        "map_state": map_state,
        "agent": agent_output,
    }