import React, { useState } from 'react';
import Layout from '../components/Layout';
import FileUpload from '../components/FileUpload';
import ErrorMessage from '../components/ErrorMessage';

const DataSetCreation: React.FC = () => {
  const [dataSetName, setDataSetName] = useState('');
  const [description, setDescription] = useState('');
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [isCreating, setIsCreating] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = (file: File) => {
    setSelectedFiles(prevFiles => [...prevFiles, file]);
    setError(null);
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!dataSetName || selectedFiles.length === 0) {
      setError('Please provide a data set name and select at least one file');
      return;
    }

    setIsCreating(true);
    setError(null);
    setResult(null);

    try {
      // TODO: Implement actual data set creation logic here
      await new Promise(resolve => setTimeout(resolve, 2000));
      setResult(`Created data set "${dataSetName}" with ${selectedFiles.length} files`);
    } catch (err) {
      setError('An error occurred while creating the data set. Please try again.');
    } finally {
      setIsCreating(false);
    }
  };

  return (
    <Layout>
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Data Set Creation</h1>
        <div className="bg-white shadow-md rounded-lg p-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="dataSetName" className="block text-sm font-medium text-gray-700">
                Data Set Name
              </label>
              <input
                type="text"
                id="dataSetName"
                value={dataSetName}
                onChange={(e) => setDataSetName(e.target.value)}
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                required
              />
            </div>
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                Description
              </label>
              <textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={3}
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Add Files to Data Set
              </label>
              <FileUpload onFileUpload={handleFileUpload} />
            </div>
            {selectedFiles.length > 0 && (
              <div>
                <h3 className="text-sm font-medium text-gray-700 mb-2">Selected Files:</h3>
                <ul className="mt-1 text-sm text-gray-500 bg-gray-50 rounded-md p-2">
                  {selectedFiles.map((file, index) => (
                    <li key={index} className="truncate">{file.name}</li>
                  ))}
                </ul>
              </div>
            )}
            <button
              type="submit"
              disabled={!dataSetName || selectedFiles.length === 0 || isCreating}
              className="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isCreating ? 'Creating...' : 'Create Data Set'}
            </button>
          </form>
          {error && <ErrorMessage message={error} />}
          {result && (
            <div className="mt-6 p-4 bg-green-100 rounded-md">
              <p className="text-green-700">{result}</p>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default DataSetCreation;
