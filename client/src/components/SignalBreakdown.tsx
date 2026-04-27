//components/SignalBreakdown.tsx

export default function SignalBreakdown({ signals }: any) {
  return (
    <div className="panel signals">
      <h3>SIGNAL BREAKDOWN</h3>

      {signals?.map((s: any) => (
        <div key={s.id} className="signal">
          <span>{s.label}</span>
          <span className="active">ACTIVE</span>
          <span>{s.evidence.length}</span>
        </div>
      ))}
    </div>
  );
}