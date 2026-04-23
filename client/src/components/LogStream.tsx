type Props = { events: any[] };

export default function LogStream({ events }: Props) {
  return (
    <div className="panel log-stream">
      {events.map((e, i) => (
        <div key={i}>
          [{new Date().toLocaleTimeString()}] {e.type} ({e.source || "mock"})
        </div>
      ))}
    </div>
  );
}