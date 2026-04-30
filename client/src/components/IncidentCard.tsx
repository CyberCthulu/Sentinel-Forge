import { useState } from "react";
import { analyzeIncident } from "../services/api";
import "../styles/incident.css";

export default function IncidentCard({ incident, correlation }: any) {
  const [open, setOpen] = useState(false);
  const [agent, setAgent] = useState<any>(null);
  const [agentLoading, setAgentLoading] = useState(false);
  const [agentError, setAgentError] = useState<string | null>(null);

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

  const handleOpen = () => {
    setOpen(true);
    setAgent(null);
    setAgentError(null);
    setAgentLoading(false);
  };

  const handleAskAnalyst = async () => {
    setAgentLoading(true);
    setAgentError(null);

    try {
      const result = await analyzeIncident({
        correlation,
        incident,
      });

      setAgent(result.agent);
    } catch (error) {
      console.error(error);
      setAgentError("Sentinel Analyst is unavailable. Try again.");
    } finally {
      setAgentLoading(false);
    }
  };

  return (
    <>
      <button
        type="button"
        className={`panel incident-panel incident-clickable ${incident.severity}`}
        onClick={handleOpen}
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
        <div className="incident-modal-backdrop" onClick={() => setOpen(false)}>
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

              <section className="analyst-section">
                <div className="analyst-section-header">
                  <div>
                    <h4>SENTINEL ANALYST</h4>
                    <p>Operator-invoked decision support.</p>
                  </div>

                  <button
                    type="button"
                    className="analyst-btn"
                    onClick={handleAskAnalyst}
                    disabled={agentLoading}
                  >
                    {agentLoading ? "ANALYZING..." : "ASK ANALYST"}
                  </button>
                </div>

                {agentError && <p className="analyst-error">{agentError}</p>}

                {agentLoading && (
                  <div className="analyst-loading">
                    Sentinel Analyst is evaluating the incident context...
                  </div>
                )}

                {agent && (
                  <div className="analyst-output">
                    <div className="analyst-meta">
                      <span>PROVIDER: {agent.provider}</span>
                      <span>WINDOW: {agent.decision_window}</span>
                    </div>

                    <h5>{agent.assessment}</h5>

                    <p>
                      <strong>Why it matters:</strong> {agent.why_it_matters}
                    </p>

                    <p>
                      <strong>Operator note:</strong> {agent.operator_note}
                    </p>

                    <p>
                      <strong>Confidence rationale:</strong>{" "}
                      {agent.confidence_rationale}
                    </p>

                    <div>
                      <strong>Next steps:</strong>
                      <ul>
                        {agent.next_steps?.map((step: string, i: number) => (
                          <li key={i}>{step}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                )}
              </section>
            </div>
          </div>
        </div>
      )}
    </>
  );
}