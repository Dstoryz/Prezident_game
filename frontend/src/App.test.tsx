import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders game title', () => {
  render(<App />);
  const titleElement = screen.getByText(/Президент: Экономика и Власть/i);
  expect(titleElement).toBeInTheDocument();
});
