function QuizModal({ data, onClose }) {
  return (
    <div className="modal-bg">
      <div className="modal">
        <button className="close-btn" onClick={onClose}>X</button>
        <h2>{data.title}</h2>
        <p><b>Summary:</b> {data.summary}</p>

        {data.quiz.map((q, idx) => (
          <div key={idx} className="question-box">
            <p><b>Q{idx+1}:</b> {q.question}</p>
            <ul>
              {q.options.map((o,i) => <li key={i}>{o}</li>)}
            </ul>
            <p><b>Answer:</b> {q.answer}</p>
            <p><b>Explanation:</b> {q.explanation}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default QuizModal;
