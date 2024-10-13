import React from 'react';
import Link from 'next/link';
import Layout from '../components/Layout';

const Home: React.FC = () => {
  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
            <span className="block">Welcome to</span>
            <span className="block text-indigo-600">AIGENT Dashboard</span>
          </h1>
          <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
            Manage your AI agents, create datasets, and process files with advanced OCR technology.
          </p>
        </div>

        <div className="mt-10">
          <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
            <Link
              href="/data-file-creation"
              className="block p-6 bg-white rounded-lg border border-gray-200 shadow-md hover:bg-gray-100">

              <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900">Data File Creation</h5>
              <p className="font-normal text-gray-700">Create and process data files using OCR technology.</p>

            </Link>
            <Link
              href="/data-set-creation"
              className="block p-6 bg-white rounded-lg border border-gray-200 shadow-md hover:bg-gray-100">

              <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900">Data Set Creation</h5>
              <p className="font-normal text-gray-700">Build and manage datasets for your AI agents.</p>

            </Link>
            <Link
              href="/agent-training"
              className="block p-6 bg-white rounded-lg border border-gray-200 shadow-md hover:bg-gray-100">

              <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900">Agent Training</h5>
              <p className="font-normal text-gray-700">Train your AI agents using various methods and datasets.</p>

            </Link>
            <Link
              href="/agent-creation"
              className="block p-6 bg-white rounded-lg border border-gray-200 shadow-md hover:bg-gray-100">

              <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900">Agent Creation</h5>
              <p className="font-normal text-gray-700">Create new AI agents with custom parameters and types.</p>

            </Link>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Home;
