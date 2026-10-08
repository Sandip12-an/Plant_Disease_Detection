import React from 'react';
import { Badge } from '../common/Badge';

export function ConfidenceMeter({ confidence, severity, isHealthy, topPredictions = [] }) {
  const percentage = (confidence * 100).toFixed(1);

  return (
    <div style={{ marginBottom: '1.5rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
        <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>AI Confidence Score</span>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.8rem' }}>
          <span style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--emerald-300)' }}>
            {percentage}%
          </span>
          <Badge status={isHealthy ? 'healthy' : severity} text={severity} />
        </div>
      </div>

      <div className="confidence-meter">
        <div
          className="confidence-fill"
          style={{ width: `${Math.min(100, Math.max(5, percentage))}%` }}
        />
      </div>

      {/* Alternative Top Predictions */}
      {topPredictions.length > 1 && (
        <div style={{ marginTop: '1rem', background: 'rgba(0,0,0,0.2)', padding: '0.75rem 1rem', borderRadius: '10px' }}>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.4rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Top Candidate Diagnoses
          </div>
          {topPredictions.map((pred, i) => (
            <div
              key={i}
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                fontSize: '0.85rem',
                padding: '0.2rem 0',
                color: i === 0 ? 'var(--emerald-300)' : 'var(--text-secondary)',
                fontWeight: i === 0 ? 600 : 400,
              }}
            >
              <span>{pred.crop} — {pred.disease_name}</span>
              <span>{pred.percentage}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
