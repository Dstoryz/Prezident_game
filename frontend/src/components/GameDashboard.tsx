import React, { useState, useEffect } from 'react';
import { GameSession } from '../types/game';
import { gameApi } from '../services/api';
import ParametersPanel from './ParametersPanel';
import IndicatorsPanel from './IndicatorsPanel';
import EventsPanel from './EventsPanel';
import GameChart from './GameChart';
import GameTips from './GameTips';
import UserProfile from './auth/UserProfile';
import { useAuth } from '../contexts/AuthContext';
import './GameDashboard.css';

const GameDashboard: React.FC = () => {
  const [game, setGame] = useState<GameSession | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [gameOver, setGameOver] = useState(false);
  const [gameOverReason, setGameOverReason] = useState<string | null>(null);
  const [chartRefreshTrigger, setChartRefreshTrigger] = useState(0); // Триггер для обновления графика
  const { logout } = useAuth();

  // Начать новую игру
  const startNewGame = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await gameApi.startGame();
      if (response.success && response.game) {
        setGame(response.game);
        setGameOver(false);
        setGameOverReason(null);
        setChartRefreshTrigger(prev => prev + 1); // Обновляем график
      } else {
        setError(response.message);
      }
    } catch (err) {
      setError('Ошибка при создании игры');
    } finally {
      setLoading(false);
    }
  };

  // Сделать следующий ход
  const handleNextTurn = async (parameters: any) => {
    if (!game) return;

    console.log('GameDashboard: handleNextTurn вызван с параметрами:', parameters);
    setLoading(true);
    setError(null);
    try {
      const response = await gameApi.nextTurn(game.id, parameters);
      console.log('GameDashboard: получен ответ:', response);
      if (response.success && response.game) {
        setGame(response.game);
        setChartRefreshTrigger(prev => prev + 1); // Обновляем график после хода
        
        if (response.game_over) {
          setGameOver(true);
          setGameOverReason(response.game_over_reason || 'Игра окончена');
        }
      } else {
        setError(response.message);
      }
    } catch (err) {
      console.error('GameDashboard: ошибка при обработке хода:', err);
      setError('Ошибка при обработке хода');
    } finally {
      setLoading(false);
    }
  };

  // Обновить состояние игры
  const refreshGameState = async () => {
    if (!game) return;

    try {
      const response = await gameApi.getGameState(game.id);
      if (response.success && response.game) {
        setGame(response.game);
        setChartRefreshTrigger(prev => prev + 1); // Обновляем график
      }
    } catch (err) {
      setError('Ошибка при обновлении состояния');
    }
  };

  useEffect(() => {
    // Автоматически начинаем игру при загрузке
    startNewGame();
  }, []);

  if (loading && !game) {
    return (
      <div className="game-dashboard">
        <div className="loading">Загрузка игры...</div>
      </div>
    );
  }

  if (error && !game) {
    return (
      <div className="game-dashboard">
        <div className="error">
          <h2>Ошибка</h2>
          <p>{error}</p>
          <button onClick={startNewGame}>Попробовать снова</button>
          <button onClick={logout} style={{marginTop: '16px', background: '#dc3545', color: 'white', padding: '10px 20px', border: 'none', borderRadius: '8px', fontWeight: 600, cursor: 'pointer'}}>Выйти</button>
        </div>
      </div>
    );
  }

  if (gameOver) {
    return (
      <div className="game-dashboard">
        <div className="game-over">
          <h2>Игра окончена</h2>
          <p>{gameOverReason}</p>
          <button onClick={startNewGame}>Начать новую игру</button>
        </div>
      </div>
    );
  }

  if (!game) {
    return (
      <div className="game-dashboard">
        <button onClick={startNewGame}>Начать игру</button>
      </div>
    );
  }

  return (
    <div className="game-dashboard">
      <header className="game-header">
        <div className="header-left">
          <h1>Президент: Экономика и Власть</h1>
          <div className="game-info">
            <span>Ход: {game.current_turn || game.turn}</span>
            <span>Год: {game.current_year}</span>
            <span>Квартал: {game.current_quarter}</span>
            <span>Выборы: {game.elections_passed}</span>
          </div>
        </div>
        <div className="header-right">
          <UserProfile />
        </div>
      </header>

      <div className="game-content">
        <div className="left-panel">
          {game.parameters && (
            <ParametersPanel 
              parameters={game.parameters}
              onNextTurn={handleNextTurn}
              loading={loading}
            />
          )}
          
          {game.current_indicators && (
            <IndicatorsPanel indicators={game.current_indicators} budget={game.current_budget} />
          )}
        </div>

        <div className="right-panel">
          <GameChart gameId={game.id} refreshTrigger={chartRefreshTrigger} />
          
          <GameTips 
            modelType={game.model_type as 'basic' | 'enhanced'}
          />
          
          <EventsPanel events={game.current_events} />
        </div>
      </div>

      <footer className="game-footer">
        <button onClick={refreshGameState} disabled={loading}>
          Обновить
        </button>
        <button onClick={startNewGame} disabled={loading}>
          Новая игра
        </button>
      </footer>
    </div>
  );
};

export default GameDashboard; 