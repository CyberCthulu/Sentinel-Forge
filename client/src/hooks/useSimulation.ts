//hooks/useSimulation.ts
import { useEffect, useState } from "react";
import {
  startSimulation,
  stepSimulation,
  resetSimulation,
  getState,
} from "../services/api";

export function useSimulation() {
  const [state, setState] = useState({
    events: [],
    signals: [],
    correlation: null,
    incident: null,
    map_state: null,
  });

  const refresh = async () => {
    const data = await getState();
    setState(data);
  };

  const start = async () => {
    await startSimulation();
    await refresh();
  };

  const step = async () => {
    await stepSimulation();
    await refresh();
  };

  const reset = async () => {
    await resetSimulation();
    await refresh();
  };

  useEffect(() => {
    refresh();
  }, []);

  return { state, start, step, reset };
}