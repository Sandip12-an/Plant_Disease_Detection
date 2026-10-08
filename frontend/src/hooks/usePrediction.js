import { useState } from 'react';
import { diseaseService } from '../services/diseaseService';
import { useScan } from '../context/ScanContext';

export function usePrediction() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { setCurrentScan, addScanToHistory } = useScan();

  const runPrediction = async (file) => {
    setLoading(true);
    setError(null);
    try {
      const result = await diseaseService.predict(file);
      setCurrentScan(result);
      addScanToHistory({
        id: result.scan_id,
        crop_name: result.crop,
        disease_name: result.disease,
        disease_class: result.disease_class,
        confidence: result.confidence,
        is_healthy: result.is_healthy,
        image_url: result.original_image_url,
        heatmap_url: result.heatmap_url,
        treatment_summary: result.treatment?.organic_treatment?.substring(0, 200),
        created_at: new Date().toISOString(),
      });
      return result;
    } catch (err) {
      console.error('Prediction failed:', err);
      setError(err.message || 'Failed to analyze plant leaf.');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    runPrediction,
    loading,
    error,
    setError,
  };
}
