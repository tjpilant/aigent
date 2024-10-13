import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import AgentTraining from '../agent-training';

describe('AgentTraining', () => {
  it('renders the page title', () => {
    render(<AgentTraining />);
    const pageTitle = screen.getByRole('heading', { name: /agent training/i });
    expect(pageTitle).toBeInTheDocument();
  });

  it('renders the form fields', () => {
    render(<AgentTraining />);
    expect(screen.getByLabelText(/agent name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/select data set/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/training method/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/number of epochs/i)).toBeInTheDocument();
  });

  it('displays data set options', () => {
    render(<AgentTraining />);
    const dataSetSelect = screen.getByLabelText(/select data set/i);
    expect(dataSetSelect).toContainElement(screen.getByText('Select a data set'));
    expect(dataSetSelect).toContainElement(screen.getByText('Data Set 1'));
    expect(dataSetSelect).toContainElement(screen.getByText('Data Set 2'));
    expect(dataSetSelect).toContainElement(screen.getByText('Data Set 3'));
  });

  it('displays training method options', () => {
    render(<AgentTraining />);
    const trainingMethodSelect = screen.getByLabelText(/training method/i);
    expect(trainingMethodSelect).toContainElement(screen.getByText('Select a training method'));
    expect(trainingMethodSelect).toContainElement(screen.getByText('Method A'));
    expect(trainingMethodSelect).toContainElement(screen.getByText('Method B'));
    expect(trainingMethodSelect).toContainElement(screen.getByText('Method C'));
  });

  it('enables the start training button when form is filled', async () => {
    render(<AgentTraining />);
    
    fireEvent.change(screen.getByLabelText(/agent name/i), { target: { value: 'Test Agent' } });
    fireEvent.change(screen.getByLabelText(/select data set/i), { target: { value: 'Data Set 1' } });
    fireEvent.change(screen.getByLabelText(/training method/i), { target: { value: 'Method A' } });

    await waitFor(() => {
      expect(screen.getByText('Start Training')).toBeEnabled();
    });
  });

  it('shows training state when start training button is clicked', async () => {
    render(<AgentTraining />);
    
    fireEvent.change(screen.getByLabelText(/agent name/i), { target: { value: 'Test Agent' } });
    fireEvent.change(screen.getByLabelText(/select data set/i), { target: { value: 'Data Set 1' } });
    fireEvent.change(screen.getByLabelText(/training method/i), { target: { value: 'Method A' } });

    const startTrainingButton = screen.getByText('Start Training');
    fireEvent.click(startTrainingButton);

    await waitFor(() => {
      expect(screen.getByText('Training...')).toBeInTheDocument();
    });
  });

  // Add more tests as needed for error handling, successful training, etc.
});
