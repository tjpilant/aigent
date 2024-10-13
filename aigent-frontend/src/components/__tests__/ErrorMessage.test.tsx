import React from 'react';
import { render, screen } from '@testing-library/react';
import ErrorMessage from '../ErrorMessage';

describe('ErrorMessage', () => {
  it('renders the error message', () => {
    const testMessage = 'Test error message';
    render(<ErrorMessage message={testMessage} />);
    
    expect(screen.getByText('Error:')).toBeInTheDocument();
    expect(screen.getByText(testMessage)).toBeInTheDocument();
  });

  it('has the correct styling', () => {
    render(<ErrorMessage message="Test message" />);
    
    const errorDiv = screen.getByRole('alert');
    expect(errorDiv).toHaveClass('bg-red-100', 'border', 'border-red-400', 'text-red-700', 'px-4', 'py-3', 'rounded', 'relative');
  });

  it('renders with long error messages', () => {
    const longMessage = 'This is a very long error message that should still be displayed correctly without any truncation or overflow issues in the component rendering.';
    render(<ErrorMessage message={longMessage} />);
    
    expect(screen.getByText(longMessage)).toBeInTheDocument();
  });
});
