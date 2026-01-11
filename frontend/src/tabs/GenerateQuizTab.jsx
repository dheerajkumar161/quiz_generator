import React, { useState } from "react";
import { generateQuiz } from "../services/api";
import QuizDisplay from "../components/QuizDisplay";

export default function GenerateQuizTab() {
  const [url, setUrl] = useState("");
  const [quizData, setQuizData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true); setError(""); setQuizData(null);
    try {
      const res = await generateQuiz(url);
      setQuizData(res);
    } catch (err) {
      setError("Could not generate quiz. Invalid URL or server error.");
    }
    setLoading(false);
  };

  return (
    <div>
      <form onSubmit={handleSubmit} className="flex mb-3">
        <input
          className="border p-2 flex-1 rounded-l"
          placeholder="Paste Wikipedia URL"
          value={url}
          onChange={e => setUrl(e.target.value)}
          required
        />
        <button className="bg-blue-500 text-white px-4 rounded-r" disabled={loading}>
          {loading ? "Generating..." : "Generate Quiz"}
        </button>
      </form>
      {error && <div className="text-red-600 mb-2">{error}</div>}
      {quizData && <QuizDisplay quizData={quizData} />}
    </div>
  );
}
