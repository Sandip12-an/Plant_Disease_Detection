import React, { useState, useEffect } from 'react';
import { ArrowLeft, BookOpen, Camera, ShieldCheck, AlertCircle } from 'lucide-react';
import { diseaseService } from '../services/diseaseService';
import { TreatmentTabs } from '../components/treatment/TreatmentTabs';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { LoadingSpinner } from '../components/common/LoadingSpinner';

export function DiseaseDetailPage({ diseaseId, onBack, onScanCrop }) {
  const [disease, setDisease] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadDetail() {
      setLoading(true);
      setError(null);
      try {
        const data = await diseaseService.getDiseaseDetail(diseaseId);
        setDisease(data);
      } catch (err) {
        console.error('Failed to load disease profile:', err);
        setError(err.message || 'Disease profile not found.');
      } finally {
        setLoading(false);
      }
    }
    if (diseaseId) {
      loadDetail();
    }
  }, [diseaseId]);

  if (loading) {
    return (
      <div className="container" style={{ padding: '6rem 1.5rem', textAlign: 'center' }}>
        <LoadingSpinner size={40} text="Loading agronomic profile..." />
      </div>
    );
  }

  if (error || !disease) {
    return (
      <div className="container" style={{ padding: '6rem 1.5rem', textAlign: 'center' }}>
        <h3 style={{ color: 'var(--rose-danger)', marginBottom: '1rem' }}>{error || 'Not Found'}</h3>
        <Button variant="secondary" icon={ArrowLeft} onClick={onBack}>
          Back to Directory
        </Button>
      </div>
    );
  }

  return (
    <div className="container" style={{ padding: '3rem 1.5rem 5rem' }}>
      <button
        onClick={onBack}
        style={{
          color: 'var(--emerald-400)',
          fontSize: '0.9rem',
          fontWeight: 600,
          display: 'inline-flex',
          alignItems: 'center',
          gap: '0.4rem',
          marginBottom: '1.5rem',
        }}
      >
        <ArrowLeft size={16} />
        Back to Encyclopedia
      </button>

      <div className="glass-panel" style={{ padding: '2.5rem', marginBottom: '2rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem', marginBottom: '1rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.8rem', marginBottom: '0.5rem' }}>
              <span style={{ fontSize: '0.85rem', color: 'var(--emerald-400)', fontWeight: 600, textTransform: 'uppercase' }}>
                {disease.crop}
              </span>
              <Badge status={disease.is_healthy ? 'healthy' : 'severe'} text={disease.is_healthy ? 'Healthy Foliage' : 'Pathogen Infection'} />
            </div>
            <h1 style={{ fontSize: '2.3rem', color: '#fff', lineHeight: 1.2 }}>
              {disease.name}
            </h1>
            {disease.scientific_name && (
              <div style={{ fontStyle: 'italic', color: 'var(--text-muted)', fontSize: '0.95rem', marginTop: '0.3rem' }}>
                Taxonomy: {disease.scientific_name}
              </div>
            )}
          </div>

          <Button variant="primary" icon={Camera} onClick={onScanCrop}>
            Scan a {disease.crop} Leaf
          </Button>
        </div>

        <p style={{ color: 'var(--text-secondary)', fontSize: '1rem', lineHeight: 1.7, margin: '1.5rem 0' }}>
          {disease.description}
        </p>

        {/* Treatment Tabs View */}
        <TreatmentTabs treatment={disease} />
      </div>
    </div>
  );
}
