const BASE_URL = "http://localhost:8000";

export async function generateQuiz(url) {
  const res = await fetch(`${BASE_URL}/generate_quiz`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ url }),
  });
  if (!res.ok) throw new Error("Quiz generation failed");
  return await res.json();
}

export async function getHistory() {
  const res = await fetch(`${BASE_URL}/history`);
  if (!res.ok) throw new Error("Failed to fetch history");
  return await res.json();
}

export async function getQuiz(id) {
  const res = await fetch(`${BASE_URL}/quiz/${id}`);
  if (!res.ok) throw new Error("Failed to fetch quiz");
  return await res.json();
}
