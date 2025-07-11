// src/App.js
import React, { useState, useEffect } from 'react';
import './App.css';

let debounceTimer;

function App() {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(false);

  const handleToggleTheme = () => setDarkMode((prev) => !prev);

  const fetchPrediction = async (inputText) => {
    if (!inputText.trim()) return setResult(null);
    setLoading(true);

    const response = await fetch("http://localhost:8000/graphql", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: `
          query {
            sentiment(text: """${inputText}""") {
              label
              score
            }
          }
        `,
      }),
    });

    const data = await response.json();
    setResult(data.data?.sentiment || null);
    setLoading(false);
  };

  // Live typing inference with debounce
  useEffect(() => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      if (text.trim()) {
        fetchPrediction(text);
      } else {
        setResult(null);
      }
    }, 700); // 700ms delay
  }, [text]);

  return (
    <div className={`App ${darkMode ? 'dark' : ''}`}>
      <div className="container">
        <div className="header">
          <h2>Electronix AI – Sentiment Analysis</h2>
          <button onClick={handleToggleTheme}>
            Toggle {darkMode ? 'Light' : 'Dark'} Mode
          </button>
        </div>

        <textarea
          rows="6"
          placeholder="Start typing to analyze sentiment..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        {loading && <p>⏳ Predicting...</p>}

        {result && !loading && (
          <div className="result">
            <p><strong>Sentiment:</strong> {result.label}</p>
            <p><strong>Confidence:</strong> {result.score}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
