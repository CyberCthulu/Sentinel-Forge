import { useState } from "react";
import "../styles/incident.css";

export default function IncidentCard({ incident }: any) {
  const [open, setOpen] = useState(false);

  if (!incident) {
    return (
      <div className="panel incident-panel incident-summary empty">
        <div className="panel-header">
          <h2>INCIDENT ASSESSMENT</h2>
        </div>

        <div className="incident-empty-body">
          <h3>No active incident</h3>
          <p>System is monitoring incoming signals.</p>
        </div>
      </div>
    );
  }

  const confidence = Math.round((incident.confidence || 0) * 100);
  const factorCount = incident.why?.length || 0;
  const actionCount = incident.recommended_actions?.length || 0;

  return (
    <>
      <button
        className={`panel incident-panel incident-summary ${incident.severity}`}
        onClick={() => setOpen(true)}
      >
        <div className="panel-header">
          <h2>INCIDENT ASSESSMENT</h2>
          <span>VIEW DETAILS ›</span>
        </div>

        <div className="incident-summary-body">
          <div className="alert-icon">⚠</div>

          <div className="incident-summary-main">
            <h3>
              {incident.severity.toUpperCase()} — {incident.type.toUpperCase()}
            </h3>
            <p>{incident.summary}</p>
            <div className="incident-summary-meta">
              <span>{factorCount} key factors</span>
              <span>{actionCount} recommended actions</span>
            </div>
          </div>

          <div className="incident-confidence">
            <span>CONFIDENCE</span>
            <strong>{confidence}%</strong>
          </div>
        </div>
      </button>

      {open && (
        <div className="incident-modal-backdrop" onClick={() => setOpen(false)}>
          <div className={`incident-modal ${incident.severity}`} onClick={(e) => e.stopPropagation()}>
            <div className="incident-modal-header">
              <div>
                <span>INCIDENT ID: {incident.id}</span>
                <h2>{incident.severity.toUpperCase()} — {incident.type.toUpperCase()}</h2>
              </div>
              <button onClick={() => setOpen(false)}>×</button>
            </div>

            <p className="incident-modal-summary">{incident.summary}</p>

            <div className="incident-modal-grid">
              <section>
                <h4>KEY FACTORS</h4>
                <ul>
                  {incident.why?.map((w: string, i: number) => (
                    <li key={i}>{w}</li>
                  ))}
                </ul>
              </section>

              <section>
                <h4>RECOMMENDED ACTIONS</h4>
                <ul>
                  {incident.recommended_actions?.map((a: string, i: number) => (
                    <li key={i}>{a}</li>
                  ))}
                </ul>
              </section>

              <section>
                <h4>SIGNALS</h4>
                <ul>
                  {incident.signals?.map((s: string, i: number) => (
                    <li key={i}>{s}</li>
                  ))}
                </ul>
              </section>

              <section>
                <h4>CONFIDENCE</h4>
                <div className="modal-confidence">{confidence}%</div>
              </section>
            </div>
          </div>
        </div>
      )}
    </>
  );
}