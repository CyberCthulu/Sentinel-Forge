# app/core/map.py


def build_map_state(events):
    tracks = []

    for e in events:
        geo = e.get("geospatial")

        if not geo:
            continue

        tracks.append(
            {
                "id": e["id"],
                "kind": e["type"],
                "lat": geo["lat"],
                "lon": geo["lon"],
                "alt": geo.get("alt"),
                "confidence": 0.8,
                "source": e.get("source"),
                "timestamp": e.get("timestamp"),
            }
        )

    return {
        "tracks": tracks,
        "assets": [
            {
                "id": "asset-auth-gw-01",
                "name": "AUTH-GW-01",
                "kind": "auth_gateway",
                "status": "operational",
                "domain": "cyber",
            },
            {
                "id": "asset-edr-01",
                "name": "EDR-01",
                "kind": "endpoint_detection",
                "status": "active",
                "domain": "cyber",
            },
            {
                "id": "asset-uas-sensor",
                "name": "UAS-SENSOR",
                "kind": "drone_sensor",
                "status": "active",
                "domain": "physical",
            },
        ],
        "zones": [
            {
                "id": "zone-sector-b",
                "name": "Sector B",
                "risk": "elevated" if tracks else "normal",
            }
        ],
        "threat_paths": [
            {
                "id": "path-coordinated-intrusion",
                "from": "AUTH-GW-01",
                "to": "Sector B",
                "active": bool(tracks),
            }
        ],
    }