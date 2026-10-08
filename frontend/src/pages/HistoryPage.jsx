import React, { useState } from 'react';
import { HistoryList } from '../components/history/HistoryList';
import { DiagnosisResult } from '../components/diagnosis/DiagnosisResult';
import { useScan } from '../context/ScanContext';

export function HistoryPage() {
  const { historyList, loadingHistory, fetchHistory, removeScanFromHistory } = useScan();
  const [selectedScanDetail, setSelectedScanDetail] = useState(null);

  const handleSelect = (scan) => {
    // Map scan database record to format expected by DiagnosisResult
    const mapped = {
      scan_id: scan.id,
      crop: scan.crop_name,
      disease: scan.disease_name,
      disease_class: scan.disease_class,
      confidence: scan.confidence,
      is_healthy: scan.is_healthy,
      severity: scan.is_healthy ? 'Healthy' : scan.confidence > 0.85 ? 'High' : 'Moderate',
      original_image_url: scan.image_url,
      heatmap_url: scan.heatmap_url,
      treatment: {
        crop: scan.crop_name,
        disease_name: scan.disease_name,
        is_healthy: scan.is_healthy,
        description: `Archived scan record: ${scan.disease_name}`,
        symptoms: 'Inspect past visual records.',
        organic_treatment: scan.treatment_summary || 'Apply organic preventative treatments.',
        chemical_treatment: 'Refer to original scan consultation.',
        prevention: 'Maintain routine field inspections and crop rotation.',
      },
      top_predictions: [
        {
          disease_class: scan.disease_class,
          crop: scan.crop_name,
          disease_name: scan.disease_name,
          confidence: scan.confidence,
          percentage: `${(scan.confidence * 100).toFixed(1)}%`,
        },
      ],
    };
    setSelectedScanDetail(mapped);
  };

  return (
    <div className="container" style={{ padding: '3rem 1.5rem 5rem' }}>
      <div style={{ marginBottom: '2.5rem' }}>
        <h1 style={{ fontSize: '2.2rem', marginBottom: '0.5rem' }}>
          Diagnostic History & Timeline
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '1rem' }}>
          Review historical plant diagnoses, compare lesion development over time, and manage records.
        </p>
      </div>

      {selectedScanDetail ? (
        <div style={{ marginBottom: '3rem' }}>
          <div style={{ marginBottom: '1rem' }}>
            <button
              onClick={() => setSelectedScanDetail(null)}
              style={{
                color: 'var(--emerald-400)',
                fontSize: '0.9rem',
                fontWeight: 600,
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.4rem',
              }}
            >
              ← Back to History List
            </button>
          </div>
          <DiagnosisResult
            result={selectedScanDetail}
            onResetScan={() => setSelectedScanDetail(null)}
          />
        </div>
      ) : (
        <HistoryList
          history={historyList}
          loading={loadingHistory}
          onRefresh={fetchHistory}
          onSelectScan={handleSelect}
          onDeleteScan={removeScanFromHistory}
        />
      )}
    </div>
  );
}
