import React from 'react';
import './ShortenedResult.css';



// this is a component to display the result of a shortened URL

function ShortenedResult({ result }) {
  if (!result) return null;

  return (
    <div className="shortened-result">
      <h3>Shortened URL</h3>
      <p>
        <a href={result.shortUrl} target="_blank" rel="noreferrer">
          {result.shortUrl}
        </a>
      </p>
      <p>Original URL: {result.originalUrl}</p>
      <p>Shortcode: {result.shortCode}</p>
      <p>Created At: {new Date(result.createdAt).toLocaleString()}</p>
    </div>
  );
}

export default ShortenedResult;
