import "../styles/logstream.css";

export default function LogStream({ events }: any) {
  return (
    <div className="panel logstream">
      <h3>EVENT STREAM</h3>

      <div className="log-list">
        {events?.map((e: any) => (
          <div key={e.id} className={`log-item ${e.domain}`}>
            <span>{e.timestamp}</span>
            <span>{e.source}</span>
            <span>{e.message}</span>
          </div>
        ))}
      </div>
    </div>
  );
}