import ActionList from "./ActionList";

type Props = { incident: any };

export default function IncidentCard({ incident }: Props) {
  if (!incident) return null;

  return (
    <div style={{ border: "2px solid red", padding: 10, marginTop: 20 }}>
      <h2>{incident.severity}</h2>
      <p>Confidence: {incident.confidence}</p>
      <p>{incident.summary}</p>

      <h4>Why:</h4>
      <ul>
        {incident.why?.map((w: string, i: number) => (
          <li key={i}>{w}</li>
        ))}
      </ul>

      <h4>Actions:</h4>
      <ActionList actions={incident.actions || []} />
    </div>
  );
}