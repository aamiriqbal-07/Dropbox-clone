import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import FileDetailPage from './pages/FileDetailPage';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/file/:id" element={<FileDetailPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;