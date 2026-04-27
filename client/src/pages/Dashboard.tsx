//pages/Dashboard.tsx
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
    <div className="dashboard-shell">
      <TopBar onStart={start} onStep={step} onReset={reset} />

      <main className="dashboard-grid">
        <section className="left-column">
          <LogStream events={state.events} />
        </section>

        <section className="middle-column">
          <SignalBreakdown signals={state.signals} />
          <MapView map={state.map_state} />
        </section>

        <section className="right-column">
          <CorrelationScore correlation={state.correlation} />
          <IncidentCard incident={state.incident} />
          <AssetStatus />
        </section>
      </main>

      <footer className="dashboard-footer">
        <span>SENTINEL FORGE v1.0.0</span>
        <span>ENGINE: LEGACY FUSION ARCHITECTURE</span>
        <span>MODE: REAL-TIME ●</span>
        <span>HEALTH: OPERATIONAL</span>
        <span>BUILT FOR THE WARFIGHTER</span>
      </footer>
    </div>
  );
}