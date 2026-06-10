'use client';

import { useCallback } from 'react';
import { Upload, AlertCircle } from 'lucide-react';

interface DocumentUploadProps {
  onUpload: (file: File) => void;
  loading: boolean;
  error: string;
}

export default function DocumentUpload({ onUpload, loading, error }: DocumentUploadProps) {
  const handleFileChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const isValidType = file.type === 'application/pdf' || 
                         file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' ||
                         file.name.endsWith('.pdf') ||
                         file.name.endsWith('.docx');
      
      if (!isValidType) {
        alert('Please upload a PDF or DOCX file');
        return;
      }
      
      onUpload(file);
    }
  }, [onUpload]);

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.currentTarget.classList.add('border-blue-500', 'bg-blue-50');
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.currentTarget.classList.remove('border-blue-500', 'bg-blue-50');
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.currentTarget.classList.remove('border-blue-500', 'bg-blue-50');
    
    const file = e.dataTransfer.files?.[0];
    if (file) {
      const isValidType = file.type === 'application/pdf' || 
                         file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' ||
                         file.name.endsWith('.pdf') ||
                         file.name.endsWith('.docx');
      
      if (!isValidType) {
        alert('Please upload a PDF or DOCX file');
        return;
      }
      
      onUpload(file);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className="card border-2 border-dashed border-slate-300 transition-colors cursor-pointer hover:border-blue-400"
      >
        <div className="card-body py-12 text-center">
          <Upload className="w-16 h-16 mx-auto mb-4 text-slate-400" />
          
          <h2 className="text-2xl font-semibold text-slate-900 mb-2">
            Upload Your Document
          </h2>
          
          <p className="text-slate-600 mb-6">
            Drag and drop your PDF or DOCX file here, or click to select
          </p>
          
          <label className="btn-primary cursor-pointer inline-block">
            {loading ? 'Processing...' : 'Select File'}
            <input
              type="file"
              accept=".pdf,.docx"
              onChange={handleFileChange}
              disabled={loading}
              className="hidden"
            />
          </label>
          
          <p className="text-xs text-slate-500 mt-4">
            Supported formats: PDF, DOCX • Max size: 50MB
          </p>
        </div>
      </div>

      {error && (
        <div className="mt-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-semibold text-red-900">Error</h3>
            <p className="text-red-800 text-sm">{error}</p>
          </div>
        </div>
      )}
    </div>
  );
}
