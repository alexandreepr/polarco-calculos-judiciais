import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { FormButtons } from '..';
import { MantineProvider } from '@mantine/core';

describe('FormButtons', () => {
  it('must renders the Reset and Count words buttons', () => {
    render(
      <MantineProvider>
        <FormButtons />
      </MantineProvider>
    );

    const resetButton = screen.getByText('Reset');
    const countWordsButton = screen.getByText('Count words');

    expect(resetButton).toBeInTheDocument();
    expect(countWordsButton).toBeInTheDocument();
  });

  it('must calls the onReset function when Reset button is clicked', () => {
    const onResetMock = jest.fn();
    render(
      <MantineProvider>
        <FormButtons onReset={onResetMock} />
      </MantineProvider>
    );

    const resetButton = screen.getByText('Reset');
    fireEvent.click(resetButton);

    expect(onResetMock).toHaveBeenCalledTimes(1);
  });
});
