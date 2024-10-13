import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import DataSetCreation from '../data-set-creation';

// Mock the FileUpload component
jest.mock('../../components/FileUpload', () => {
  return function DummyFileUpload({ onFileUpload }: { onFileUpload: (file: File) => void }) {
    return (
      <button onClick={() => onFileUpload(new File([''], 'test.png', { type: 'image/png' }))}>
        Upload File
      </button>
    );
  };
});

describe('DataSetCreation', () => {
  it('renders the page title', () => {
    render(<DataSetCreation />);
    const pageTitle = screen.getByRole('heading', { name: /data set creation/i });
    expect(pageTitle).toBeInTheDocument();
  });

  it('renders the form fields', () => {
    render(<DataSetCreation />);
    expect(screen.getByLabelText(/data set name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/description/i)).toBeInTheDocument();
    expect(screen.getByText(/add files to data set/i)).toBeInTheDocument();
  });

  it('renders the FileUpload component', () => {
    render(<DataSetCreation />);
    expect(screen.getByText('Upload File')).toBeInTheDocument();
  });

  it('displays selected files', async () => {
    render(<DataSetCreation />);
    const uploadButton = screen.getByText('Upload File');
    fireEvent.click(uploadButton);
    await waitFor(() => {
      expect(screen.getByText('Selected Files:')).toBeInTheDocument();
      expect(screen.getByText('test.png')).toBeInTheDocument();
    });
  });

  it('enables the create button when form is filled', async () => {
    render(<DataSetCreation />);
    
    fireEvent.change(screen.getByLabelText(/data set name/i), { target: { value: 'Test Data Set' } });
    fireEvent.click(screen.getByText('Upload File'));

    await waitFor(() => {
      expect(screen.getByText('Create Data Set')).toBeEnabled();
    });
  });

  it('shows creating state when create button is clicked', async () => {
    render(<DataSetCreation />);
    
    fireEvent.change(screen.getByLabelText(/data set name/i), { target: { value: 'Test Data Set' } });
    fireEvent.click(screen.getByText('Upload File'));

    const createButton = screen.getByText('Create Data Set');
    fireEvent.click(createButton);

    await waitFor(() => {
      expect(screen.getByText('Creating...')).toBeInTheDocument();
    });
  });

  // Add more tests as needed for error handling, successful creation, etc.
});
