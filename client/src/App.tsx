import { useState } from "react";
import {
  startSimulation,
  stepSimulation,
  getState,
  resetSimulation,
} from "./services/api";

function App() {
  const [data, setData] = useState<any>(null);

  const handleStart = async () => {
    const res = await startSimulation();
    setData(res);
  };

  const handleStep = async () => {
    const res = await stepSimulation();
    setData(res);
  };

  const handleState = async () => {
    const res = await getState();
    setData(res);
  };

  const handleReset = async () => {
    const res = await resetSimulation();
    setData(res);
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Sentinel Forge</h1>

      <div style={{ marginBottom: 20 }}>
        <button onClick={handleStart}>Start</button>
        <button onClick={handleStep}>Step</button>
        <button onClick={handleState}>Get State</button>
        <button onClick={handleReset}>Reset</button>
      </div>

      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}

export default App;