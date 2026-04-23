import ActionList from "./ActionList";

type Props = { incident: any };

export default function IncidentCard({ incident }: Props) {
  if (!incident) return null;

  return (
    <div className="incident">
      <h2>🚨 {incident.severity}</h2>
      <p>Confidence: {incident.confidence}</p>
      <p>{incident.summary}</p>

      <h4>Why this triggered:</h4>
      <ul>
        {incident.why?.map((w: string, i: number) => (
          <li key={i}>{w}</li>
        ))}
      </ul>

      <h4>Recommended Actions:</h4>
      <ActionList actions={incident.actions || []} />
    </div>
  );
}