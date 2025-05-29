// src/hooks/useAccounts.js
import { useState, useEffect } from 'react';

export function useAccounts() {
  const [accounts, setAccounts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true; // to prevent state updates on unmounted component

    async function fetchAccounts() {
      try {
        const response = await fetch('http://localhost:8000/accounts/');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        if (isMounted) {
          setAccounts(data);
          setError(null);
        }
      } catch (err) {
        if (isMounted) setError(err.message);
      } finally {
        if (isMounted) setLoading(false);
      }
    }

    // Initial fetch
    fetchAccounts();

    // Set up polling to refresh accounts every 5 seconds
    const intervalId = setInterval(fetchAccounts, 2000);

    // Cleanup function
    return () => {
      isMounted = false;
      clearInterval(intervalId);
    };
  }, []);

  return { accounts, loading, error };
}
