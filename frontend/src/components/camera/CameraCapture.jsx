import React, { useEffect } from 'react';
import { Camera, X, AlertCircle } from 'lucide-react';
import { Button } from '../common/Button';
import { useCamera } from '../../hooks/useCamera';

export function CameraCapture({ onCapture, onClose }) {
  const { videoRef, isCameraActive, startCamera, stopCamera, capturePhoto, error } = useCamera();

  useEffect(() => {
    startCamera();
    return () => stopCamera();
  }, [startCamera, stopCamera]);

  const handleTakeSnapshot = async () => {
    const file = await capturePhoto();
    if (file) {
      stopCamera();
      onCapture(file);
    }
  };

  return (
    <div className="glass-panel" style={{ padding: '2rem', textAlign: 'center' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.2rem' }}>
        <h3 style={{ fontSize: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
          <Camera size={20} style={{ color: 'var(--emerald-400)' }} />
          Live Leaf Scanner
        </h3>
        <Button variant="outline" icon={X} onClick={onClose} style={{ padding: '0.4rem 0.8rem' }}>
          Close
        </Button>
      </div>

      {error ? (
        <div style={{ padding: '2rem', color: 'var(--rose-danger)', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.7rem' }}>
          <AlertCircle size={24} />
          <span>{error}</span>
        </div>
      ) : (
        <>
          <div className="camera-box">
            <video ref={videoRef} autoPlay playsInline muted className="camera-video" />
            <div
              style={{
                position: 'absolute',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
                width: '240px',
                height: '240px',
                border: '2px dashed rgba(52, 211, 153, 0.6)',
                borderRadius: '16px',
                pointerEvents: 'none',
              }}
            />
          </div>

          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '0.8rem' }}>
            Position the infected or healthy leaf centered within the frame
          </p>

          <div style={{ marginTop: '1.5rem', display: 'flex', gap: '1rem', justifyContent: 'center' }}>
            <Button variant="primary" icon={Camera} onClick={handleTakeSnapshot}>
              Capture & Diagnose
            </Button>
            <Button variant="secondary" onClick={onClose}>
              Cancel
            </Button>
          </div>
        </>
      )}
    </div>
  );
}
