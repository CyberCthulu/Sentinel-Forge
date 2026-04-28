import { useState } from "react";
import "../styles/incident.css";

export default function IncidentCard({ incident }: any) {
  const [open, setOpen] = useState(false);

  if (!incident) {
    return (
      <div className="panel incident-panel empty">
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

  return (
    <>
      <button
        type="button"
        className={`panel incident-panel incident-clickable ${incident.severity}`}
        onClick={() => setOpen(true)}
      >
        <div className="panel-header">
          <h2>INCIDENT ASSESSMENT</h2>
          <span className="incident-status">STATUS: ACTIVE</span>
        </div>

        <div className="incident-hero">
          <div className="alert-icon">⚠</div>

          <div className="incident-main">
            <h3>
              {incident.severity.toUpperCase()} — {incident.type.toUpperCase()}
            </h3>
            <p>{incident.summary}</p>
          </div>

          <div className="incident-confidence">
            <span>CONFIDENCE</span>
            <strong>{confidence}%</strong>
          </div>
        </div>

        <div className="incident-details">
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
        </div>
      </button>

      {open && (
        <div
          className="incident-modal-backdrop"
          onClick={() => setOpen(false)}
        >
          <div
            className={`incident-modal ${incident.severity}`}
            onClick={(e) => e.stopPropagation()}
          >
            <div className="incident-modal-header">
              <div>
                <span>INCIDENT ID: {incident.id}</span>
                <h2>
                  {incident.severity.toUpperCase()} —{" "}
                  {incident.type.toUpperCase()}
                </h2>
              </div>

              <button type="button" onClick={() => setOpen(false)}>
                ×
              </button>
            </div>

            <div className="incident-modal-summary">
              <p>{incident.summary}</p>

              <div className="incident-modal-confidence">
                <span>CONFIDENCE</span>
                <strong>{confidence}%</strong>
              </div>
            </div>

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
                <h4>CONTRIBUTING SIGNALS</h4>
                <ul>
                  {incident.signals?.map((s: string, i: number) => (
                    <li key={i}>{s}</li>
                  ))}
                </ul>
              </section>

              <section>
                <h4>OPERATOR SUMMARY</h4>
                <p>
                  Sentinel Forge correlated the available signals into a staged
                  threat assessment. The current classification reflects signal
                  confidence, domain coverage, and escalation pattern.
                </p>
              </section>
            </div>
          </div>
        </div>
      )}
    </>
  );
}