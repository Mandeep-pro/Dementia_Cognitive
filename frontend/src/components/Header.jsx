import React from 'react';
import { LogoIcon } from './Icons';

export function Header({ patient, onAvatarClick }) {
  return (
    <header className="smriti-header">
      {/* Brand Logo & Name */}
      <div className="brand-group">
        <LogoIcon className="brand-icon" />
        <div className="brand-text">
          <span className="brand-title">SmritiRoots</span>
          <span className="brand-tagline">Play · Remember · Live Better</span>
        </div>
      </div>

      {/* User Avatar */}
      <button
        onClick={onAvatarClick}
        className="avatar-btn"
        aria-label={`Open ${patient?.preferred_name || patient?.name || 'User'} Profile`}
        title="View Profile"
      >
        <img
          src="/placeholder_avatar.svg"
          alt={patient?.preferred_name || patient?.name || "User"}
          className="avatar-img"
        />
      </button>
    </header>
  );
}
