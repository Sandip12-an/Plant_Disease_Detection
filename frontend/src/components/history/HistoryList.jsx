import React, { useState } from 'react';
import { History, Filter, RefreshCw, AlertCircle } from 'lucide-react';
import { HistoryCard } from './HistoryCard';
import { Button } from '../common/Button';
import { LoadingSpinner } from '../common/LoadingSpinner';

export function HistoryList({ history, loading, onRefresh, onSelectScan, onDeleteScan }) {
  const [filter, setFilter] = useState('all'); // 'all' | 'healthy' | 'diseased'

  const filteredHistory = history.filter((item) => {
    if (filter === 'healthy') return item.is_healthy;
    if (filter === 'diseased') return !item.is_healthy;
    return true;
  });

  return (
    <div>
      {/* Controls Bar */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem', marginBottom: '2rem' }}>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <Button
            variant={filter === 'all' ? 'primary' : 'secondary'}
            onClick={() => setFilter('all')}
            style={{ fontSize: '0.85rem', padding: '0.4rem 1rem' }}
          >
            All Scans ({history.length})
          </Button>
          <Button
            variant={filter === 'diseased' ? 'primary' : 'secondary'}
            onClick={() => setFilter('diseased')}
            style={{ fontSize: '0.85rem', padding: '0.4rem 1rem' }}
          >
            Diseased
          </Button>
          <Button
            variant={filter === 'healthy' ? 'primary' : 'secondary'}
            onClick={() => setFilter('healthy')}
            style={{ fontSize: '0.85rem', padding: '0.4rem 1rem' }}
          >
            Healthy
          </Button>
        </div>

        <Button variant="outline" icon={RefreshCw} onClick={onRefresh} loading={loading}>
          Refresh
        </Button>
      </div>

      {loading && history.length === 0 ? (
        <div style={{ padding: '4rem', textAlign: 'center' }}>
          <LoadingSpinner size={32} text="Loading past scans..." />
        </div>
      ) : filteredHistory.length === 0 ? (
        <div className="glass-panel" style={{ padding: '3.5rem', textAlign: 'center' }}>
          <History size={48} style={{ color: 'var(--text-muted)', marginBottom: '1rem' }} />
          <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>No Scan History Found</h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
            Upload or capture your first plant leaf to start tracking disease diagnosis history.
          </p>
        </div>
      ) : (
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
            gap: '1.5rem',
          }}
        >
          {filteredHistory.map((scan) => (
            <HistoryCard
              key={scan.id}
              scan={scan}
              onSelect={onSelectScan}
              onDelete={onDeleteScan}
            />
          ))}
        </div>
      )}
    </div>
  );
}
