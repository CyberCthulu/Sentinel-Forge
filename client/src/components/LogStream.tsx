// components/LogStream.tsx
import { useEffect, useMemo, useRef, useState } from "react";
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
  const value = String(source || "").toUpperCase();

  if (value.includes("AUTH")) return "AUTH";
  if (value.includes("EDR")) return "EDR";
  if (value.includes("UAS")) return "UAS";
  if (value.includes("AIS")) return "AIS";
  if (value.includes("SIEM")) return "SIEM";
  if (value.includes("DEFENDER")) return "MDE";
  if (value.includes("NET")) return "NET";
  if (value.includes("FUSION")) return "FUSION";

  return "SYS";
}

function eventTone(event: any) {
  const type = String(event?.type || "").toLowerCase();
  const severity = String(event?.severity || "unknown").toLowerCase();

  const isTelemetry =
    type.includes("heartbeat") ||
    type.includes("health") ||
    type.includes("telemetry") ||
    type.startsWith("adapter.") ||
    type.startsWith("sensor.heartbeat") ||
    event?.metadata?.background === true;

  if (isTelemetry) return "telemetry";

  /*
    Explicit event semantics override generic severity.

    Source identity:
    - dot + source pill

    Event meaning/severity:
    - event message + time color
  */
  if (
    type === "auth.failed" ||
    type === "network.lateral" ||
    type === "identity.privilege_escalation" ||
    type === "network.exfiltration" ||
    type === "physical.drone" ||
    type === "osint.ais_anomaly"
  ) {
    return "alert";
  }

  if (type === "auth.success") {
    const unfamiliar =
      event?.metadata?.unfamiliar_ip === true ||
      event?.metadata?.known_source === false;

    return unfamiliar ? "suspicious" : "normal";
  }

  if (type === "node.access") {
    return event?.metadata?.rapid_sequence === true ? "suspicious" : "normal";
  }

  if (severity === "critical" || severity === "high") return "alert";
  if (severity === "medium") return "suspicious";
  if (severity === "low") return "normal";

  return "unknown";
}

function eventClassLabel(event: any) {
  const tone = eventTone(event);

  if (tone === "telemetry") return "TELEMETRY";
  if (tone === "alert") return "ALERT";
  if (tone === "suspicious") return "SUSPICIOUS";
  if (tone === "normal") return "NORMAL";

  return "EVENT";
}

function formatType(type: string) {
  return String(type || "unknown.event").replace(/_/g, " ");
}

export default function LogStream({ events }: any) {
  const [isOpen, setIsOpen] = useState(false);

  const eventListRef = useRef<HTMLDivElement | null>(null);
  const shouldAutoScrollRef = useRef(true);

  const orderedEvents = useMemo(() => {
    return Array.isArray(events) ? events : [];
  }, [events]);

  const handleEventListScroll = () => {
    const el = eventListRef.current;
    if (!el) return;

    const distanceFromBottom = el.scrollHeight - el.scrollTop - el.clientHeight;

    /*
      If operator is close to the bottom, keep following live events.
      If they scroll up to inspect older logs, pause auto-follow.
    */
    shouldAutoScrollRef.current = distanceFromBottom < 48;
  };

  useEffect(() => {
    const el = eventListRef.current;
    if (!el) return;

    if (shouldAutoScrollRef.current) {
      el.scrollTop = el.scrollHeight;
    }
  }, [orderedEvents.length]);

  useEffect(() => {
    if (!isOpen) return;

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setIsOpen(false);
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen]);

  return (
    <>
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

        <div
          ref={eventListRef}
          className="event-list"
          onScroll={handleEventListScroll}
        >
          {orderedEvents.map((event: any) => {
            const source = sourceType(event.source);
            const tone = eventTone(event);

            return (
              <div
                key={event.id}
                className={`event-row ${event.domain || "unknown"} ${tone} source-${source.toLowerCase()}`}
              >
                <span className="event-dot" />

                <span className="event-time">
                  {formatTime(event.timestamp)}
                </span>

                <span className={`source-pill ${source.toLowerCase()}`}>
                  {source}
                </span>

                <span className="event-message">{event.message}</span>
              </div>
            );
          })}
        </div>

        <button
          type="button"
          className="view-log-btn"
          onClick={() => setIsOpen(true)}
        >
          ⌘ VIEW FULL LOG
        </button>
      </div>

      {isOpen && (
        <div
          className="log-modal-backdrop"
          role="presentation"
          onMouseDown={() => setIsOpen(false)}
        >
          <section
            className="log-modal"
            role="dialog"
            aria-modal="true"
            aria-label="Full event log"
            onMouseDown={(event) => event.stopPropagation()}
          >
            <header className="log-modal-header">
              <div>
                <h2>FULL EVENT LOG</h2>
                <span>{orderedEvents.length} EVENTS CAPTURED</span>
              </div>

              <button
                type="button"
                className="log-modal-close"
                onClick={() => setIsOpen(false)}
                aria-label="Close full event log"
              >
                ×
              </button>
            </header>

            <div className="log-modal-table-head">
              <span>TIME</span>
              <span>SOURCE</span>
              <span>CLASS</span>
              <span>TYPE</span>
              <span>EVENT</span>
            </div>

            <div className="log-modal-list">
              {orderedEvents.map((event: any) => {
                const source = sourceType(event.source);
                const tone = eventTone(event);
                const label = eventClassLabel(event);

                return (
                  <div
                    key={event.id}
                    className={`log-modal-row ${tone} source-${source.toLowerCase()}`}
                  >
                    <span className="log-modal-time">
                      {formatTime(event.timestamp)}
                    </span>

                    <span className={`source-pill ${source.toLowerCase()}`}>
                      {source}
                    </span>

                    <span className={`log-modal-label ${tone}`}>{label}</span>

                    <span className="log-modal-type">
                      {formatType(event.type)}
                    </span>

                    <span className="log-modal-message">{event.message}</span>
                  </div>
                );
              })}
            </div>
          </section>
        </div>
      )}
    </>
  );
}