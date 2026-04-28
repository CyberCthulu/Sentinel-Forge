# app/core/detection.py

from app.models.signal import Signal


def detect(events):
    signals = []

    # -----------------------
    # FAILED LOGIN BURST
    # -----------------------
    failed = [e for e in events if e["type"] == "auth.failed"]

    if len(failed) >= 3:
        signals.append(
            Signal(
                id="sig-failed-burst",
                kind="auth.failed_burst",
                domain="cyber",
                weight=0.18,
                evidence=[e["id"] for e in failed],
                label="Failed Authentication Burst",
                description="Multiple failed authentication attempts observed in the event window.",
                source="auth-rule",
            )
        )

    # -----------------------
    # ANOMALOUS LOGIN
    # -----------------------
    success = [e for e in events if e["type"] == "auth.success"]

    if success:
        signals.append(
            Signal(
                id="sig-anomalous-login",
                kind="auth.anomalous_login",
                domain="cyber",
                weight=0.22,
                evidence=[e["id"] for e in success],
                label="Suspicious Login",
                description="Successful login occurred after failed authentication attempts.",
                source="auth-rule",
            )
        )

    # -----------------------
    # LATERAL MOVEMENT
    # -----------------------
    lateral = [e for e in events if e["type"] == "network.lateral"]

    if lateral:
        signals.append(
            Signal(
                id="sig-lateral",
                kind="network.lateral_movement",
                domain="cyber",
                weight=0.26,
                evidence=[e["id"] for e in lateral],
                label="Rapid Lateral Movement",
                description="Movement across internal nodes suggests active intrusion behavior.",
                source="network-rule",
            )
        )

    # -----------------------
    # DRONE ACTIVITY
    # -----------------------
    drone = [e for e in events if e["type"] == "physical.drone"]

    if drone:
        latest = drone[-1]
        geo = latest.get("geospatial", {})

        signals.append(
            Signal(
                id="sig-drone",
                kind="physical.drone_recon",
                domain="physical",
                weight=0.25,
                evidence=[e["id"] for e in drone],
                label="Physical Drone Activity",
                description="Drone activity detected near protected perimeter.",
                source="physical-rule",
                location={
                    "lat": geo.get("lat"),
                    "lon": geo.get("lon"),
                },
            )
        )

    return signals


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