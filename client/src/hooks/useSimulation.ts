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
    signals: {
      failed_logins: false,
      suspicious_login: false,
      lateral_movement: false,
      drone_activity: false,
    },
    incident: null,
  });

  const start = async () => setState(await startSimulation());
  const step = async () => setState(await stepSimulation());
  const refresh = async () => setState(await getState());
  const reset = async () => setState(await resetSimulation());

  return { state, start, step, refresh, reset };
}
