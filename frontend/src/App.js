import React from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';
import { WordCounter } from './components/WordCounter';

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<WordCounter />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
