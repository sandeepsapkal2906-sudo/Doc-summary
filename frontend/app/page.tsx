'use client';

import { useState } from 'react';
import DocumentUpload from '@/components/DocumentUpload';
import SummaryDisplay from '@/components/SummaryDisplay';
import LoadingSpinner from '@/components/LoadingSpinner';

export default function Home() {
  const [summary, setSummary] = useState(null);
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [filename, setFilename] = useState('');

  const handleUpload = async (file: File) => {
    setLoading(true);
    setError('');
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await fetch('http://localhost:8080/api/upload', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error('Failed to process document');
      }
      
      const data = await response.json();
      setSummary(data.summary);
      setInsights(data.insights);
      setFilename(data.filename);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSummary(null);
    setInsights(null);
    setError('');
    setFilename('');
  };

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-slate-900 mb-3">
            📄 Document Summarizer
          </h1>
          <p className="text-lg text-slate-600">
            Upload your PDF or DOCX documents and get instant summaries with key insights
          </p>
          <p className="text-sm text-green-600 mt-2">
            ✓ All processing happens locally on your machine - completely private
          </p>
        </div>

        {/* Main Content */}
        {!summary ? (
          <DocumentUpload onUpload={handleUpload} loading={loading} error={error} />
        ) : (
          <SummaryDisplay 
            summary={summary}
            insights={insights}
            filename={filename}
            onReset={handleReset}
          />
        )}

        {loading && <LoadingSpinner />}
      </div>
    </main>
  );
}
