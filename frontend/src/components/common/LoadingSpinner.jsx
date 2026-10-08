import React from 'react';
import { Loader2 } from 'lucide-react';

export function LoadingSpinner({ size = 24, text = null, className = '' }) {
  return (
    <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.6rem' }} className={className}>
      <Loader2 size={size} className="spinner" style={{ color: 'var(--emerald-400)' }} />
      {text && <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>{text}</span>}
    </div>
  );
}
