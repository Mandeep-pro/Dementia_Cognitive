import React from 'react';
import { Puzzle } from 'lucide-react';
import { BrainIcon, ArrowRightIcon } from '../components/Icons';

export function GamesView({ games = [], onPlayGame }) {
  return (
    <div className="tab-view-container animate-fade-in">
      <div className="view-header">
        <h1 className="view-title" style={{ display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
          <span>Mind Games</span>
          <Puzzle size={22} color="#0D9488" />
        </h1>
        <p className="view-sub">Comforting activities to boost memory and focus.</p>
      </div>

      <div className="games-grid">
        {games.map((game) => (
          <div key={game.id} className="game-item-card">
            <div className="game-card-top">
              <div className="game-icon-circle">
                <BrainIcon className="game-item-icon" />
              </div>
              <span className="game-badge">{game.badge || 'Brain Exercise'}</span>
            </div>

            <h3 className="game-item-title">{game.name}</h3>
            <p className="game-item-desc">{game.description}</p>

            <button
              onClick={() => onPlayGame(game)}
              className="card-btn btn-game-item"
              aria-label={`Play ${game.name}`}
            >
              <span>Play Now</span>
              <ArrowRightIcon className="btn-arrow-icon" />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
