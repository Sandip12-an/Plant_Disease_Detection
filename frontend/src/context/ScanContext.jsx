import React, { createContext, useContext, useState, useEffect } from 'react';
import { diseaseService } from '../services/diseaseService';

const ScanContext = createContext(null);

export function ScanProvider({ children }) {
  const [currentScan, setCurrentScan] = useState(null);
  const [historyList, setHistoryList] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(false);

  const fetchHistory = async () => {
    setLoadingHistory(true);
    try {
      const data = await diseaseService.getHistory(30, 0);
      setHistoryList(data.items || []);
    } catch (err) {
      console.error('Failed to fetch scan history:', err);
    } finally {
      setLoadingHistory(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const addScanToHistory = (scan) => {
    setHistoryList((prev) => [scan, ...prev]);
  };

  const removeScanFromHistory = async (id) => {
    try {
      await diseaseService.deleteHistory(id);
      setHistoryList((prev) => prev.filter((item) => item.id !== id));
      if (currentScan?.scan_id === id) {
        setCurrentScan(null);
      }
    } catch (err) {
      console.error('Failed to delete scan:', err);
    }
  };

  return (
    <ScanContext.Provider
      value={{
        currentScan,
        setCurrentScan,
        historyList,
        loadingHistory,
        fetchHistory,
        addScanToHistory,
        removeScanFromHistory,
      }}
    >
      {children}
    </ScanContext.Provider>
  );
}

export const useScan = () => useContext(ScanContext);
