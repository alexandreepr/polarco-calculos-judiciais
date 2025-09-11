import { Button, Group } from '@mantine/core';

export const FormButtons = ({ onReset }) => (
  <Group style={{ justifyContent: 'end', display: 'flex' }} mt="md">
    <Button onClick={onReset} color="red">
      Reset
    </Button>
    <Button type="submit">Count words</Button>
  </Group>
);
