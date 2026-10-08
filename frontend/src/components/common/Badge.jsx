import React from 'react';
import { CheckCircle2, AlertTriangle, AlertCircle, ShieldCheck } from 'lucide-react';

export function Badge({ status, text }) {
  if (status === 'healthy') {
    return (
      <span className="badge badge-healthy">
        <ShieldCheck size={14} />
        {text || 'Healthy'}
      </span>
    );
  }
  if (status === 'severe' || status === 'High') {
    return (
      <span className="badge badge-diseased">
        <AlertCircle size={14} />
        {text || 'Severe Infection'}
      </span>
    );
  }
  return (
    <span className="badge badge-warning">
      <AlertTriangle size={14} />
      {text || 'Moderate / Mild'}
    </span>
  );
}
