import React from 'react';
import { RotateCcw, Share2, Sparkles, CheckCircle2 } from 'lucide-react';
import { ConfidenceMeter } from './ConfidenceMeter';
import { GradCamViewer } from './GradCamViewer';
import { TreatmentTabs } from '../treatment/TreatmentTabs';
import { Button } from '../common/Button';

export function DiagnosisResult({ result, onResetScan }) {
  if (!result) return null;

  return (
    <div className="glass-panel" style={{ padding: '2.5rem' }}>
      {/* Header Banner */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.5rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.4rem' }}>
            <span style={{ fontSize: '0.85rem', color: 'var(--emerald-400)', textTransform: 'uppercase', letterSpacing: '0.05em', fontWeight: 600 }}>
              {result.crop} Diagnosis
            </span>
          </div>
          <h2 style={{ fontSize: '2rem', lineHeight: 1.2, color: '#fff' }}>
            {result.disease}
          </h2>
        </div>

        <div style={{ display: 'flex', gap: '0.6rem' }}>
          <Button variant="secondary" icon={RotateCcw} onClick={onResetScan}>
            New Scan
          </Button>
        </div>
      </div>

      {/* Main Grid: Left = Visualizer, Right = Metrics & Remedies */}
      <div className="diagnosis-grid">
        <div>
          <GradCamViewer
            originalUrl={result.original_image_url}
            heatmapUrl={result.heatmap_url}
          />
        </div>

        <div>
          <ConfidenceMeter
            confidence={result.confidence}
            severity={result.severity}
            isHealthy={result.is_healthy}
            topPredictions={result.top_predictions}
          />

          <TreatmentTabs
            treatment={result.treatment}
            warning={result.warning}
          />
        </div>
      </div>
    </div>
  );
}
