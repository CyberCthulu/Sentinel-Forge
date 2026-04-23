const BASE_URL = "http://localhost:8000";

export async function startSimulation() {
  const res = await fetch(`${BASE_URL}/simulate/start`, {
    method: "POST",
  });
  return res.json();
}

export async function stepSimulation() {
  const res = await fetch(`${BASE_URL}/simulate/step`, {
    method: "POST",
  });
  return res.json();
}

export async function getState() {
  const res = await fetch(`${BASE_URL}/state`);
  return res.json();
}

export async function resetSimulation() {
  const res = await fetch(`${BASE_URL}/reset`, {
    method: "POST",
  });
  return res.json();
}