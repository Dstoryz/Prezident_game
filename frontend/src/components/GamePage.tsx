import React from 'react';
import GameDashboard from './GameDashboard';
import './GamePage.css';

const GamePage: React.FC = () => {
  return (
    <div className="game-page">
      <header className="game-header">
        <h1>🎮 Президент: Экономика и Власть</h1>
        <div className="game-info">
          <span className="game-status">Игра активна</span>
        </div>
      </header>
      
      <main className="game-main">
        <GameDashboard />
      </main>
      
      <footer className="game-footer">
        <p>© 2025 Президент: Экономика и Власть - Стратегическая игра</p>
      </footer>
    </div>
  );
};

export default GamePage; 