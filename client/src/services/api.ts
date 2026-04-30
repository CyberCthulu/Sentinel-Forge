// services/api.ts
const BASE_URL = "http://localhost:8000";

export async function startSimulation() {
  const res = await fetch(`${BASE_URL}/simulate/start`, {
    method: "POST",
  });

  if (!res.ok) {
    throw new Error("Failed to start simulation");
  }

  return res.json();
}

export async function stepSimulation() {
  const res = await fetch(`${BASE_URL}/simulate/step`, {
    method: "POST",
  });

  if (!res.ok) {
    throw new Error("Failed to step simulation");
  }

  return res.json();
}

export async function getState() {
  const res = await fetch(`${BASE_URL}/state`);

  if (!res.ok) {
    throw new Error("Failed to fetch state");
  }

  return res.json();
}

export async function resetSimulation() {
  const res = await fetch(`${BASE_URL}/reset`, {
    method: "POST",
  });

  if (!res.ok) {
    throw new Error("Failed to reset simulation");
  }

  return res.json();
}

export async function analyzeIncident(payload: {
  correlation: any;
  incident: any;
}) {
  const res = await fetch(`${BASE_URL}/agent/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error("Failed to analyze incident");
  }

  return res.json();
}