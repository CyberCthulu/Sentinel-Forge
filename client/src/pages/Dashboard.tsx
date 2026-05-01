import TopBar from "../components/TopBar";
import LogStream from "../components/LogStream";
import SignalBreakdown from "../components/SignalBreakdown";
import CorrelationScore from "../components/CorrelationScore";
import IncidentCard from "../components/IncidentCard";
import MapView from "../components/MapView";
import AssetStatus from "../components/AssetStatus";

import { useSimulation } from "../hooks/useSimulation";

export default function Dashboard() {
  const {
    state,
    step,
    reset,
    toggleRun,
    isAutoRunning,
    isSystemRunning,
    isBusy,
  } = useSimulation();

  return (
    <div className="dashboard-shell">
      <TopBar
        onRunToggle={toggleRun}
        onStep={step}
        onReset={reset}
        isAutoRunning={isAutoRunning}
        isSystemRunning={isSystemRunning}
        isBusy={isBusy}
      />

      <main className="dashboard-grid">
        <section className="dashboard-area event-area">
          <LogStream events={state.events} />
        </section>

        <section className="dashboard-area signal-area">
          <SignalBreakdown signals={state.signals} />
        </section>

        <section className="dashboard-area right-top-area">
          <CorrelationScore correlation={state.correlation} />
          <IncidentCard
            incident={state.incident}
            correlation={state.correlation}
          />
        </section>

        <section className="dashboard-area map-area">
          <MapView map={state.map_state} />
        </section>

        <section className="dashboard-area asset-area">
          <AssetStatus />
        </section>
      </main>
    </div>
  );
}