import React, { useState } from 'react';
import Layout from '../components/Layout';
import ErrorMessage from '../components/ErrorMessage';

const AgentTraining: React.FC = () => {
  const [agentName, setAgentName] = useState('');
  const [selectedDataSet, setSelectedDataSet] = useState('');
  const [trainingMethod, setTrainingMethod] = useState('');
  const [epochs, setEpochs] = useState(10);
  const [isTraining, setIsTraining] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Mock data sets (replace with actual data from backend)
  const dataSets = ['Data Set 1', 'Data Set 2', 'Data Set 3'];

  // Mock training methods (replace with actual methods)
  const trainingMethods = ['Method A', 'Method B', 'Method C'];

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!agentName || !selectedDataSet || !trainingMethod) {
      setError('Please fill in all required fields');
      return;
    }

    setIsTraining(true);
    setError(null);
    setResult(null);

    try {
      // TODO: Implement actual agent training logic here
      await new Promise(resolve => setTimeout(resolve, 3000));
      setResult(`Agent "${agentName}" trained successfully using ${trainingMethod} on ${selectedDataSet} for ${epochs} epochs.`);
    } catch (err) {
      setError('An error occurred during agent training. Please try again.');
    } finally {
      setIsTraining(false);
    }
  };

  return (
    <Layout>
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Agent Training</h1>
        <div className="bg-white shadow-md rounded-lg p-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="agentName" className="block text-sm font-medium text-gray-700">
                Agent Name
              </label>
              <input
                type="text"
                id="agentName"
                value={agentName}
                onChange={(e) => setAgentName(e.target.value)}
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                required
              />
            </div>
            <div>
              <label htmlFor="dataSet" className="block text-sm font-medium text-gray-700">
                Select Data Set
              </label>
              <select
                id="dataSet"
                value={selectedDataSet}
                onChange={(e) => setSelectedDataSet(e.target.value)}
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                required
              >
                <option value="">Select a data set</option>
                {dataSets.map((dataSet, index) => (
                  <option key={index} value={dataSet}>{dataSet}</option>
                ))}
              </select>
            </div>
            <div>
              <label htmlFor="trainingMethod" className="block text-sm font-medium text-gray-700">
                Training Method
              </label>
              <select
                id="trainingMethod"
                value={trainingMethod}
                onChange={(e) => setTrainingMethod(e.target.value)}
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                required
              >
                <option value="">Select a training method</option>
                {trainingMethods.map((method, index) => (
                  <option key={index} value={method}>{method}</option>
                ))}
              </select>
            </div>
            <div>
              <label htmlFor="epochs" className="block text-sm font-medium text-gray-700">
                Number of Epochs
              </label>
              <input
                type="number"
                id="epochs"
                value={epochs}
                onChange={(e) => setEpochs(parseInt(e.target.value))}
                min="1"
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                required
              />
            </div>
            <button
              type="submit"
              disabled={!agentName || !selectedDataSet || !trainingMethod || isTraining}
              className="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isTraining ? 'Training...' : 'Start Training'}
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

export default AgentTraining;
