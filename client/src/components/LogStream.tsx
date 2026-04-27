//components/LogStream.tsx
import "../styles/logstream.css";

function formatTime(timestamp: string) {
  if (!timestamp) return "--:--:--";
  return new Date(timestamp).toLocaleTimeString("en-US", {
    hour12: false,
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}

function sourceType(source: string) {
  if (source?.includes("AUTH")) return "AUTH";
  if (source?.includes("EDR")) return "EDR";
  if (source?.includes("UAS")) return "UAS";
  return "SYS";
}

export default function LogStream({ events }: any) {
  return (
    <div className="panel event-stream-panel">
      <div className="panel-header">
        <h2>EVENT STREAM</h2>
        <span className="panel-filter">FILTER&nbsp; All⌄</span>
      </div>

      <div className="event-table-head">
        <span>TIME</span>
        <span>SOURCE</span>
        <span>EVENT</span>
      </div>

      <div className="event-list">
        {events?.map((e: any) => {
          const type = sourceType(e.source);

          return (
            <div key={e.id} className={`event-row ${e.domain}`}>
              <span className="event-dot" />
              <span className="event-time">{formatTime(e.timestamp)}</span>
              <span className={`source-pill ${type.toLowerCase()}`}>{type}</span>
              <span className="event-message">{e.message}</span>
            </div>
          );
        })}
      </div>

      <button className="view-log-btn">⌘ VIEW FULL LOG</button>
    </div>
  );
}