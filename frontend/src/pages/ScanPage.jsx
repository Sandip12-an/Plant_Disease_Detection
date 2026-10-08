import React, { useState } from 'react';
import { Camera, UploadCloud, AlertCircle } from 'lucide-react';
import { DropZone } from '../components/camera/DropZone';
import { CameraCapture } from '../components/camera/CameraCapture';
import { DiagnosisResult } from '../components/diagnosis/DiagnosisResult';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { usePrediction } from '../hooks/usePrediction';
import { useScan } from '../context/ScanContext';

export function ScanPage() {
  const [isCameraActive, setIsCameraActive] = useState(false);
  const { runPrediction, loading, error, setError } = usePrediction();
  const { currentScan, setCurrentScan } = useScan();

  const handleFileSelect = async (file) => {
    try {
      await runPrediction(file);
    } catch {
      // Error handled in hook
    }
  };

  const handleReset = () => {
    setCurrentScan(null);
    setError(null);
    setIsCameraActive(false);
  };

  return (
    <div className="container scan-workstation">
      <div style={{ textAlign: 'center', marginBottom: '2.5rem' }}>
        <h1 style={{ fontSize: '2.4rem', marginBottom: '0.6rem' }}>
          Crop Diagnostic Workstation
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '1.05rem', maxWidth: '620px', margin: '0 auto' }}>
          Position your leaf photograph or capture live via camera. Our deep learning engine will analyze the pathology in milliseconds.
        </p>
      </div>

      {error && (
        <div
          style={{
            background: 'rgba(251, 113, 133, 0.12)',
            border: '1px solid rgba(251, 113, 133, 0.3)',
            color: 'var(--rose-danger)',
            padding: '1rem 1.25rem',
            borderRadius: '12px',
            marginBottom: '2rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.75rem',
          }}
        >
          <AlertCircle size={22} />
          <span>{error}</span>
        </div>
      )}

      {loading ? (
        <div className="glass-panel" style={{ padding: '5rem 2rem', textAlign: 'center' }}>
          <LoadingSpinner size={44} />
          <h3 style={{ fontSize: '1.35rem', marginTop: '1.5rem', marginBottom: '0.5rem' }}>
            Analyzing Leaf Pathology...
          </h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem' }}>
            Extracting deep convolutional feature maps & generating Grad-CAM explainability heatmap.
          </p>
        </div>
      ) : currentScan ? (
        <DiagnosisResult result={currentScan} onResetScan={handleReset} />
      ) : isCameraActive ? (
        <CameraCapture
          onCapture={handleFileSelect}
          onClose={() => setIsCameraActive(false)}
        />
      ) : (
        <DropZone
          onFileSelect={handleFileSelect}
          onLaunchCamera={() => setIsCameraActive(true)}
          isProcessing={loading}
        />
      )}
    </div>
  );
}
