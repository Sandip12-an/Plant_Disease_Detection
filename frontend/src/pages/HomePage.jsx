import React from 'react';
import { Camera, Sparkles, ShieldCheck, Activity, BookOpen, ArrowRight, Zap, Eye } from 'lucide-react';
import { Button } from '../components/common/Button';

export function HomePage({ onStartScanning, onBrowseDirectory }) {
  return (
    <div>
      {/* Hero Section */}
      <section className="hero-section">
        <div className="container">
          <div className="hero-pill">
            <Sparkles size={16} />
            <span>MobileNetV2 Vision Architecture • Sub-30ms Inference</span>
          </div>

          <h1 className="hero-title">
            Intelligent Plant Disease Detection & Agronomic Remedy
          </h1>

          <p className="hero-subtitle">
            Upload or snap a plant leaf photo to instantly detect pathogen infections,
            inspect Grad-CAM visual lesion heatmaps, and obtain biological & chemical treatment plans.
          </p>

          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
            <Button
              variant="primary"
              icon={Camera}
              style={{ padding: '0.9rem 2rem', fontSize: '1.05rem' }}
              onClick={onStartScanning}
            >
              Launch Leaf Scanner
            </Button>
            <Button
              variant="secondary"
              icon={BookOpen}
              style={{ padding: '0.9rem 1.8rem', fontSize: '1.05rem' }}
              onClick={onBrowseDirectory}
            >
              Browse Disease Catalog
            </Button>
          </div>

          {/* Quick Metrics Bar */}
          <div className="hero-stats">
            <div className="glass-panel stat-card">
              <div className="stat-number">38</div>
              <div className="stat-label">Crop Disease & Healthy Classes</div>
            </div>
            <div className="glass-panel stat-card">
              <div className="stat-number">14</div>
              <div className="stat-label">Major Agricultural Crops Covered</div>
            </div>
            <div className="glass-panel stat-card">
              <div className="stat-number">&lt; 30ms</div>
              <div className="stat-label">Ultra-Fast ONNX Serving Latency</div>
            </div>
            <div className="glass-panel stat-card">
              <div className="stat-number">Grad-CAM</div>
              <div className="stat-label">Visual Lesion Explainability</div>
            </div>
          </div>
        </div>
      </section>

      {/* Feature Highlights Section */}
      <section style={{ padding: '4rem 0' }}>
        <div className="container">
          <h2 style={{ fontSize: '2rem', textAlign: 'center', marginBottom: '2.5rem' }}>
            How PhytoScan AI Empowers Crop Care
          </h2>

          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
              gap: '2rem',
            }}
          >
            <div className="glass-panel" style={{ padding: '2rem' }}>
              <div
                style={{
                  width: '48px',
                  height: '48px',
                  background: 'rgba(16, 185, 129, 0.15)',
                  borderRadius: '12px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'var(--emerald-400)',
                  marginBottom: '1.2rem',
                }}
              >
                <Zap size={24} />
              </div>
              <h3 style={{ fontSize: '1.25rem', marginBottom: '0.6rem' }}>Instant Lab-Grade Inference</h3>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem' }}>
                Optimized transfer learning models running on CPU/GPU via ONNX runtime deliver immediate diagnosis without heavy cloud latency.
              </p>
            </div>

            <div className="glass-panel" style={{ padding: '2rem' }}>
              <div
                style={{
                  width: '48px',
                  height: '48px',
                  background: 'rgba(20, 184, 166, 0.15)',
                  borderRadius: '12px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'var(--teal-accent)',
                  marginBottom: '1.2rem',
                }}
              >
                <Eye size={24} />
              </div>
              <h3 style={{ fontSize: '1.25rem', marginBottom: '0.6rem' }}>Visual Explainability (Grad-CAM)</h3>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem' }}>
                Look inside the neural network. See exactly which necrosis spots, chlorotic rings, or powdery mildew spores triggered the AI prediction.
              </p>
            </div>

            <div className="glass-panel" style={{ padding: '2rem' }}>
              <div
                style={{
                  width: '48px',
                  height: '48px',
                  background: 'rgba(163, 230, 53, 0.15)',
                  borderRadius: '12px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'var(--lime-accent)',
                  marginBottom: '1.2rem',
                }}
              >
                <ShieldCheck size={24} />
              </div>
              <h3 style={{ fontSize: '1.25rem', marginBottom: '0.6rem' }}>Integrated Remedy Protocols</h3>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem' }}>
                Get certified organic bio-fungicide options (neem oil, Bacillus), registered chemical controls with active ingredients, and crop hygiene strategies.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
