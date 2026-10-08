import React from 'react';
import { Trash2, Calendar, ShieldCheck, AlertCircle } from 'lucide-react';
import { Badge } from '../common/Badge';

export function HistoryCard({ scan, onSelect, onDelete }) {
  const formattedDate = scan.created_at
    ? new Date(scan.created_at).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
      })
    : 'Recent';

  return (
    <div
      className="glass-panel"
      style={{
        padding: '1.2rem',
        display: 'flex',
        flexDirection: 'column',
        gap: '0.8rem',
        position: 'relative',
      }}
    >
      {/* Leaf Thumbnail */}
      <div
        style={{
          borderRadius: '12px',
          overflow: 'hidden',
          aspectRatio: '16 / 10',
          background: '#000',
          cursor: 'pointer',
        }}
        onClick={() => onSelect(scan)}
      >
        <img
          src={scan.image_url}
          alt={scan.disease_name}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
      </div>

      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.3rem' }}>
          <span style={{ fontSize: '0.78rem', color: 'var(--emerald-400)', fontWeight: 600, textTransform: 'uppercase' }}>
            {scan.crop_name}
          </span>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
            <Calendar size={12} />
            {formattedDate}
          </span>
        </div>

        <h4
          style={{ fontSize: '1.05rem', color: '#fff', cursor: 'pointer', marginBottom: '0.5rem' }}
          onClick={() => onSelect(scan)}
        >
          {scan.disease_name}
        </h4>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Badge
            status={scan.is_healthy ? 'healthy' : 'severe'}
            text={`${(scan.confidence * 100).toFixed(0)}% Conf.`}
          />

          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              onDelete(scan.id);
            }}
            style={{
              color: 'var(--text-muted)',
              padding: '0.4rem',
              borderRadius: '6px',
              transition: 'color 0.15s ease',
            }}
            title="Delete scan record"
          >
            <Trash2 size={16} />
          </button>
        </div>
      </div>
    </div>
  );
}
