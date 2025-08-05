// src/components/ShortenForm.js
import React, { useState } from 'react';
import axios from 'axios';
import './ShortenForm.css';



function ShortenForm({ onShorten }) {
  const [url, setUrl] = useState('');
  const [customCode, setCustomCode] = useState('');
  const [expiresAt, setExpiresAt] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const payload = {
        url,
        customCode,
        expiresAt: expiresAt ? new Date(expiresAt).toISOString() : undefined,
        generateQR: false  // Optional
      };

      const res = await axios.post('http://localhost:5000/api/v1/urls/shorten', payload);
      onShorten(res.data.data);
      setUrl('');
      setCustomCode('');
      setExpiresAt('');
    } catch (err) {
      setError(err.response?.data?.error || 'Something went wrong');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="url"
        placeholder="Enter long URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        required
      />
      <input
        type="text"
        placeholder="Custom shortcode (optional)"
        value={customCode}
        onChange={(e) => setCustomCode(e.target.value)}
      />
      <input
        type="datetime-local"
        value={expiresAt}
        onChange={(e) => setExpiresAt(e.target.value)}
      />
      <button type="submit">Shorten</button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </form>
  );
}

export default ShortenForm;
