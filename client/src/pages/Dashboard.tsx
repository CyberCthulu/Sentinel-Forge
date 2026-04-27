import "../styles/dashboard.css";

import TopBar from "../components/TopBar";
import LogStream from "../components/LogStream";
import SignalBreakdown from "../components/SignalBreakdown";
import CorrelationScore from "../components/CorrelationScore";
import IncidentCard from "../components/IncidentCard";
import MapView from "../components/MapView";
import AssetStatus from "../components/AssetStatus";

import { useSimulation } from "../hooks/useSimulation";

export default function Dashboard() {
  const { state, start, step, reset } = useSimulation();

  return (
    <div className="dashboard">
      <TopBar onStart={start} onStep={step} onReset={reset} />

      <div className="main-grid">
        <LogStream events={state.events} />
        <SignalBreakdown signals={state.signals} />

        <div className="right-panel">
          <CorrelationScore correlation={state.correlation} />
          <IncidentCard incident={state.incident} />
        </div>
      </div>

      <div className="bottom-grid">
        <MapView map={state.map_state} />
        <AssetStatus />
      </div>
    </div>
  );
}