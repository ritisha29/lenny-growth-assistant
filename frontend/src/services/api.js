import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

export async function createSession(title = "New conversation") {
  const response = await api.post("/sessions", {
    title,
  });

  return response.data;
}

export async function sendMessage(sessionId, message) {
  const response = await api.post("/chat", {
    session_id: sessionId,
    message,
  });

  return response.data;
}

export async function generateShip30(
  sessionId,
  topic,
  sourceUrl = null,
) {
  const response = await api.post("/ship30", {
    session_id: sessionId,
    topic,
    source_url: sourceUrl,
  });

  return response.data;
}

export async function getArtifact(artifactId) {
  const response = await api.get(`/artifacts/${artifactId}`);

  return response.data;
}

export default api;