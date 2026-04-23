import { useState } from "react";
import {
  startSimulation,
  stepSimulation,
  getState,
  resetSimulation,
} from "../services/api";

export function useSimulation() {
  const [state, setState] = useState<any>({
    events: [],
    incident: null,
  });

  const start = async () => setState(await startSimulation());
  const step = async () => setState(await stepSimulation());
  const refresh = async () => setState(await getState());
  const reset = async () => setState(await resetSimulation());

  return { state, start, step, refresh, reset };
}