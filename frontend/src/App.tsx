import React, { useState } from 'react';
import './App.css';
import CreateGameForm from './components/CreateGameForm';
import GameDashboard from './components/GameDashboard';
import ProtectedRoute from './components/auth/ProtectedRoute';
import EnhancedGameDashboard from './components/EnhancedGameDashboard';
import { GameSession } from './types/game';
import { Routes, Route, Navigate } from 'react-router-dom';
import AuthPage from './components/auth/AuthPage';

interface GameData {
  game_id: number;
  player_name: string;
  difficulty: string;
  status: string;
  economic_indicators: any;
  budget_data: any;
  message: string;
}

function mapGameDataToGameSession(data: GameData): GameSession {
  return {
    id: data.game_id,
    user: 0,
    current_turn: 1,
    current_year: 2025,
    current_quarter: 1,
    elections_passed: 0,
    is_active: true,
    created_at: '',
    updated_at: '',
    model_type: data.difficulty || 'basic',
    budget: 0,
    accumulated_reserves: 0,
    parameters: undefined,
    current_indicators: data.economic_indicators,
    current_budget: data.budget_data,
    current_events: [],
  };
}

function App() {
  const [gameData, setGameData] = useState<GameData | null>(null);
  const [showGameForm, setShowGameForm] = useState(true);

  const handleGameCreated = (data: GameData) => {
    setGameData(data);
    setShowGameForm(false);
  };

  // Функция для создания новой игры (пока не используется)
  // const handleNewGame = () => {
  //   setGameData(null);
  //   setShowGameForm(true);
  // };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎮 Президент: Экономика и Власть</h1>
        <p>Стратегическая игра управления экономикой</p>
      </header>
      <main className="App-main">
        <Routes>
          <Route path="/auth" element={<AuthPage />} />
          <Route path="/" element={
            showGameForm ? (
              <CreateGameForm onGameCreated={handleGameCreated} />
            ) : gameData && gameData.difficulty === 'enhanced' ? (
              <ProtectedRoute>
                <EnhancedGameDashboard gameId={gameData.game_id} onNextTurn={() => {}} />
              </ProtectedRoute>
            ) : (
              <ProtectedRoute>
                <GameDashboard key={gameData?.game_id} initialGame={gameData ? mapGameDataToGameSession(gameData) : undefined} />
              </ProtectedRoute>
            )
          } />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
