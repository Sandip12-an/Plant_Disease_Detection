import React, { useState, useEffect } from 'react';
import { Search, Filter, BookOpen, ArrowRight, ShieldCheck, AlertCircle } from 'lucide-react';
import { diseaseService } from '../services/diseaseService';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { Badge } from '../components/common/Badge';

export function DiseaseDirectoryPage({ onSelectDisease }) {
  const [crops, setCrops] = useState([]);
  const [selectedCrop, setSelectedCrop] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [diseases, setDiseases] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadCrops() {
      try {
        const cropList = await diseaseService.getCrops();
        setCrops(cropList);
      } catch (err) {
        console.error('Failed to load crops:', err);
      }
    }
    loadCrops();
  }, []);

  useEffect(() => {
    async function loadDiseases() {
      setLoading(true);
      try {
        const data = await diseaseService.getDiseases({
          crop: selectedCrop,
          search: searchQuery,
          limit: 50,
        });
        setDiseases(data.items || []);
      } catch (err) {
        console.error('Failed to load diseases:', err);
      } finally {
        setLoading(false);
      }
    }

    const timer = setTimeout(() => {
      loadDiseases();
    }, 200);

    return () => clearTimeout(timer);
  }, [selectedCrop, searchQuery]);

  return (
    <div className="container" style={{ padding: '3rem 1.5rem 5rem' }}>
      <div style={{ textAlign: 'center', marginBottom: '2.5rem' }}>
        <h1 style={{ fontSize: '2.4rem', marginBottom: '0.6rem' }}>
          Crop Pathology Encyclopedia
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '1rem', maxWidth: '650px', margin: '0 auto' }}>
          Explore symptoms, causative pathogens, biological solutions, and prevention strategies across all 38 supported disease classes.
        </p>
      </div>

      {/* Search and Filters Bar */}
      <div
        className="glass-panel"
        style={{
          padding: '1.25rem',
          marginBottom: '2.5rem',
          display: 'flex',
          gap: '1rem',
          flexWrap: 'wrap',
          alignItems: 'center',
        }}
      >
        {/* Search Input */}
        <div style={{ flex: '1 1 280px', position: 'relative' }}>
          <Search
            size={18}
            style={{
              position: 'absolute',
              left: '12px',
              top: '50%',
              transform: 'translateY(-50%)',
              color: 'var(--text-muted)',
            }}
          />
          <input
            type="text"
            placeholder="Search by disease name, symptom, or pathogen..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{
              width: '100%',
              padding: '0.75rem 1rem 0.75rem 2.4rem',
              background: 'var(--bg-surface-elevated)',
              border: '1px solid var(--border-subtle)',
              borderRadius: '10px',
              color: 'var(--text-primary)',
              fontSize: '0.95rem',
              outline: 'none',
            }}
          />
        </div>

        {/* Crop Selector */}
        <div style={{ flex: '0 1 220px' }}>
          <select
            value={selectedCrop}
            onChange={(e) => setSelectedCrop(e.target.value)}
            style={{
              width: '100%',
              padding: '0.75rem 1rem',
              background: 'var(--bg-surface-elevated)',
              border: '1px solid var(--border-subtle)',
              borderRadius: '10px',
              color: 'var(--text-primary)',
              fontSize: '0.95rem',
              outline: 'none',
              cursor: 'pointer',
            }}
          >
            <option value="">All Crop Species ({crops.length})</option>
            {crops.map((crop) => (
              <option key={crop} value={crop}>
                {crop}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Disease Cards Grid */}
      {loading ? (
        <div style={{ padding: '4rem', textAlign: 'center' }}>
          <LoadingSpinner size={36} text="Querying agronomic database..." />
        </div>
      ) : diseases.length === 0 ? (
        <div className="glass-panel" style={{ padding: '3.5rem', textAlign: 'center' }}>
          <BookOpen size={44} style={{ color: 'var(--text-muted)', marginBottom: '1rem' }} />
          <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>No Diseases Found</h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
            No records matched your search query. Try clearing filters or searching for terms like "blight" or "rust".
          </p>
        </div>
      ) : (
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
            gap: '1.5rem',
          }}
        >
          {diseases.map((d) => (
            <div
              key={d.id}
              className="glass-panel"
              style={{
                padding: '1.5rem',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                cursor: 'pointer',
              }}
              onClick={() => onSelectDisease(d.id)}
            >
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.6rem' }}>
                  <span style={{ fontSize: '0.8rem', color: 'var(--emerald-400)', fontWeight: 600, textTransform: 'uppercase' }}>
                    {d.crop}
                  </span>
                  <Badge status={d.is_healthy ? 'healthy' : 'severe'} text={d.is_healthy ? 'Healthy' : 'Diseased'} />
                </div>

                <h3 style={{ fontSize: '1.2rem', marginBottom: '0.6rem', color: '#fff' }}>
                  {d.name}
                </h3>

                <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: 1.5, marginBottom: '1rem' }}>
                  {d.symptoms.length > 140 ? `${d.symptoms.substring(0, 140)}...` : d.symptoms}
                </p>
              </div>

              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.4rem',
                  fontSize: '0.85rem',
                  color: 'var(--emerald-300)',
                  fontWeight: 600,
                  marginTop: '0.5rem',
                }}
              >
                <span>View Full Treatment & Symptoms</span>
                <ArrowRight size={14} />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
