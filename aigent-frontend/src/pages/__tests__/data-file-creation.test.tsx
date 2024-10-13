import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import DataFileCreation from '../data-file-creation';

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

describe('DataFileCreation', () => {
  it('renders the page title', () => {
    render(<DataFileCreation />);
    const pageTitle = screen.getByRole('heading', { name: /data file creation/i });
    expect(pageTitle).toBeInTheDocument();
  });

  it('renders the FileUpload component', () => {
    render(<DataFileCreation />);
    expect(screen.getByText('Upload File')).toBeInTheDocument();
  });

  it('renders OCR method selection', () => {
    render(<DataFileCreation />);
    expect(screen.getByLabelText('Google AI OCR')).toBeInTheDocument();
    expect(screen.getByLabelText('Tesseract OCR')).toBeInTheDocument();
  });

  it('enables the process button when file is uploaded and OCR method is selected', async () => {
    render(<DataFileCreation />);
    
    const uploadButton = screen.getByText('Upload File');
    fireEvent.click(uploadButton);

    const googleOcrRadio = screen.getByLabelText('Google AI OCR');
    fireEvent.click(googleOcrRadio);

    await waitFor(() => {
      expect(screen.getByText('Process File')).toBeEnabled();
    });
  });

  it('shows processing state when process button is clicked', async () => {
    render(<DataFileCreation />);
    
    const uploadButton = screen.getByText('Upload File');
    fireEvent.click(uploadButton);

    const googleOcrRadio = screen.getByLabelText('Google AI OCR');
    fireEvent.click(googleOcrRadio);

    const processButton = screen.getByText('Process File');
    fireEvent.click(processButton);

    await waitFor(() => {
      expect(screen.getByText('Processing...')).toBeInTheDocument();
    });
  });

  // Add more tests as needed for error handling, successful processing, etc.
});
