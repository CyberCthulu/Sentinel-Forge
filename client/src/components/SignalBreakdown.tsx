//components/SignalBreakdown.tsx

const SIGNAL_LABELS: Record<string, string> = {
  "auth.failed_burst": "FAILED_AUTH_BURST",
  "auth.anomalous_login": "ANOMALOUS_LOGIN",
  "network.lateral_movement": "LATERAL_MOVEMENT",
  "physical.drone_recon": "DRONE_ACTIVITY",
};

const SIGNAL_DESCRIPTIONS: Record<string, string> = {
  "auth.failed_burst": "Multiple failed logins in short window",
  "auth.anomalous_login": "Login from unfamiliar source",
  "network.lateral_movement": "Internal movement across hosts",
  "physical.drone_recon": "Drone in restricted area",
};

export default function SignalBreakdown({ signals }: any) {
  const activeCount = signals?.length || 0;

  return (
    <div className="panel signal-panel">
      <div className="panel-header">
        <h2>SIGNAL BREAKDOWN</h2>
        <span className="active-count">{activeCount} / 12 ACTIVE</span>
      </div>

      <div className="signal-table-head">
        <span>SIGNAL</span>
        <span>STATUS</span>
        <span>EVIDENCE</span>
      </div>

      <div className="signal-list">
        {signals?.map((s: any) => {
          const evidenceCount = s.evidence?.length || 0;
          const width = Math.min(100, evidenceCount * 32);

          return (
            <div key={s.id} className={`signal-row ${s.domain}`}>
              <div className="signal-icon">●</div>

              <div className="signal-main">
                <strong>{SIGNAL_LABELS[s.kind] || s.kind}</strong>
                <span>{SIGNAL_DESCRIPTIONS[s.kind] || s.label}</span>
              </div>

              <div className="signal-status">ACTIVE</div>

              <div className="signal-evidence">
                <span>{evidenceCount}</span>
                <div className="evidence-bar">
                  <div style={{ width: `${width}%` }} />
                </div>
              </div>
            </div>
          );
        })}

        {["MALWARE_SIGNATURE", "PORT_SCAN", "BEACONING_ACTIVITY", "INSIDER_THREAT", "PHYSICAL_BREACH", "AIS_ANOMALY"].map((name) => (
          <div key={name} className="signal-row inactive">
            <div className="signal-icon">○</div>
            <div className="signal-main">
              <strong>{name}</strong>
              <span>No matching indicator detected</span>
            </div>
            <div className="signal-status">INACTIVE</div>
            <div className="signal-evidence">
              <span>0</span>
              <div className="evidence-bar" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}