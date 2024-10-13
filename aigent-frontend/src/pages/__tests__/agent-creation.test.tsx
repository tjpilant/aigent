import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import AgentCreation from '../agent-creation';

describe('AgentCreation', () => {
  it('renders the page title', () => {
    render(<AgentCreation />);
    const pageTitle = screen.getByRole('heading', { name: /agent creation/i });
    expect(pageTitle).toBeInTheDocument();
  });

  it('renders the form fields', () => {
    render(<AgentCreation />);
    expect(screen.getByLabelText(/agent name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/agent type/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/description/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/parameters/i)).toBeInTheDocument();
  });

  it('displays agent type options', () => {
    render(<AgentCreation />);
    const agentTypeSelect = screen.getByLabelText(/agent type/i);
    expect(agentTypeSelect).toContainElement(screen.getByText('Select an agent type'));
    expect(agentTypeSelect).toContainElement(screen.getByText('Conversational'));
    expect(agentTypeSelect).toContainElement(screen.getByText('Task-oriented'));
    expect(agentTypeSelect).toContainElement(screen.getByText('Analytical'));
  });

  it('shows validation errors when submitting an empty form', async () => {
    render(<AgentCreation />);
    
    const submitButton = screen.getByText('Create Agent');
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText('Agent name is required')).toBeInTheDocument();
      expect(screen.getByText('Agent type is required')).toBeInTheDocument();
    });
  });

  it('shows validation error for short agent name', async () => {
    render(<AgentCreation />);
    
    const agentNameInput = screen.getByLabelText(/agent name/i);
    fireEvent.change(agentNameInput, { target: { value: 'Ab' } });

    const submitButton = screen.getByText('Create Agent');
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText('Agent name must be at least 3 characters')).toBeInTheDocument();
    });
  });

  it('shows validation error for invalid JSON in parameters', async () => {
    render(<AgentCreation />);
    
    const parametersInput = screen.getByLabelText(/parameters/i);
    fireEvent.change(parametersInput, { target: { value: '{invalid json}' } });

    const submitButton = screen.getByText('Create Agent');
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText('Parameters must be valid JSON')).toBeInTheDocument();
    });
  });

  it('submits the form successfully with valid data', async () => {
    render(<AgentCreation />);
    
    fireEvent.change(screen.getByLabelText(/agent name/i), { target: { value: 'Test Agent' } });
    fireEvent.change(screen.getByLabelText(/agent type/i), { target: { value: 'Conversational' } });
    fireEvent.change(screen.getByLabelText(/description/i), { target: { value: 'Test Description' } });
    fireEvent.change(screen.getByLabelText(/parameters/i), { target: { value: '{"key": "value"}' } });

    const submitButton = screen.getByText('Create Agent');
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText('Creating...')).toBeInTheDocument();
    });

    const successMessage = await screen.findByText(/Agent "Test Agent" of type Conversational created successfully./i, {}, { timeout: 3000 });
    expect(successMessage).toBeInTheDocument();
  });
});
