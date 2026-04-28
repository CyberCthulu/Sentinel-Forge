# app/state/store.py
from __future__ import annotations

from copy import deepcopy
from typing import Any


def build_initial_state() -> dict[str, Any]:
    """
    Canonical API state shape.

    This is the contract the frontend expects.
    Do not casually change this shape.
    """
    return {
        "events": [],
        "signals": [],
        "correlation": {
            "confidence": 0,
            "cyberCount": 0,
            "physicalCount": 0,
            "signals": [],
            "history": [],
        },
        "incident": None,
        "map_state": {
            "tracks": [],
            "assets": [],
            "zones": [],
            "threat_paths": [],
        },
        "meta": {
            "mode": "demo",
            "step": 0,
            "status": "idle",
        },
    }


class StateStore:
    """
    In-memory state store.

    For the hackathon demo, this is enough.
    Later this could be swapped for Redis, Postgres, or an event bus.
    """

    def __init__(self):
        self._state = build_initial_state()

    def reset(self) -> dict[str, Any]:
        self._state = build_initial_state()
        return self.get()

    def get(self) -> dict[str, Any]:
        return deepcopy(self._state)

    def replace(self, state: dict[str, Any]) -> dict[str, Any]:
        self._state = deepcopy(state)
        return self.get()

    def set_status(self, status: str) -> dict[str, Any]:
        self._state["meta"]["status"] = status
        return self.get()

    def get_step(self) -> int:
        return int(self._state.get("meta", {}).get("step", 0))

    def increment_step(self) -> int:
        current = self.get_step()
        self._state["meta"]["step"] = current + 1
        return self._state["meta"]["step"]

    def append_event(self, event: dict[str, Any]) -> dict[str, Any]:
        self._state["events"].append(event)
        return self.get()

    def apply_pipeline_result(self, result: dict[str, Any]) -> dict[str, Any]:
        if "events" in result:
            self._state["events"] = result.get("events", [])

        self._state["signals"] = result.get("signals", [])
        self._state["correlation"] = result.get(
            "correlation",
            {
                "confidence": 0,
                "cyberCount": 0,
                "physicalCount": 0,
                "signals": [],
                "history": [],
            },
        )
        self._state["incident"] = result.get("incident")
        self._state["map_state"] = result.get(
            "map_state",
            {
                "tracks": [],
                "assets": [],
                "zones": [],
                "threat_paths": [],
            },
        )
        return self.get()
        self._state["signals"] = result.get("signals", [])
        self._state["correlation"] = result.get(
            "correlation",
            {
                "confidence": 0,
                "cyberCount": 0,
                "physicalCount": 0,
                "signals": [],
                "history": [],
            },
        )
        self._state["incident"] = result.get("incident")
        self._state["map_state"] = result.get(
            "map_state",
            {
                "tracks": [],
                "assets": [],
                "zones": [],
                "threat_paths": [],
            },
        )
        return self.get()