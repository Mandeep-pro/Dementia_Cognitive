import React, { useState } from 'react';
import { Camera, Heart, Users, MapPin, Sparkles, Image as ImageIcon } from 'lucide-react';
import { ArrowLeftIcon } from '../components/Icons';

function PolaroidCard({ mem, renderMemoryIcon }) {
  const [imgError, setImgError] = useState(false);

  const formattedDate = mem.date || (mem.created_at ? (() => {
    try {
      const d = new Date(mem.created_at);
      if (!isNaN(d.getTime())) {
        return d.toLocaleDateString(undefined, { month: 'short', year: 'numeric' });
      }
    } catch {
      // fallback
    }
    return 'Cherished';
  })() : 'Cherished');

  const hasImage = Boolean(mem.image_url && !imgError);

  return (
    <div className="polaroid-card">
      <div className="polaroid-photo-frame">
        {hasImage ? (
          <img
            src={mem.image_url}
            alt={mem.title || 'Memory photo'}
            className="polaroid-photo-img"
            onError={() => setImgError(true)}
            loading="lazy"
          />
        ) : (
          <div className="polaroid-visual-placeholder">
            <span className="polaroid-emoji" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              {renderMemoryIcon(mem.category)}
            </span>
          </div>
        )}
        <span className="polaroid-badge-date">{formattedDate}</span>
      </div>

      <div className="polaroid-caption">
        <h3 className="polaroid-title">{mem.title}</h3>
        {mem.description && <p className="polaroid-desc">{mem.description}</p>}
      </div>
    </div>
  );
}

export function MemoriesView({ memories = [], onBack }) {
  const renderMemoryIcon = (cat) => {
    if (cat === 'family') return <Users size={32} color="#0D9488" />;
    if (cat === 'place') return <MapPin size={32} color="#10B981" />;
    if (cat === 'event') return <Sparkles size={32} color="#F59E0B" />;
    if (cat === 'person') return <Heart size={32} color="#EC4899" />;
    return <ImageIcon size={32} color="#0D9488" />;
  };

  return (
    <div className="tab-view-container animate-fade-in">
      <div className="view-header flex-header">
        {onBack && (
          <button onClick={onBack} className="btn-icon-back" aria-label="Back">
            <ArrowLeftIcon className="w-5 h-5" />
          </button>
        )}
        <div>
          <h1 className="view-title" style={{ display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
            <span>Cherished Memories</span>
            <Camera size={22} color="#0D9488" />
          </h1>
          <p className="view-sub">Photos, stories, and heartwarming moments.</p>
        </div>
      </div>

      {memories.length === 0 ? (
        <div className="empty-state-card" style={{ textAlign: 'center', padding: '40px 20px', background: '#F8FAFC', borderRadius: '16px', border: '1px dashed #CBD5E1', marginTop: '16px' }}>
          <ImageIcon size={44} color="#94A3B8" style={{ margin: '0 auto 12px', display: 'block' }} />
          <h3 style={{ fontSize: '17px', fontWeight: 700, color: '#334155', marginBottom: '6px' }}>No memories yet</h3>
          <p style={{ fontSize: '13.5px', color: '#64748B', lineHeight: '1.4' }}>Your caregiver can add special photos and stories here.</p>
        </div>
      ) : (
        <div className="memories-grid">
          {memories.map((mem) => (
            <PolaroidCard
              key={mem.id || mem._id || `${mem.title}-${mem.created_at}`}
              mem={mem}
              renderMemoryIcon={renderMemoryIcon}
            />
          ))}
        </div>
      )}
    </div>
  );
}

