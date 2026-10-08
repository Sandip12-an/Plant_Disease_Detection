import React, { useState } from 'react';
import { Eye, Layers, Sparkles } from 'lucide-react';

export function GradCamViewer({ originalUrl, heatmapUrl }) {
  const [viewMode, setViewMode] = useState('overlay'); // 'overlay' | 'original'

  const activeSrc = viewMode === 'overlay' && heatmapUrl ? heatmapUrl : originalUrl;

  return (
    <div>
      <div className="gradcam-container">
        <img
          src={activeSrc}
          alt="Plant Leaf Analysis"
          className="gradcam-img"
        />

        {viewMode === 'overlay' && (
          <div
            style={{
              position: 'absolute',
              bottom: '12px',
              left: '12px',
              background: 'rgba(0, 0, 0, 0.75)',
              backdropFilter: 'blur(8px)',
              padding: '0.35rem 0.75rem',
              borderRadius: '8px',
              fontSize: '0.75rem',
              color: 'var(--emerald-300)',
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
            }}
          >
            <Sparkles size={13} />
            <span>Grad-CAM Explainability Active</span>
          </div>
        )}
      </div>

      <div className="gradcam-toggle-bar">
        <button
          type="button"
          className={`gradcam-toggle-btn ${viewMode === 'overlay' ? 'active' : ''}`}
          onClick={() => setViewMode('overlay')}
        >
          <Layers size={14} style={{ display: 'inline', marginRight: '5px' }} />
          Lesion Heatmap Overlay
        </button>

        <button
          type="button"
          className={`gradcam-toggle-btn ${viewMode === 'original' ? 'active' : ''}`}
          onClick={() => setViewMode('original')}
        >
          <Eye size={14} style={{ display: 'inline', marginRight: '5px' }} />
          Original Leaf
        </button>
      </div>

      <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '0.5rem', textAlign: 'center' }}>
        Red and orange zones highlight regions of high pathogen symptom activation (chlorosis, necrosis, or spots).
      </p>
    </div>
  );
}
