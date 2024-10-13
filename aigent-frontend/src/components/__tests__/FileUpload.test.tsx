import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import FileUpload from '../FileUpload';

describe('FileUpload', () => {
  it('renders file input', () => {
    render(<FileUpload onFileUpload={() => {}} />);
    expect(screen.getByLabelText(/choose an image file/i)).toBeInTheDocument();
  });

  it('calls onFileUpload when a file is selected', () => {
    const mockOnFileUpload = jest.fn();
    render(<FileUpload onFileUpload={mockOnFileUpload} />);
    
    const file = new File(['dummy content'], 'test.png', { type: 'image/png' });
    const input = screen.getByLabelText(/choose an image file/i) as HTMLInputElement;
    
    fireEvent.change(input, { target: { files: [file] } });
    
    expect(mockOnFileUpload).toHaveBeenCalledWith(file);
  });

  it('displays the name of the selected file', () => {
    render(<FileUpload onFileUpload={() => {}} />);
    
    const file = new File(['dummy content'], 'test.png', { type: 'image/png' });
    const input = screen.getByLabelText(/choose an image file/i) as HTMLInputElement;
    
    fireEvent.change(input, { target: { files: [file] } });
    
    expect(screen.getByText(/Selected file: test.png/i)).toBeInTheDocument();
  });
});
