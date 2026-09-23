import React from 'react';

// SmritiRoots Sprout/Leaf Logo
export function LogoIcon({ className = 'w-7 h-7' }) {
  return (
    <svg className={className} viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
      {/* Top golden leaf */}
      <path
        d="M17.5 4C23.5 4 28 8.5 28 14.5C28 20 23 23.5 17.5 24C16.8 17.5 20 9.5 17.5 4Z"
        fill="#D49A36"
      />
      <path
        d="M21.5 8C25.5 11 26 15 25.5 17.5"
        stroke="#E9B958"
        strokeWidth="1.5"
        strokeLinecap="round"
      />
      {/* Bottom forest green leaf */}
      <path
        d="M16 11C10 11.5 6 16 6 22C6 27.5 11 31 16.5 31.5C17.2 25 13.5 17 16 11Z"
        fill="#1E5038"
      />
      <path
        d="M12 17C8.5 20.5 8.5 24.5 9.5 27"
        stroke="#2E7051"
        strokeWidth="1.5"
        strokeLinecap="round"
      />
      {/* Central sprout stem */}
      <path
        d="M16.5 32C17 26 18 19 23 15"
        stroke="#1E5038"
        strokeWidth="2"
        strokeLinecap="round"
      />
    </svg>
  );
}

// Read Aloud Speaker Icon
export function SpeakerIcon({ className = 'w-5 h-5' }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" fill="currentColor" fillOpacity="0.15" />
      <path d="M15.54 8.46a5 5 0 0 1 0 7.07" />
      <path d="M19.07 4.93a10 10 0 0 1 0 14.14" />
    </svg>
  );
}

// Golden Bell Icon
export function BellIcon({ className = 'w-6 h-6', fill = '#A75A26' }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path
        d="M12 3C8.686 3 6 5.686 6 9V14.5L4.5 16.5C4.05 17.1 4.45 18 5.2 18H18.8C19.55 18 19.95 17.1 19.5 16.5L18 14.5V9C18 5.686 15.314 3 12 3Z"
        fill={fill}
      />
      <path
        d="M10 19C10 20.1 10.9 21 12 21C13.1 21 14 20.1 14 19"
        stroke={fill}
        strokeWidth="2"
        strokeLinecap="round"
      />
    </svg>
  );
}

// Medicine Capsule Pill Icon
export function PillIcon({ className = 'w-7 h-7' }) {
  return (
    <svg className={className} viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
      <g transform="rotate(-45 16 16)">
        {/* Top half red/coral */}
        <path
          d="M11 6C11 3.23858 13.2386 1 16 1C18.7614 1 21 3.23858 21 6V15H11V6Z"
          fill="#D9383A"
        />
        {/* Bottom half white/cream */}
        <path
          d="M11 15H21V26C21 28.7614 18.7614 31 16 31C13.2386 31 11 28.7614 11 26V15Z"
          fill="#FFFFFF"
          stroke="#E5E7EB"
          strokeWidth="1"
        />
        {/* Highlight sheen */}
        <path
          d="M13 4V13"
          stroke="rgba(255,255,255,0.6)"
          strokeWidth="1.5"
          strokeLinecap="round"
        />
      </g>
    </svg>
  );
}

// Brain Mascot Icon (Stylized 3D Brain)
export function BrainIcon({ className = 'w-6 h-6', color = '#5539A2' }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 4.44-2.04" />
      <path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-4.44-2.04" />
    </svg>
  );
}

// Home Nav Icon
export function HomeIcon({ className = 'w-6 h-6', filled = false }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill={filled ? 'currentColor' : 'none'} stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M3 9.5L12 3L21 9.5V20C21 20.5523 20.5523 21 20 21H15V14H9V21H4C3.44772 21 3 20.5523 3 20V9.5Z" />
    </svg>
  );
}

// Gamepad Nav Icon
export function GamesIcon({ className = 'w-6 h-6', filled = false }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill={filled ? 'currentColor' : 'none'} stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="2" y="6" width="20" height="12" rx="6" />
      <path d="M6 12H10" />
      <path d="M8 10V14" />
      <circle cx="15" cy="13" r="1" fill="currentColor" />
      <circle cx="18" cy="11" r="1" fill="currentColor" />
    </svg>
  );
}

// Reminders / Calendar Nav Icon
export function RemindersIcon({ className = 'w-6 h-6', filled = false }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill={filled ? 'currentColor' : 'none'} stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="4" width="18" height="18" rx="4" />
      <line x1="16" y1="2" x2="16" y2="6" />
      <line x1="8" y1="2" x2="8" y2="6" />
      <line x1="3" y1="10" x2="21" y2="10" />
      <path d="M8 14H8.01" strokeWidth="3" />
      <path d="M12 14H12.01" strokeWidth="3" />
      <path d="M16 14H16.01" strokeWidth="3" />
    </svg>
  );
}

// Profile Nav Icon
export function ProfileIcon({ className = 'w-6 h-6', filled = false }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill={filled ? 'currentColor' : 'none'} stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M20 21V19C20 16.7909 18.2091 15 16 15H8C5.79086 15 4 16.7909 4 19V21" />
      <circle cx="12" cy="7" r="4" />
    </svg>
  );
}

// Chevron Left / Back Icon
export function ChevronLeftIcon({ className = 'w-6 h-6' }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M15 19L8 12L15 5" />
    </svg>
  );
}

// Arrow Right Icon
export function ArrowRightIcon({ className = 'w-5 h-5' }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M5 12H19" />
      <path d="M12 5L19 12L12 19" />
    </svg>
  );
}

// Arrow Left Icon
export function ArrowLeftIcon({ className = 'w-5 h-5' }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M19 12H5" />
      <path d="M12 19L5 12L12 5" />
    </svg>
  );
}

// Check Icon
export function CheckIcon({ className = 'w-5 h-5' }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="20 6 9 17 4 12" />
    </svg>
  );
}
