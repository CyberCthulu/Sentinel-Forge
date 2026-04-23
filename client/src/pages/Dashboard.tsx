import { useSimulation } from "../hooks/useSimulation";
import LogStream from "../components/LogStream";
import IncidentCard from "../components/IncidentCard";

export default function Dashboard() {
  const { state, start, step, reset } = useSimulation();

  return (
    <div style={{ padding: 20 }}>
      <h1>Sentinel Forge</h1>

      <div style={{ marginBottom: 20 }}>
        <button onClick={start}>Start</button>
        <button onClick={step}>Step</button>
        <button onClick={reset}>Reset</button>
      </div>

      <LogStream events={state.events} />
      <IncidentCard incident={state.incident} />
    </div>
  );
}