import { useSimulation } from "../hooks/useSimulation";
import LogStream from "../components/LogStream";
import IncidentCard from "../components/IncidentCard";
import SignalBreakdown from "../components/SignalBreakdown";
import { useEffect, useState } from "react";
import "../App.css";

export default function Dashboard() {
  const { state, start, step, reset } = useSimulation();
  const [auto, setAuto] = useState(false);

  useEffect(() => {
    if (!auto) return;
    const interval = setInterval(step, 800);
    return () => clearInterval(interval);
  }, [auto]);

  return (
    <div className="app">
      <h1 className="header">Sentinel Forge</h1>

      <div className="controls">
        <button className="button" onClick={start}>Start</button>
        <button className="button" onClick={step}>Step</button>
        <button className="button" onClick={() => setAuto(!auto)}>
          {auto ? "Stop Auto" : "Auto"}
        </button>
        <button className="button" onClick={reset}>Reset</button>
      </div>

      <div className="main">
        <div className="left-panel panel">
          <LogStream events={state.events} />
        </div>

        <div className="right-panel panel">
          <SignalBreakdown signals={state.signals} />
        </div>
      </div>

      <IncidentCard incident={state.incident} />
    </div>
  );
}