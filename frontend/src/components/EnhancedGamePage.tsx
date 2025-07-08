import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import EnhancedGameDashboard from './EnhancedGameDashboard';
import GameChart from './GameChart';
import GameTips from './GameTips';
import './EnhancedGamePage.css';

interface GameSession {
  id: number;
  turn: number;
  model_type: string;
  is_active: boolean;
}

const EnhancedGamePage: React.FC = () => {
  const { gameId } = useParams<{ gameId: string }>();
  const navigate = useNavigate();
  const [gameSession, setGameSession] = useState<GameSession | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'dashboard' | 'chart' | 'tips'>('dashboard');
  const [gameHistory, setGameHistory] = useState<any[]>([]);

  useEffect(() => {
    if (gameId) {
      loadGameSession();
    }
  }, [gameId]);

  const loadGameSession = async () => {
    try {
      setLoading(true);
      const response = await fetch(`/api/game/enhanced/${gameId}/enhanced_state/`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setGameSession(data.game);
        
        // Загружаем историю игры для графика
        loadGameHistory();
      } else {
        setError('Игра не найдена или недоступна');
      }
    } catch (err) {
      setError('Ошибка подключения к серверу');
    } finally {
      setLoading(false);
    }
  };

  const loadGameHistory = async () => {
    try {
      const response = await fetch(`/api/game/enhanced/${gameId}/history/`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setGameHistory(data.history || []);
      }
    } catch (err) {
      console.error('Ошибка загрузки истории:', err);
    }
  };

  const handleNextTurn = async (parameters: any) => {
    // Обновляем историю после хода
    await loadGameHistory();
  };

  const handleNewGame = () => {
    navigate('/game/new');
  };

  const handleBackToMenu = () => {
    navigate('/');
  };

  if (loading) {
    return (
      <div className="enhanced-game-page loading">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Загрузка игры...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="enhanced-game-page error">
        <div className="error-content">
          <h2>Ошибка</h2>
          <p>{error}</p>
          <div className="error-actions">
            <button onClick={handleBackToMenu}>Вернуться в меню</button>
            <button onClick={handleNewGame}>Новая игра</button>
          </div>
        </div>
      </div>
    );
  }

  if (!gameSession) {
    return (
      <div className="enhanced-game-page error">
        <div className="error-content">
          <h2>Игра не найдена</h2>
          <p>Запрашиваемая игра не существует или была удалена.</p>
          <div className="error-actions">
            <button onClick={handleBackToMenu}>Вернуться в меню</button>
            <button onClick={handleNewGame}>Новая игра</button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="enhanced-game-page">
      {/* Верхняя панель навигации */}
      <div className="game-header">
        <div className="game-info">
          <h1>Президент: Экономическая стратегия</h1>
          <div className="game-meta">
            <span className="game-id">Игра #{gameSession.id}</span>
            <span className="turn-counter">Ход {gameSession.turn}</span>
            <span className="model-type">{gameSession.model_type}</span>
          </div>
        </div>
        
        <div className="game-actions">
          <button className="action-btn secondary" onClick={handleBackToMenu}>
            Меню
          </button>
          <button className="action-btn primary" onClick={handleNewGame}>
            Новая игра
          </button>
        </div>
      </div>

      {/* Панель вкладок */}
      <div className="game-tabs">
        <button 
          className={`tab-btn ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveTab('dashboard')}
        >
          📊 Дашборд
        </button>
        <button 
          className={`tab-btn ${activeTab === 'chart' ? 'active' : ''}`}
          onClick={() => setActiveTab('chart')}
        >
          📈 Графики
        </button>
        <button 
          className={`tab-btn ${activeTab === 'tips' ? 'active' : ''}`}
          onClick={() => setActiveTab('tips')}
        >
          💡 Советы
        </button>
      </div>

      {/* Основной контент */}
      <div className="game-content">
        {activeTab === 'dashboard' && (
          <EnhancedGameDashboard 
            gameId={parseInt(gameId!)}
            onNextTurn={handleNextTurn}
          />
        )}
        
        {activeTab === 'chart' && (
          <div className="chart-container">
            <GameChart 
              gameId={parseInt(gameId!)}
            />
          </div>
        )}
        
        {activeTab === 'tips' && (
          <div className="tips-container">
            <GameTips modelType="enhanced" />
          </div>
        )}
      </div>

      {/* Информационная панель */}
      <div className="game-footer">
        <div className="footer-info">
          <p>
            <strong>Расширенная модель</strong> включает двухсекторную экономику, 
            валютный курс, внешнюю торговлю и систему кризисов.
          </p>
        </div>
        <div className="footer-help">
          <p>💡 Используйте вкладки для переключения между режимами просмотра</p>
        </div>
      </div>
    </div>
  );
};

export default EnhancedGamePage; 