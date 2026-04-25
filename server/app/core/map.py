def build_map_state(events):
    tracks = []

    for e in events:
        geo = e.get("geospatial")

        if not geo:
            continue

        tracks.append({
            "id": e["id"],
            "kind": e["type"],  # can refine later
            "lat": geo["lat"],
            "lon": geo["lon"],
            "alt": geo.get("alt"),
            "confidence": 0.8,  # simple for now
            "source": e.get("source"),
        })

    return {
        "tracks": tracks
    }