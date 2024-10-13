import React from 'react';
import { render, screen } from '@testing-library/react';
import Layout from '../Layout';

// Mock the Next.js router
jest.mock('next/router', () => ({
  useRouter() {
    return {
      route: '/',
      pathname: '',
      query: '',
      asPath: '',
    };
  },
}));

describe('Layout', () => {
  it('renders the layout with navigation and footer', () => {
    render(
      <Layout>
        <div>Test Content</div>
      </Layout>
    );

    // Check if the navigation is present
    expect(screen.getByRole('navigation')).toBeInTheDocument();

    // Check if the main content is rendered
    expect(screen.getByText('Test Content')).toBeInTheDocument();

    // Check if the footer is present
    expect(screen.getByRole('contentinfo')).toBeInTheDocument();
  });

  it('contains all the required navigation links', () => {
    render(
      <Layout>
        <div>Test Content</div>
      </Layout>
    );

    // Check for the presence of all navigation links
    expect(screen.getByText('AIGENT')).toBeInTheDocument();
    expect(screen.getByText('Data File Creation')).toBeInTheDocument();
    expect(screen.getByText('Data Set Creation')).toBeInTheDocument();
    expect(screen.getByText('Agent Training')).toBeInTheDocument();
    expect(screen.getByText('Agent Creation')).toBeInTheDocument();
  });

  it('renders children content', () => {
    render(
      <Layout>
        <div data-testid="child-content">Custom Child Content</div>
      </Layout>
    );

    expect(screen.getByTestId('child-content')).toBeInTheDocument();
    expect(screen.getByText('Custom Child Content')).toBeInTheDocument();
  });
});
