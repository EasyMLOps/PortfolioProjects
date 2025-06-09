
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import ImageEnhancer from './components/ImageEnhancer';

export default function App() {
  const [error, setError] = React.useState(null);  
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="max-w-4xl w-full p-6 bg-white shadow-lg rounded-2xl">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-6">AI Image Enhancer</h1>
        <p className="text-center text-gray-600 mb-4">
          Upload a JPEG image to enhance its quality using AI.
        </p>
        <p className="text-center text-gray-600 mb-6">
          Supported formats: JPEG only. Maximum file size: 5MB.
        </p>
        {error && (
          <p className="text-red-600 text-center mb-4">
            {error}
          </p>
        )}
          <ImageEnhancer setError={setError}></ImageEnhancer>
      </div>
    </div>
  );
}

