import { useState } from "react";
import TabGenerate from "./components/TabGenerate";
import TabHistory from "./components/TabHistory";
import "./App.css";

function App() {
  const [activeTab, setActiveTab] = useState("generate");

  return (
    <div className="container">
      <h1 className="title">DeepKlarity - AI Wiki Quiz Generator</h1>

      <div className="tabs">
        <button
          className={activeTab === "generate" ? "active" : ""}
          onClick={() => setActiveTab("generate")}
        >
          Generate Quiz
        </button>

        <button
          className={activeTab === "history" ? "active" : ""}
          onClick={() => setActiveTab("history")}
        >
          Past Quizzes
        </button>
      </div>

      {activeTab === "generate" ? <TabGenerate /> : <TabHistory />}
    </div>
  );
}

export default App;
