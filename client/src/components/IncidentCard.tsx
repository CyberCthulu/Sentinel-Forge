//components/IncidentCard.tsx

export default function IncidentCard({ incident }: any) {
  if (!incident) return <div className="panel">No Incident</div>;

  return (
    <div className="panel incident critical">
      <h2>{incident.type}</h2>
      <p>{incident.summary}</p>

      <div className="actions">
        {incident.recommended_actions.map((a: string, i: number) => (
          <div key={i}>{a}</div>
        ))}
      </div>
    </div>
  );
}