// src/services/api.js

const API_BASE_URL = 'http://localhost:8000';

const handleApiError = (error) => {
  if (error.response) {
    throw new Error(error.response.data.message || 'Server error');
  } else if (error.request) {
    throw new Error('No response from server. Please check your connection.');
  } else {
    throw new Error('Failed to send request. Please try again.');
  }
};

export const chatAPI = {
  sendMessage: async (message) => {
    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: message }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new Error(
          errorData?.message || 
          `Server error: ${response.status} ${response.statusText}`
        );
      }

      const data = await response.json();
      return data.answer || data.response || data.message || data;
    } catch (error) {
      console.error('Error sending message:', error);
      handleApiError(error);
    }
  }
};