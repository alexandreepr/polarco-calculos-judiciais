import React from 'react';
import { Alert, Box, Card, Text, TextInput } from '@mantine/core';
import { useForm } from '@mantine/form';
import axios from 'axios';
import { FormButtons } from '../FormButtons';

export const WordCounter = () => {
  const [wordsCounter, setWordsCounter] = React.useState(0);
  const [error, setError] = React.useState(null);

  const form = useForm({
    initialValues: { text: '' },
    validate: {
      text: (value) => {
        if (value.length < 1 || value.trim().length < 1) {
          setWordsCounter(0);
          return 'Please enter a text';
        }
      }
    }
  });

  const handleSubmit = async () => {
    try {
      const response = await axios.post(`${process.env.REACT_APP_API_URL}/words-counter`, {
        words_string: form.values.text
      });

      setWordsCounter(response.data.words_count);
    } catch (error) {
      setError(`Error: ${error}`);
    }
  };

  return (
    <Box
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh'
      }}>
      <Card
        shadow="md"
        p="lg"
        radius="md"
        withBorder
        style={{ backgroundColor: '#e1ebee', height: '17vh', width: '50vh', minHeight: '320px' }}>
        <Text style={{ fontSize: '50px', textAlign: 'center' }}>Words Counter</Text>

        <form
          onSubmit={form.onSubmit((values) => {
            form.setValues(values);
            handleSubmit();
          })}>
          <TextInput
            placeholder="Start typing..."
            value={form.values.text}
            {...form.getInputProps('text')}
          />
          {error && (
            <Alert mt="xs" color="red">
              {error}
            </Alert>
          )}

          <Text mt="xs">Words count: {wordsCounter}</Text>

          <FormButtons
            onReset={() => {
              form.reset();
              setWordsCounter(0);
            }}
          />
        </form>
      </Card>
    </Box>
  );
};
