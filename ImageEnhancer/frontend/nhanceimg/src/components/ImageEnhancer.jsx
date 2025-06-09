import React, { useState } from 'react';

function ImageEnhancer({ setError }) {
  const [selectedImage, setSelectedImage] = useState(null);
  const [enhancedImage, setEnhancedImage] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    console.log(file);
    
    if (!file) return;

    const reader = new FileReader();
    reader.onloadend = () => {
      const base64 = reader.result.split(',')[1];
      setSelectedImage(reader.result); // full data URL for preview
      sendToBackend(base64);
    };

    reader.readAsDataURL(file);
  };

  const sendToBackend = async (base64Image) => {
    setLoading(true);
    setEnhancedImage(null);

    try {
      const response = await fetch('http://localhost:83/api/enhance/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          encoded_base_img: [base64Image],
          method: 'gfpgan' // or 'RestoreFormer' or 'codeformer' as required
        }),
      });

      const data = await response.json();
      if (!response.ok) {
        setError(`Error: ${data.error || 'Failed to enhance image'}`);
        return;
      }
      if (data.message) {
        setError(`Error: ${data.message || 'Failed to enhance image'}`);
        return;
      }
      setEnhancedImage(`data:image/jpeg;base64,${data.image}`);
    } catch (error) {
      console.error('Error enhancing image:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    const link = document.createElement('a');
    link.href = enhancedImage;
    link.download = 'enhanced.jpg';
    link.click();
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6 flex flex-col items-center">
      <div className="bg-white shadow-lg rounded-2xl p-6 w-full max-w-4xl">
        {/* <h1 className="text-3xl font-bold text-center text-gray-800 mb-6">AI Image Enhancer</h1> */}

        <input
          type="file"
          accept="image/jpeg"
          onChange={handleFileChange}
          className="w-full mb-6 border border-gray-300 rounded-md p-2 text-gray-700 bg-gray-50 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-700"
        />

        {loading && (
          <p className="text-center text-blue-600 font-medium mb-4 animate-pulse">
            Enhancing image, please wait...
          </p>
        )}

        {(selectedImage || enhancedImage) && (
          <div className="grid md:grid-cols-2 gap-6 mt-4">
            {selectedImage && (
              <div>
                <h3 className="text-lg font-medium text-gray-700 mb-2">Original Image</h3>
                <img
                  src={selectedImage}
                  alt="Original"
                  className="w-full rounded-lg shadow border"
                />
              </div>
            )}

            {enhancedImage && (
              <div>
                <h3 className="text-lg font-medium text-gray-700 mb-2">Enhanced Image</h3>
                <img
                  src={enhancedImage}
                  alt="Enhanced"
                  className="w-full rounded-lg shadow border"
                />
                <button
                  onClick={handleDownload}
                  className="mt-4 w-full bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-lg font-semibold transition"
                >
                  Download Enhanced Image
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default ImageEnhancer;
