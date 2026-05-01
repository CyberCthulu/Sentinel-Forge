# app/core/map.py

from __future__ import annotations

from typing import Any


def build_map_state(events: list[dict[str, Any]], signals=None) -> dict[str, Any]:
    signals = signals or []

    signal_kinds = {s.kind for s in signals}
    event_types = {e.get("type") for e in events}

    tracks = build_tracks(events)
    assets = build_assets(signal_kinds, event_types)
    zones = build_zones(signal_kinds, tracks)
    threat_paths = build_threat_paths(signal_kinds, events, tracks)

    return {
        "tracks": tracks,
        "assets": assets,
        "zones": zones,
        "threat_paths": threat_paths,
        "risk_level": calculate_map_risk(signal_kinds),
    }


def build_tracks(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    tracks = []

    for event in events:
        geo = event.get("geospatial")

        if not geo:
            continue

        tracks.append(
            {
                "id": event["id"],
                "kind": event["type"],
                "lat": geo["lat"],
                "lon": geo["lon"],
                "alt": geo.get("alt"),
                "confidence": confidence_for_track(event),
                "source": event.get("source"),
                "timestamp": event.get("timestamp"),
                "label": label_for_track(event),
            }
        )

    return tracks


def build_assets(signal_kinds: set[str], event_types: set[str]) -> list[dict[str, Any]]:
    """
    Asset/adaptor status model.

    Important semantics:
    - STREAMING: adapter/feed is live and ingesting.
    - ACTIVE: physical/OSINT sensor is live and monitoring.
    - SUSPECT: asset/account path is involved in suspicious behavior.
    - ALERTING: monitoring system raised an alert condition.
    - LIVE: fusion core is running.
    """
    system_live = len(event_types) > 0

    cyber_status = "streaming" if system_live else "operational"
    physical_status = "active" if system_live else "operational"
    osint_status = "active" if system_live else "operational"

    auth_status = cyber_status
    if has_auth_threat(signal_kinds):
      auth_status = "suspect"

    edr_status = cyber_status
    if (
        "network.lateral_movement" in signal_kinds
        or "identity.privilege_escalation" in signal_kinds
    ):
        edr_status = "alerting"

    network_status = cyber_status
    if "network.data_exfiltration" in signal_kinds:
        network_status = "alerting"
    elif "network.lateral_movement" in signal_kinds:
        network_status = "suspect"

    uas_status = physical_status
    if "physical.drone_recon" in signal_kinds:
        uas_status = "alerting"

    ais_status = osint_status
    if "osint.ais_anomaly" in signal_kinds:
        ais_status = "alerting"

    return [
        {
            "id": "asset-auth-gw-01",
            "name": "AUTH SERVER",
            "kind": "auth_gateway",
            "domain": "cyber",
            "status": auth_status,
        },
        {
            "id": "asset-edr-network",
            "name": "EDR SENSOR NETWORK",
            "kind": "endpoint_detection",
            "domain": "cyber",
            "status": edr_status,
        },
        {
            "id": "asset-network-gateway",
            "name": "NETWORK GATEWAY",
            "kind": "network_gateway",
            "domain": "cyber",
            "status": network_status,
        },
        {
            "id": "asset-uas-monitoring",
            "name": "UAS MONITORING",
            "kind": "uas_sensor",
            "domain": "physical",
            "status": uas_status,
        },
        {
            "id": "asset-ais-monitoring",
            "name": "AIS MONITORING",
            "kind": "ais_feed",
            "domain": "osint",
            "status": ais_status,
        },
        {
            "id": "asset-fusion-core",
            "name": "FUSION CORE",
            "kind": "fusion_engine",
            "domain": "fusion",
            "status": "live" if system_live else "standby",
        },
    ]


def build_zones(signal_kinds: set[str], tracks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sector_b_active = (
        "physical.drone_recon" in signal_kinds
        or any(track["kind"] == "physical.drone" for track in tracks)
    )

    return [
        {
            "id": "zone-sector-b",
            "name": "Sector B",
            "risk": "critical" if sector_b_active else "normal",
            "active": sector_b_active,
            "center": {
                "lat": 37.7749,
                "lon": -122.4194,
            },
            "radius_m": 500,
        }
    ]


def build_threat_paths(
    signal_kinds: set[str],
    events: list[dict[str, Any]],
    tracks: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    paths = []

    if "auth.failed_burst" in signal_kinds or "auth.anomalous_login" in signal_kinds:
        paths.append(
            {
                "id": "path-auth-to-gateway",
                "kind": "cyber_path",
                "from": "AUTH SERVER",
                "to": "NETWORK GATEWAY",
                "active": True,
                "severity": "medium",
                "label": "Suspicious authentication path",
            }
        )

    if "network.lateral_movement" in signal_kinds:
        paths.append(
            {
                "id": "path-gateway-to-hq",
                "kind": "cyber_path",
                "from": "NETWORK GATEWAY",
                "to": "HQ NODE",
                "active": True,
                "severity": "high",
                "label": "Lateral movement path",
            }
        )

    if "physical.drone_recon" in signal_kinds:
        paths.append(
            {
                "id": "path-uas-to-sector-b",
                "kind": "physical_path",
                "from": "UAS TRACK",
                "to": "Sector B",
                "active": True,
                "severity": "critical",
                "label": "Drone approach path",
            }
        )

    if "osint.ais_anomaly" in signal_kinds:
        paths.append(
            {
                "id": "path-vessel-to-corridor",
                "kind": "osint_path",
                "from": "UNKNOWN VESSEL",
                "to": "Restricted Corridor",
                "active": True,
                "severity": "medium",
                "label": "AIS anomaly path",
            }
        )

    return paths


def calculate_map_risk(signal_kinds: set[str]) -> str:
    if "physical.drone_recon" in signal_kinds and "network.lateral_movement" in signal_kinds:
        return "critical"

    if "network.data_exfiltration" in signal_kinds:
        return "critical"

    if "network.lateral_movement" in signal_kinds:
        return "high"

    if "auth.anomalous_login" in signal_kinds:
        return "medium"

    if "auth.failed_burst" in signal_kinds:
        return "low"

    return "normal"


def has_auth_threat(signal_kinds: set[str]) -> bool:
    return (
        "auth.failed_burst" in signal_kinds
        or "auth.anomalous_login" in signal_kinds
    )


def confidence_for_track(event: dict[str, Any]) -> float:
    event_type = event.get("type")

    if event_type == "physical.drone":
        return 0.86

    if event_type == "osint.ais_anomaly":
        return 0.72

    return 0.6


def label_for_track(event: dict[str, Any]) -> str:
    event_type = event.get("type")

    if event_type == "physical.drone":
        return "UAS"

    if event_type == "osint.ais_anomaly":
        return "UNKNOWN VESSEL"

    return event.get("source", "TRACK")