//components/LogStream.tsx

export default function LogStream({ events }: any) {
  return (
    <div className="panel logstream">
      <h3>EVENT STREAM</h3>

      <div className="log-list">
        {events?.map((e: any) => (
          <div key={e.id} className={`event ${e.domain}`}>
            <span className="time">{e.timestamp}</span>
            <span className="source">{e.source}</span>
            <span className="message">{e.message}</span>
          </div>
        ))}
      </div>
    </div>
  );
}