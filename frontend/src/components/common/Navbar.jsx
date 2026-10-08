import React, { useState } from 'react';
import { Sprout, Camera, History, BookOpen, User, LogOut, LogIn } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { Button } from './Button';

export function Navbar({ activePage, setActivePage, onOpenAuthModal }) {
  const { user, logout } = useAuth();
  const [dropdownOpen, setDropdownOpen] = useState(false);

  return (
    <nav className="navbar">
      <div className="container navbar-container">
        <div
          className="brand-logo"
          style={{ cursor: 'pointer' }}
          onClick={() => setActivePage('home')}
        >
          <div className="brand-icon">
            <Sprout size={20} />
          </div>
          <span>PhytoScan AI</span>
        </div>

        <ul className="nav-links">
          <li>
            <button
              className={`nav-link ${activePage === 'home' ? 'active' : ''}`}
              onClick={() => setActivePage('home')}
            >
              Home
            </button>
          </li>
          <li>
            <button
              className={`nav-link ${activePage === 'scan' ? 'active' : ''}`}
              onClick={() => setActivePage('scan')}
            >
              <Camera size={16} />
              Scan Leaf
            </button>
          </li>
          <li>
            <button
              className={`nav-link ${activePage === 'history' ? 'active' : ''}`}
              onClick={() => setActivePage('history')}
            >
              <History size={16} />
              History
            </button>
          </li>
          <li>
            <button
              className={`nav-link ${activePage === 'directory' ? 'active' : ''}`}
              onClick={() => setActivePage('directory')}
            >
              <BookOpen size={16} />
              Encyclopedia
            </button>
          </li>
        </ul>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.8rem' }}>
          {user ? (
            <div style={{ position: 'relative' }}>
              <Button
                variant="secondary"
                icon={User}
                onClick={() => setDropdownOpen(!dropdownOpen)}
              >
                {user.full_name ? user.full_name.split(' ')[0] : 'Farmer'}
              </Button>
              {dropdownOpen && (
                <div
                  className="glass-panel"
                  style={{
                    position: 'absolute',
                    right: 0,
                    top: '120%',
                    padding: '0.75rem',
                    minWidth: '180px',
                    zIndex: 200,
                  }}
                >
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
                    {user.email}
                  </div>
                  <Button
                    variant="outline"
                    icon={LogOut}
                    style={{ width: '100%', fontSize: '0.85rem' }}
                    onClick={() => {
                      logout();
                      setDropdownOpen(false);
                    }}
                  >
                    Sign Out
                  </Button>
                </div>
              )}
            </div>
          ) : (
            <Button
              variant="outline"
              icon={LogIn}
              onClick={onOpenAuthModal}
            >
              Sign In
            </Button>
          )}
        </div>
      </div>
    </nav>
  );
}
