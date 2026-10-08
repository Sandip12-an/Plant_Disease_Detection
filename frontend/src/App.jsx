import React, { useState } from 'react';
import { AuthProvider } from './context/AuthContext';
import { ScanProvider } from './context/ScanContext';
import { Navbar } from './components/common/Navbar';
import { AuthModal } from './components/common/AuthModal';
import { HomePage } from './pages/HomePage';
import { ScanPage } from './pages/ScanPage';
import { HistoryPage } from './pages/HistoryPage';
import { DiseaseDirectoryPage } from './pages/DiseaseDirectoryPage';
import { DiseaseDetailPage } from './pages/DiseaseDetailPage';
import { Sprout } from 'lucide-react';

export function AppContent() {
  const [activePage, setActivePage] = useState('home'); // 'home' | 'scan' | 'history' | 'directory' | 'detail'
  const [selectedDiseaseId, setSelectedDiseaseId] = useState(null);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);

  const handleSelectDisease = (diseaseId) => {
    setSelectedDiseaseId(diseaseId);
    setActivePage('detail');
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Navbar
        activePage={activePage}
        setActivePage={(page) => {
          setActivePage(page);
          if (page !== 'detail') setSelectedDiseaseId(null);
        }}
        onOpenAuthModal={() => setIsAuthModalOpen(true)}
      />

      <main style={{ flex: 1 }}>
        {activePage === 'home' && (
          <HomePage
            onStartScanning={() => setActivePage('scan')}
            onBrowseDirectory={() => setActivePage('directory')}
          />
        )}

        {activePage === 'scan' && <ScanPage />}

        {activePage === 'history' && <HistoryPage />}

        {activePage === 'directory' && (
          <DiseaseDirectoryPage onSelectDisease={handleSelectDisease} />
        )}

        {activePage === 'detail' && (
          <DiseaseDetailPage
            diseaseId={selectedDiseaseId}
            onBack={() => setActivePage('directory')}
            onScanCrop={() => setActivePage('scan')}
          />
        )}
      </main>

      <AuthModal
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
      />

      {/* Footer */}
      <footer
        style={{
          borderTop: '1px solid var(--border-subtle)',
          padding: '2.5rem 0',
          background: 'rgba(8, 15, 10, 0.9)',
          marginTop: 'auto',
        }}
      >
        <div
          className="container"
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            flexWrap: 'wrap',
            gap: '1rem',
            fontSize: '0.88rem',
            color: 'var(--text-muted)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <Sprout size={18} style={{ color: 'var(--emerald-400)' }} />
            <span style={{ fontWeight: 600, color: 'var(--text-primary)' }}>PhytoScan AI</span>
            <span>— Precision Agricultural Vision Platform</span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
            <span>Powered by MobileNetV2 & ONNX Runtime</span>
            <span style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
              Built for Farmers Worldwide
            </span>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <ScanProvider>
        <AppContent />
      </ScanProvider>
    </AuthProvider>
  );
}
