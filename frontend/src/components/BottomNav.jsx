import React from 'react';
import { HomeIcon, GamesIcon, RemindersIcon, ProfileIcon } from './Icons';

export function BottomNav({ activeTab, onTabChange, reminderCount = 0 }) {
  const tabs = [
    { id: 'home', label: 'Home', icon: HomeIcon },
    { id: 'games', label: 'Games', icon: GamesIcon },
    { id: 'reminders', label: 'Reminders', icon: RemindersIcon, badge: reminderCount },
    { id: 'profile', label: 'Profile', icon: ProfileIcon },
  ];

  return (
    <nav className="smriti-bottom-nav" aria-label="Bottom Navigation">
      <div className="bottom-nav-inner">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;

          return (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={`nav-tab-btn ${isActive ? 'active' : ''}`}
              aria-label={tab.label}
              title={tab.label}
              aria-current={isActive ? 'page' : undefined}
            >
              <div className="nav-tab-pill">
                <Icon className="nav-icon" filled={isActive} />
                {tab.badge > 0 && (
                  <span className="nav-badge">{tab.badge}</span>
                )}
              </div>
            </button>
          );
        })}
      </div>
    </nav>
  );
}
