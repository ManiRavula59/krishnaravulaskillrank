import { useEffect, useState } from "react";

function App() {
  const [stats, setStats] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/stats")
      .then(res => res.json())
      .then(setStats);
  }, []);

  const askAI = () => {
    fetch("http://127.0.0.1:8000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(question)
    })
      .then(res => res.json())
      .then(data => setAnswer(data.answer));
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>📊 Social Media Insight Engine</h1>

      {stats && (
        <>
          <p>Total Posts: {stats.total_posts}</p>
          <p>😊 Positive: {stats.positive}</p>
          <p>😐 Neutral: {stats.neutral}</p>
          <p>😢 Negative: {stats.negative}</p>
        </>
      )}

      <h2>🤖 Ask AI</h2>

      <input
        style={{ width: "400px", padding: "8px" }}
        value={question}
        onChange={e => setQuestion(e.target.value)}
        placeholder="Ask: which post has highest likes?"
      />

      <button onClick={askAI}>Ask</button>

      <p style={{ marginTop: "20px" }}>{answer}</p>
    </div>
  );
}

export default App;