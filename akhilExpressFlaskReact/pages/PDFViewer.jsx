import React, { useState } from 'react';
import { fetchPDF } from 'C:/Users/Akhil/OneDrive/Documents/ShallowSeek/doodlegyan/src/pages/api.jsx';
import './PDFViewer.css';

function PDFViewer() {
  const [pdfUrl, setPdfUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFetchPDF = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const url = await fetchPDF();
      setPdfUrl(url);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <button onClick={handleFetchPDF} disabled={isLoading}>
        {isLoading ? 'Generating PDF...' : 'Fetch PDF'}
      </button>
      {error && <p>Error: {error}</p>}
      {pdfUrl && (
        <iframe
          src={pdfUrl}
          width="100%"
          height="600px"
          title="PDF Viewer"
        ></iframe>
      )}
    </div>
  );
}

export default PDFViewer;