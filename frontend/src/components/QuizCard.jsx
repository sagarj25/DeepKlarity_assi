function QuizCard({ data }) {
  return (
    <div className="quiz-card">
      <h2>{data.title}</h2>
      <p><b>Summary:</b> {data.summary}</p>

      <h3>Quiz</h3>
      {data.quiz.map((q, idx) => (
        <div key={idx} className="question-box">
          <p><b>Q{idx+1}:</b> {q.question}</p>
          <ul>
            {q.options.map((o,i) => <li key={i}>{o}</li>)}
          </ul>
          <p><b>Answer:</b> {q.answer}</p>
          <p><b>Explanation:</b> {q.explanation}</p>
          <p><b>Difficulty:</b> {q.difficulty}</p>
        </div>
      ))}

      <h3>Related Topics</h3>
      <ul>
        {data.related_topics.map((t,i)=><li key={i}>{t}</li>)}
      </ul>
    </div>
  );
}

export default QuizCard;
