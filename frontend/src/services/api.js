// src/services/api.js

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const chatAPI = {
  sendMessage: async (message) => {
    try {
      const response = await fetch(`${API_BASE_URL}/ai/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: message }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      return data.answer;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }
};