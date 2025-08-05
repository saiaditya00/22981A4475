// src/App.js
import React, { useState } from 'react';
import ShortenForm from './components/ShortenForm';
import ShortenedResult from './components/ShortenedResult';

function App() {
  const [result, setResult] = useState(null);

  return (
    <div style={{ padding: '2rem' }}>
      <h1>URL Shortener</h1>
      <ShortenForm onShorten={setResult} />
      <ShortenedResult result={result} />
    </div>
  );
}

export default App;
