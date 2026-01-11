import React, { useState } from "react";
import GenerateQuizTab from "./tabs/GenerateQuizTab";
import HistoryTab from "./tabs/HistoryTab";

const TABS = ["Generate Quiz", "Past Quizzes"];

export default function App() {
  const [active, setActive] = useState(0);

  return (
    <div className="bg-gray-100 min-h-screen p-6">
      <div className="max-w-3xl mx-auto bg-white rounded shadow p-4">
        <div className="flex border-b mb-4">
          {TABS.map((tab, idx) => (
            <button
              key={tab}
              className={`px-4 py-2 ${active === idx ? "border-b-2 border-blue-500 font-semibold" : "text-gray-500"}`}
              onClick={() => setActive(idx)}
            >{tab}</button>
          ))}
        </div>
        {active === 0 ? <GenerateQuizTab /> : <HistoryTab />}
      </div>
    </div>
  );
}
