// components/TopBar.tsx
import { useEffect, useMemo, useState } from "react";
import "../styles/topbar.css";

type MaybePromise<T = void> = T | Promise<T>;

type Props = {
  onRunToggle: () => MaybePromise;
  onStep: () => MaybePromise;
  onReset: () => MaybePromise;
  isAutoRunning: boolean;
  isSystemRunning: boolean;
  isBusy?: boolean;
};

export default function TopBar({
  onRunToggle,
  onStep,
  onReset,
  isAutoRunning,
  isSystemRunning,
  isBusy = false,
}: Props) {
  const [now, setNow] = useState(() => new Date());
  const [startedAt, setStartedAt] = useState(() => Date.now());

  useEffect(() => {
    const interval = window.setInterval(() => {
      setNow(new Date());
    }, 1000);

    return () => window.clearInterval(interval);
  }, []);

  const runtime = useMemo(() => {
    const elapsedMs = Math.max(0, now.getTime() - startedAt);
    return formatDuration(elapsedMs);
  }, [now, startedAt]);

  const utcTime = useMemo(() => {
    return `${now.toISOString().slice(11, 19)} Z`;
  }, [now]);

  const utcDate = useMemo(() => {
    return now.toISOString().slice(0, 10).toUpperCase();
  }, [now]);

  const handleRunToggle = async () => {
    if (!isAutoRunning) {
      setStartedAt(Date.now());
    }

    await onRunToggle();
  };

  const handleStep = async () => {
    await onStep();
  };

  const handleReset = async () => {
    setStartedAt(Date.now());
    await onReset();
  };

  return (
    <header className="topbar">
      <div className="brand">
        <div className="brand-mark">♜</div>

        <div>
          <h1>SENTINEL FORGE</h1>
          <p>Multi-Domain Threat Fusion &amp; Decision Engine</p>
        </div>
      </div>

      <div className="topbar-controls">
        <button
          type="button"
          className={`control-btn start ${isAutoRunning ? "active" : ""}`}
          onClick={handleRunToggle}
          disabled={isBusy && !isAutoRunning}
        >
          {isAutoRunning ? "Ⅱ PAUSE" : "▶ START"}
        </button>

        <button
          type="button"
          className="control-btn"
          onClick={handleStep}
          disabled={isBusy || isAutoRunning}
        >
          » STEP
        </button>

        <button
          type="button"
          className="control-btn"
          onClick={handleReset}
          disabled={isBusy}
        >
          ↻ RESET
        </button>
      </div>

      <div className="runtime-status">
        <span className={`live-dot ${isSystemRunning ? "active" : ""}`} />
        <strong>{isSystemRunning ? "LIVE" : "READY"}</strong>
        <span className="runtime-clock">{runtime}</span>
      </div>

      <div className="scenario-box">
        <span>SCENARIO</span>
        <strong>Coordinated Intrusion</strong>
      </div>

      <div className="time-box">
        <span>TIME</span>
        <strong>{utcTime}</strong>
        <small>{utcDate}</small>
      </div>
    </header>
  );
}

function formatDuration(ms: number) {
  const totalSeconds = Math.floor(ms / 1000);

  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;

  return [
    String(hours).padStart(2, "0"),
    String(minutes).padStart(2, "0"),
    String(seconds).padStart(2, "0"),
  ].join(":");
}