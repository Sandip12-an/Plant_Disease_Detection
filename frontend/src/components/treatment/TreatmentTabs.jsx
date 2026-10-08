import React, { useState } from 'react';
import { Leaf, FlaskConical, Shield, Info, AlertTriangle } from 'lucide-react';

export function TreatmentTabs({ treatment, warning }) {
  const [activeTab, setActiveTab] = useState('organic'); // 'organic' | 'chemical' | 'prevention' | 'symptoms'

  if (!treatment) return null;

  return (
    <div>
      {warning && (
        <div
          style={{
            background: 'rgba(251, 191, 36, 0.12)',
            border: '1px solid rgba(251, 191, 36, 0.3)',
            color: 'var(--amber-warning)',
            padding: '0.75rem 1rem',
            borderRadius: '10px',
            marginBottom: '1.2rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.6rem',
            fontSize: '0.85rem',
          }}
        >
          <AlertTriangle size={18} />
          <span>{warning}</span>
        </div>
      )}

      {/* Tabs Header */}
      <div className="treatment-tabs-nav">
        <button
          type="button"
          className={`treatment-tab-btn ${activeTab === 'organic' ? 'active' : ''}`}
          onClick={() => setActiveTab('organic')}
        >
          <Leaf size={16} />
          Organic & Bio
        </button>

        <button
          type="button"
          className={`treatment-tab-btn ${activeTab === 'chemical' ? 'active' : ''}`}
          onClick={() => setActiveTab('chemical')}
        >
          <FlaskConical size={16} />
          Chemical Control
        </button>

        <button
          type="button"
          className={`treatment-tab-btn ${activeTab === 'prevention' ? 'active' : ''}`}
          onClick={() => setActiveTab('prevention')}
        >
          <Shield size={16} />
          Prevention
        </button>

        <button
          type="button"
          className={`treatment-tab-btn ${activeTab === 'symptoms' ? 'active' : ''}`}
          onClick={() => setActiveTab('symptoms')}
        >
          <Info size={16} />
          Symptoms
        </button>
      </div>

      {/* Tab Content Panels */}
      <div className="treatment-content-box">
        {activeTab === 'organic' && (
          <div>
            <h4 style={{ color: 'var(--emerald-300)', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Leaf size={18} />
              Biological & Eco-Friendly Management
            </h4>
            <p style={{ color: 'var(--text-primary)', fontSize: '0.95rem' }}>
              {treatment.organic_treatment}
            </p>
          </div>
        )}

        {activeTab === 'chemical' && (
          <div>
            <h4 style={{ color: 'var(--teal-accent)', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <FlaskConical size={18} />
              Targeted Chemical Sprays & Active Ingredients
            </h4>
            <p style={{ color: 'var(--text-primary)', fontSize: '0.95rem' }}>
              {treatment.chemical_treatment || 'No chemical treatment required for healthy crops.'}
            </p>
          </div>
        )}

        {activeTab === 'prevention' && (
          <div>
            <h4 style={{ color: 'var(--lime-accent)', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Shield size={18} />
              Cultural Hygiene & Long-Term Prevention
            </h4>
            <p style={{ color: 'var(--text-primary)', fontSize: '0.95rem' }}>
              {treatment.prevention}
            </p>
          </div>
        )}

        {activeTab === 'symptoms' && (
          <div>
            <h4 style={{ color: 'var(--amber-warning)', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Info size={18} />
              Pathology & Diagnostic Indicators
            </h4>
            <p style={{ color: 'var(--text-primary)', fontSize: '0.95rem', marginBottom: '0.8rem' }}>
              <strong>Symptoms:</strong> {treatment.symptoms}
            </p>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.88rem' }}>
              {treatment.description}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
