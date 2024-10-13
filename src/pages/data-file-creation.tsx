import React, { useState } from 'react';
import Layout from '../components/Layout';
import ErrorMessage from '../components/ErrorMessage';
import FileUpload from '../components/FileUpload';

const DataFileCreation: React.FC = () => {
  const [files, setFiles] = useState<File[]>([]);
  const [ocrMethod, setOcrMethod] = useState<'google' | 'tesseract'>('google');
  const [isProcessing, setIsProcessing] = useState(false);
  const [results, setResults] = useState<string[]>([]);
  const [errors, setErrors] = useState<string[]>([]);
  const [downloadLinks, setDownloadLinks] = useState<string[]>([]);
  const [originalFilenames, setOriginalFilenames] = useState<string[]>([]);

  const handleFileUpload = (file: File) => {
    setFiles([file]);
    setErrors([]);
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (files.length === 0) {
      setErrors(['Please select at least one file']);
      return;
    }

    setIsProcessing(true);
    setErrors([]);
    setResults([]);
    setDownloadLinks([]);
    setOriginalFilenames([]);

    const formData = new FormData();
    files.forEach((file, index) => {
      formData.append(`file${index}`, file);
    });
    formData.append('ocrMethod', ocrMethod);

    console.log('Submitting files:', files.map(f => f.name));

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

      setResults(Array.isArray(data.results) ? data.results : [data.result]);
      setDownloadLinks(Array.isArray(data.downloadUrls) ? data.downloadUrls : [data.downloadUrl]);
      setOriginalFilenames(Array.isArray(data.originalFilenames) ? data.originalFilenames : [data.originalFilename]);
    } catch (err) {
      console.error('Error in OCR processing:', err);
      if (err instanceof Error) {
        setErrors([err.message]);
      } else {
        setErrors(['An error occurred while processing the files. Please try again.']);
      }
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <Layout>
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Data File Creation</h1>
        {errors.length > 0 && (
          <div className="mb-4">
            {errors.map((error, index) => (
              <ErrorMessage key={index} message={error} />
            ))}
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
            disabled={files.length === 0 || isProcessing}
            className="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isProcessing ? 'Processing...' : 'Process Files'}
          </button>
        </form>
        {results.length > 0 && (
          <div className="mt-6 space-y-4">
            {results.map((result, index) => (
              <div key={index} className="p-4 bg-green-100 rounded-md">
                <p className="text-green-700">{result}</p>
                {downloadLinks[index] && (
                  <a
                    href={downloadLinks[index]}
                    download={`${originalFilenames[index]}_ocr_result.md`}
                    className="mt-2 inline-block px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    Download OCR Result
                  </a>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </Layout>
  );
};

export default DataFileCreation;
