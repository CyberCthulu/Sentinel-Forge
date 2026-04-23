type Signals = Record<string, boolean>;

type SignalBreakdownProps = {
  signals: Signals;
};

const formatSignalName = (name: string) =>
  name
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");

export default function SignalBreakdown({ signals }: SignalBreakdownProps) {
  const entries = Object.entries(signals || {});

  return (
    <div>
      <h3>Signals</h3>
      {entries.length === 0 ? (
        <div>No signals yet.</div>
      ) : (
        <ul className="signal-list">
          {entries.map(([name, active]) => (
            <li key={name} className="signal-item">
              {active ? "✅" : "⬜"} {formatSignalName(name)}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
