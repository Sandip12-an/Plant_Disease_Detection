import React, { useState, useRef } from 'react';
import { UploadCloud, Image as ImageIcon, Sparkles } from 'lucide-react';
import { Button } from '../common/Button';

export function DropZone({ onFileSelect, onLaunchCamera, isProcessing }) {
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = () => {
    setDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      onFileSelect(e.target.files[0]);
    }
  };

  // Quick sample loaders for instant testing
  const loadSample = async (sampleName) => {
    try {
      const response = await fetch(`/data/sample_images/${sampleName}`);
      const blob = await response.blob();
      const file = new File([blob], sampleName, { type: 'image/jpeg' });
      onFileSelect(file);
    } catch (err) {
      console.error('Error loading sample image:', err);
    }
  };

  return (
    <div className="glass-panel" style={{ padding: '2rem' }}>
      <div
        className={`dropzone-container ${dragOver ? 'drag-over' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <input
          type="file"
          ref={fileInputRef}
          style={{ display: 'none' }}
          accept="image/jpeg,image/png,image/webp"
          onChange={handleFileChange}
        />

        <div className="dropzone-icon">
          <UploadCloud size={36} />
        </div>

        <h3 style={{ fontSize: '1.4rem', marginBottom: '0.5rem' }}>
          Drag & Drop Leaf Photo Here
        </h3>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem', fontSize: '0.95rem' }}>
          Supports high-resolution JPG, PNG, and WEBP files (Max 15MB)
        </p>

        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
          <Button
            variant="primary"
            icon={ImageIcon}
            onClick={(e) => {
              e.stopPropagation();
              fileInputRef.current?.click();
            }}
            disabled={isProcessing}
          >
            Browse Local File
          </Button>

          <Button
            variant="secondary"
            onClick={(e) => {
              e.stopPropagation();
              onLaunchCamera();
            }}
            disabled={isProcessing}
          >
            Use Live Camera
          </Button>
        </div>
      </div>

      {/* Quick Test Samples */}
      <div style={{ marginTop: '1.5rem', textAlign: 'center' }}>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '0.8rem' }}>
          <Sparkles size={15} style={{ color: 'var(--lime-accent)' }} />
          <span>Or test instantly with pre-loaded samples:</span>
        </div>
        <div style={{ display: 'flex', gap: '0.8rem', justifyContent: 'center', flexWrap: 'wrap' }}>
          <Button
            variant="outline"
            style={{ fontSize: '0.8rem', padding: '0.4rem 0.9rem' }}
            onClick={() => loadSample('tomato_early_blight.jpg')}
          >
            🍅 Tomato Early Blight
          </Button>
          <Button
            variant="outline"
            style={{ fontSize: '0.8rem', padding: '0.4rem 0.9rem' }}
            onClick={() => loadSample('potato_late_blight.jpg')}
          >
            🥔 Potato Late Blight
          </Button>
          <Button
            variant="outline"
            style={{ fontSize: '0.8rem', padding: '0.4rem 0.9rem' }}
            onClick={() => loadSample('tomato_healthy.jpg')}
          >
            🌿 Tomato Healthy
          </Button>
        </div>
      </div>
    </div>
  );
}
