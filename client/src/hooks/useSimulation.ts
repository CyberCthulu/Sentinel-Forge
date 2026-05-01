// hooks/useSimulation.ts
import { useEffect, useRef, useState } from "react";
import {
  startSimulation,
  stepSimulation,
  resetSimulation,
  getState,
} from "../services/api";

type SimulationState = {
  events: any[];
  signals: any[];
  correlation: any;
  incident: any;
  map_state: any;
  meta?: {
    mode?: string;
    step?: number;
    status?: "idle" | "running" | "complete" | string;
  };
};

const INITIAL_STATE: SimulationState = {
  events: [],
  signals: [],
  correlation: null,
  incident: null,
  map_state: null,
  meta: {
    mode: "demo",
    step: 0,
    status: "idle",
  },
};

const AUTO_STEP_MS = 900;

export function useSimulation() {
  const [state, setState] = useState<SimulationState>(INITIAL_STATE);
  const [isAutoRunning, setIsAutoRunning] = useState(false);
  const [isBusy, setIsBusy] = useState(false);

  const stateRef = useRef<SimulationState>(INITIAL_STATE);
  const stepInFlightRef = useRef(false);

  const applyState = (nextState: SimulationState) => {
    stateRef.current = nextState;
    setState(nextState);
  };

  const refresh = async () => {
    const data = await getState();
    applyState(data);
    return data;
  };

  const start = async () => {
    setIsBusy(true);

    try {
      const data = await startSimulation();
      applyState(data);
      setIsAutoRunning(true);
      return data;
    } finally {
      setIsBusy(false);
    }
  };

  const pause = () => {
    setIsAutoRunning(false);
  };

  const step = async () => {
    if (stepInFlightRef.current) return stateRef.current;

    stepInFlightRef.current = true;
    setIsBusy(true);

    try {
      const data = await stepSimulation();
      applyState(data);

      if (data?.meta?.status === "complete") {
        setIsAutoRunning(false);
      }

      return data;
    } finally {
      stepInFlightRef.current = false;
      setIsBusy(false);
    }
  };

  const reset = async () => {
    setIsBusy(true);

    try {
      setIsAutoRunning(false);
      const data = await resetSimulation();
      applyState(data);
      return data;
    } finally {
      setIsBusy(false);
    }
  };

  const toggleRun = async () => {
    if (isAutoRunning) {
      pause();
      return;
    }

    const currentStatus = stateRef.current?.meta?.status;

    if (currentStatus === "running") {
      setIsAutoRunning(true);
      return;
    }

    await start();
  };

  useEffect(() => {
    refresh();
  }, []);

  useEffect(() => {
    if (!isAutoRunning) return;

    const interval = window.setInterval(async () => {
      const currentStatus = stateRef.current?.meta?.status;

      if (currentStatus === "complete") {
        setIsAutoRunning(false);
        return;
      }

      await step();
    }, AUTO_STEP_MS);

    return () => window.clearInterval(interval);
  }, [isAutoRunning]);

  const systemStatus = state?.meta?.status ?? "idle";
  const isSystemRunning = systemStatus === "running";

  return {
    state,
    start,
    step,
    reset,
    toggleRun,
    isAutoRunning,
    isSystemRunning,
    isBusy,
  };
}