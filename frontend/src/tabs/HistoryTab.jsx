import React, { useState, useEffect } from "react";
import { getHistory, getQuiz } from "../services/api";
import HistoryTable from "../components/HistoryTable";
import Modal from "../components/Modal";
import QuizDisplay from "../components/QuizDisplay";

export default function HistoryTab() {
  const [history, setHistory] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedQuiz, setSelectedQuiz] = useState(null);

  useEffect(() => {
    getHistory().then(setHistory);
  }, []);

  const handleDetails = async (quizId) => {
    const data = await getQuiz(quizId);
    setSelectedQuiz(data);
    setModalOpen(true);
  };

  return (
    <div>
      <HistoryTable history={history} onDetails={handleDetails} />
      <Modal open={modalOpen} onClose={() => setModalOpen(false)}>
        <QuizDisplay quizData={selectedQuiz} />
      </Modal>
    </div>
  );
}
