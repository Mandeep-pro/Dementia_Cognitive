import React from 'react';
import { Volume2 } from 'lucide-react';

export function ProfileView({
  patient,
  backendStatus,
  textSize,
  onTextSizeChange,
  onLogout
}) {
  return (
    <div className="tab-view-container animate-fade-in">
      <div className="profile-hero">
        <div className="profile-avatar-large">
          <img
            src="/placeholder_avatar.svg"
            alt={patient?.preferred_name || patient?.name || 'User Profile'}
            className="avatar-large-img"
          />
        </div>

        <h1 className="profile-name">{patient?.preferred_name || patient?.name || 'My Account'}</h1>
        <p className="profile-subtitle">
          {patient?.age ? `Age ${patient.age} · ` : ''}
          {patient?.email || patient?.preferred_language || 'SmritiRoots Member'}
        </p>

        {patient?.caregiver_name && (
          <div className="caregiver-pill">
            <span className="caregiver-dot"></span>
            <span>Caregiver: {patient.caregiver_name}</span>
          </div>
        )}
      </div>

      {/* Accessibility Settings */}
      <section className="profile-section">
        <h2 className="section-title">Elder Accessibility & Comfort</h2>

        <div className="setting-card">
          <span className="setting-label">Text Size</span>
          <div className="text-size-pills">
            {['normal', 'large', 'xlarge'].map((size) => (
              <button
                key={size}
                onClick={() => onTextSizeChange(size)}
                className={`size-pill ${textSize === size ? 'active' : ''}`}
              >
                {size === 'normal' ? 'Normal' : size === 'large' ? 'Large (Aa)' : 'Extra Large (AA)'}
              </button>
            ))}
          </div>
        </div>

        <div className="setting-card">
          <span className="setting-label">Preferred Language</span>
          <span className="setting-value">{patient?.preferred_language || 'Hindi / English'}</span>
        </div>

        <div className="setting-card">
          <span className="setting-label">Voice Read Aloud</span>
          <span className="setting-badge-green" style={{ display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
            <span>Enabled</span>
            <Volume2 size={13} />
          </span>
        </div>
      </section>

      {/* Personal Context & Memories */}
      <section className="profile-section">
        <h2 className="section-title">Personal Information & Family</h2>

        <div className="info-card">
          <h3 className="info-title">Beloved Family</h3>
          <ul className="info-list">
            {patient?.family?.map((f, i) => (
              <li key={i}>{f}</li>
            ))}
          </ul>
        </div>

        <div className="info-card">
          <h3 className="info-title">Favorite Comforts</h3>
          <ul className="info-list">
            {patient?.favorite_things?.map((f, i) => (
              <li key={i}>{f}</li>
            ))}
          </ul>
        </div>
      </section>

      {/* System & Backend Status */}
      <section className="profile-section">
        <div className="system-status-box">
          <span className="system-status-label">SmritiRoots Backend API</span>
          <span className={`system-status-badge ${backendStatus === 'online' ? 'online' : 'preview'}`}>
            {backendStatus === 'online' ? '● Connected to Flask API (Port 5000)' : '● Interactive Mode'}
          </span>
        </div>

        {onLogout && (
          <button
            onClick={onLogout}
            className="btn-logout"
            aria-label="Sign out of account"
          >
            Sign Out of Account
          </button>
        )}
      </section>
    </div>
  );
}
