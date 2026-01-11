import React from "react";

export default function QuizDisplay({ quizData, hideAnswers = false }) {
  if (!quizData) return null;
  const { title, summary, key_entities, sections, quiz, related_topics } = quizData;
  return (
    <div className="p-4 bg-white rounded shadow space-y-4">
      <h2 className="text-2xl font-bold">{title}</h2>
      <p className="text-gray-700 mb-2">{summary}</p>
      <div className="mb-2">
        <strong>Entities:</strong>
        <ul className="list-disc list-inside">
          {key_entities.people.length > 0 && <li><b>People:</b> {key_entities.people.join(", ")}</li>}
          {key_entities.organizations.length > 0 && <li><b>Organizations:</b> {key_entities.organizations.join(", ")}</li>}
          {key_entities.locations.length > 0 && <li><b>Locations:</b> {key_entities.locations.join(", ")}</li>}
        </ul>
      </div>
      <div>
        <strong>Sections:</strong> <span>{sections.join(", ")}</span>
      </div>
      <div>
        <h3 className="font-semibold mt-2">Quiz Questions:</h3>
        {quiz.map((q, idx) => (
          <div key={idx} className="my-3 p-3 bg-gray-50 rounded border">
            <b>Q{idx+1}:</b> {q.question}
            <ul className="list-disc list-inside ml-6">
              {q.options.map((opt, i) => (
                <li key={i}>{String.fromCharCode(65+i)}. {opt}</li>
              ))}
            </ul>
            {!hideAnswers && (
              <>
                <div className="text-green-600 mt-1">Correct: <b>{q.answer}</b> [{q.difficulty}]</div>
                <div className="text-xs text-gray-600">{q.explanation}</div>
              </>
            )}
          </div>
        ))}
      </div>
      <div>
        <b>Suggested topics:</b> {related_topics.join(", ")}
      </div>
    </div>
  );
}
