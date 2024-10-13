import React, { useState } from 'react';
import Layout from '../components/Layout';
import ErrorMessage from '../components/ErrorMessage';
import FileUpload from '../components/FileUpload';

const DataFileCreation: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [ocrMethod, setOcrMethod] = useState<'google' | 'tesseract'>('google');
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [fileToken, setFileToken] = useState<string | null>(null);

  const handleFileUpload = (uploadedFile: File) => {
    setFile(uploadedFile);
    setError(null);
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!file) {
      setError('Please select a file');
      return;
    }

    setIsProcessing(true);
    setError(null);
    setResult(null);
    setFileToken(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('ocrMethod', ocrMethod);

    console.log('Submitting file:', file.name);

    try {
      const apiEndpoint = ocrMethod === 'google' ? '/api/process-ocr' : '/api/process-tesseract-ocr';
      const response = await fetch(apiEndpoint, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      console.log('Response data:', data);

      if (!response.ok) {
        throw new Error(data.error || 'OCR processing failed');
      }

      setResult(data.result);
      setFileToken(data.fileToken);
    } catch (err) {
      console.error('Error in OCR processing:', err);
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An error occurred while processing the file. Please try again.');
      }
    } finally {
      setIsProcessing(false);
    }
  };

  const handleDownload = () => {
    if (fileToken) {
      window.location.href = `/api/serve-ocr-result?token=${fileToken}`;
    }
  };

  return (
    <Layout>
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Data File Creation</h1>
        {error && (
          <div className="mb-4">
            <ErrorMessage message={error} />
          </div>
        )}
        <form onSubmit={handleSubmit} className="space-y-6">
          <FileUpload onFileUpload={handleFileUpload} />
          <div>
            <label className="block text-sm font-medium text-gray-700">OCR Method</label>
            <div className="mt-1 space-y-2">
              <div className="flex items-center">
                <input
                  id="google-ocr"
                  name="ocr-method"
                  type="radio"
                  value="google"
                  checked={ocrMethod === 'google'}
                  onChange={() => setOcrMethod('google')}
                  className="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300"
                />
                <label htmlFor="google-ocr" className="ml-3 block text-sm font-medium text-gray-700">
                  Google Cloud Vision OCR
                </label>
              </div>
              <div className="flex items-center">
                <input
                  id="tesseract-ocr"
                  name="ocr-method"
                  type="radio"
                  value="tesseract"
                  checked={ocrMethod === 'tesseract'}
                  onChange={() => setOcrMethod('tesseract')}
                  className="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300"
                />
                <label htmlFor="tesseract-ocr" className="ml-3 block text-sm font-medium text-gray-700">
                  Tesseract OCR
                </label>
              </div>
            </div>
          </div>
          <button
            type="submit"
            disabled={!file || isProcessing}
            className="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isProcessing ? 'Processing...' : 'Process File'}
          </button>
        </form>
        {result && (
          <div className="mt-6 p-4 bg-green-100 rounded-md">
            <h3 className="font-semibold text-green-800">{file?.name}</h3>
            <p className="text-green-700">{result}</p>
            {fileToken && (
              <button
                onClick={handleDownload}
                className="mt-2 inline-block px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Download OCR Result
              </button>
            )}
          </div>
        )}
      </div>
    </Layout>
  );
};

export default DataFileCreation;
