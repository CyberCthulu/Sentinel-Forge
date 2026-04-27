//components/TopBar.tsx
import "../styles/topbar.css";

export default function TopBar({ onStart, onStep, onReset }: any) {
  return (
    <header className="topbar">
      <div className="brand">
        <div className="brand-mark">♜</div>
        <div>
          <h1>SENTINEL FORGE</h1>
          <p>Multi-Domain Threat Fusion & Decision Engine</p>
        </div>
      </div>

      <div className="topbar-controls">
        <button className="control-btn start" onClick={onStart}>▶ START</button>
        <button className="control-btn step" onClick={onStep}>» STEP</button>
        <button className="control-btn reset" onClick={onReset}>↻ RESET</button>
      </div>

      <div className="runtime-status">
        <span className="live-dot" />
        <span>LIVE</span>
        <span className="runtime-clock">00:07:42</span>
      </div>

      <div className="scenario-box">
        <span>SCENARIO</span>
        <strong>Coordinated Intrusion</strong>
      </div>

      <div className="time-box">
        <span>TIME</span>
        <strong>14:32:18 Z</strong>
      </div>
    </header>
  );
}