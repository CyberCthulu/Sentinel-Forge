type Props = { events: any[] };

export default function LogStream({ events }: Props) {
  return (
    <div>
      <h3>Logs</h3>
      {events.map((e, i) => (
        <div key={i}>
          [{e.source || "mock"}] {e.type}
        </div>
      ))}
    </div>
  );
}