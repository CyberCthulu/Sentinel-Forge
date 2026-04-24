# app/adapters/mock.py
from datetime import datetime
from typing import Any
from .base import Adapter


class MockAdapter(Adapter):

    @property
    def name(self):
        return "mock"

    def __init__(self, config=None):
        super().__init__(config)
        self.events = sorted(config.get("events", []), key=lambda e: e["timestamp"])

    def _parse(self, ts):
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))

    def _pull_page(self, *, cursor, since, page_size):
        start = int(cursor) if cursor else 0

        filtered = self.events
        if since:
            filtered = [e for e in filtered if self._parse(e["timestamp"]) > self._parse(since)]

        page = filtered[start:start + page_size]
        next_cursor = str(start + page_size) if start + page_size < len(filtered) else None

        return page, next_cursor

    def normalize_event(self, event: dict[str, Any]):
        return {
            "id": str(event.get("id") or f"mock-{hash(str(event))}"),
            "timestamp": self._to_rfc3339_utc(event["timestamp"]),
            "source": self.name,
            "domain": "cyber",
            "type": event.get("type", "mock_event"),
            "severity": event.get("severity", "low"),
            "raw": event,
            "metadata": event.get("metadata", {}),
        }