import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import Layout from '../components/Layout';

const AgentCreation: React.FC = () => {
  // Mock agent types (replace with actual types from backend)
  const agentTypes = ['Conversational', 'Task-oriented', 'Analytical'];

  const validationSchema = Yup.object().shape({
    agentName: Yup.string()
      .required('Agent name is required')
      .min(3, 'Agent name must be at least 3 characters'),
    agentType: Yup.string()
      .required('Agent type is required')
      .oneOf(agentTypes, 'Invalid agent type'),
    description: Yup.string()
      .max(500, 'Description must not exceed 500 characters'),
    parameters: Yup.string()
      .test('is-json', 'Parameters must be valid JSON', (value) => {
        if (!value) return true;
        try {
          JSON.parse(value);
          return true;
        } catch {
          return false;
        }
      }),
  });

  const handleSubmit = async (values: any, { setSubmitting, setStatus }: any) => {
    try {
      // TODO: Implement actual agent creation logic here
      await new Promise(resolve => setTimeout(resolve, 2000));
      setStatus({ success: `Agent "${values.agentName}" of type ${values.agentType} created successfully.` });
    } catch (err) {
      setStatus({ error: 'An error occurred while creating the agent. Please try again.' });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Layout>
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Agent Creation</h1>
        <div className="bg-white shadow-md rounded-lg p-6">
          <Formik
            initialValues={{ agentName: '', agentType: '', description: '', parameters: '' }}
            validationSchema={validationSchema}
            onSubmit={handleSubmit}
          >
            {({ isSubmitting, status }) => (
              <Form className="space-y-6">
                <div>
                  <label htmlFor="agentName" className="block text-sm font-medium text-gray-700">
                    Agent Name
                  </label>
                  <Field
                    type="text"
                    id="agentName"
                    name="agentName"
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                  <ErrorMessage name="agentName" component="div" className="mt-1 text-sm text-red-600" />
                </div>
                <div>
                  <label htmlFor="agentType" className="block text-sm font-medium text-gray-700">
                    Agent Type
                  </label>
                  <Field
                    as="select"
                    id="agentType"
                    name="agentType"
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  >
                    <option value="">Select an agent type</option>
                    {agentTypes.map((type, index) => (
                      <option key={index} value={type}>{type}</option>
                    ))}
                  </Field>
                  <ErrorMessage name="agentType" component="div" className="mt-1 text-sm text-red-600" />
                </div>
                <div>
                  <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                    Description
                  </label>
                  <Field
                    as="textarea"
                    id="description"
                    name="description"
                    rows={3}
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                  <ErrorMessage name="description" component="div" className="mt-1 text-sm text-red-600" />
                </div>
                <div>
                  <label htmlFor="parameters" className="block text-sm font-medium text-gray-700">
                    Parameters (JSON format)
                  </label>
                  <Field
                    as="textarea"
                    id="parameters"
                    name="parameters"
                    rows={4}
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    placeholder='{"key": "value"}'
                  />
                  <ErrorMessage name="parameters" component="div" className="mt-1 text-sm text-red-600" />
                </div>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isSubmitting ? 'Creating...' : 'Create Agent'}
                </button>
                {status && status.success && (
                  <div className="mt-3 p-3 bg-green-100 text-green-700 rounded-md">
                    {status.success}
                  </div>
                )}
                {status && status.error && (
                  <div className="mt-3 p-3 bg-red-100 text-red-700 rounded-md">
                    {status.error}
                  </div>
                )}
              </Form>
            )}
          </Formik>
        </div>
      </div>
    </Layout>
  );
};

export default AgentCreation;
