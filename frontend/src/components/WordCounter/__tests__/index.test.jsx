import React from 'react';
import axios from 'axios';
import { render, fireEvent, screen, waitFor } from '@testing-library/react';
import { WordCounter } from '..';
import { MantineProvider } from '@mantine/core';

jest.mock('axios');

describe('WordCounter', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('must renders correctly', () => {
    render(
      <MantineProvider>
        <WordCounter />
      </MantineProvider>
    );
    expect(screen.getByText(/words counter/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/start typing/i)).toBeInTheDocument();
    expect(screen.getByText(/words count: 0/i)).toBeInTheDocument();
  });

  it('must displays an error message when submitting an empty form', async () => {
    render(
      <MantineProvider>
        <WordCounter />
      </MantineProvider>
    );

    fireEvent.click(screen.getByText(/count words/i));

    await waitFor(() => {
      expect(screen.getByText(/please enter a text/i)).toBeInTheDocument();
    });
  });

  it('must displays the word count when API call is successful', async () => {
    axios.post.mockResolvedValue({ data: { words_count: 3 } });

    render(
      <MantineProvider>
        <WordCounter />
      </MantineProvider>
    );

    fireEvent.change(screen.getByPlaceholderText(/start typing/i), {
      target: { value: 'hello world test' }
    });

    fireEvent.click(screen.getByText(/count words/i));

    await waitFor(() => {
      expect(screen.getByText(/words count: 3/i)).toBeInTheDocument();
    });
  });

  it('must displays an error message when API call fails', async () => {
    axios.post.mockRejectedValue(new Error('Network Error'));

    render(
      <MantineProvider>
        <WordCounter />
      </MantineProvider>
    );

    fireEvent.change(screen.getByPlaceholderText(/start typing/i), {
      target: { value: 'hello world test' }
    });

    fireEvent.click(screen.getByText(/count words/i));

    await waitFor(() => {
      expect(screen.getByText(/error: network error/i)).toBeInTheDocument();
    });
  });

  it('must resets the form and word count', () => {
    render(
      <MantineProvider>
        <WordCounter />
      </MantineProvider>
    );

    fireEvent.change(screen.getByPlaceholderText(/start typing/i), {
      target: { value: 'hello world test' }
    });

    fireEvent.click(screen.getByText(/reset/i));

    expect(screen.getByPlaceholderText(/start typing/i).value).toBe('');
    expect(screen.getByText(/words count: 0/i)).toBeInTheDocument();
  });
});
