import { useState } from "react";
import axios from "axios";
import QuizCard from "./QuizCard";

function TabGenerate() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:8000/api/generate_quiz", { url });
      setResult(res.data);
    } catch (err) {
      alert("Error generating quiz");
    }
    setLoading(false);
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Enter Wikipedia URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        className="input-box"
      />
      <button onClick={handleGenerate} disabled={loading} className="btn">
        {loading ? "Generating..." : "Generate Quiz"}
      </button>

      {result && <QuizCard data={result} />}
    </div>
  );
}

export default TabGenerate;
