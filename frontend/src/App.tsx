import React, { useState } from 'react';
import './App.css';
import CreateGameForm from './components/CreateGameForm';

interface GameData {
  game_id: number;
  player_name: string;
  difficulty: string;
  status: string;
  economic_indicators: any;
  budget_data: any;
  message: string;
}

function App() {
  const [gameData, setGameData] = useState<GameData | null>(null);
  const [showGameForm, setShowGameForm] = useState(true);

  const handleGameCreated = (data: GameData) => {
    setGameData(data);
    setShowGameForm(false);
  };

  const handleNewGame = () => {
    setGameData(null);
    setShowGameForm(true);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎮 Президент: Экономика и Власть</h1>
        <p>Стратегическая игра управления экономикой</p>
      </header>

      <main className="App-main">
        {showGameForm ? (
          <CreateGameForm onGameCreated={handleGameCreated} />
        ) : (
          <div className="game-status">
            <h2>🎉 Игра создана успешно!</h2>
            <div className="game-info">
              <p><strong>Игрок:</strong> {gameData?.player_name}</p>
              <p><strong>Сложность:</strong> {gameData?.difficulty}</p>
              <p><strong>ID игры:</strong> {gameData?.game_id}</p>
              <p><strong>Статус:</strong> {gameData?.status}</p>
            </div>
            
            {gameData?.economic_indicators && (
              <div className="economic-data">
                <h3>📊 Экономические показатели:</h3>
                <div className="indicators-grid">
                  <div className="indicator">
                    <span>ВВП:</span>
                    <span>${gameData.economic_indicators.gdp?.toLocaleString()}</span>
                  </div>
                  <div className="indicator">
                    <span>Рост ВВП:</span>
                    <span>{gameData.economic_indicators.gdp_growth}%</span>
                  </div>
                  <div className="indicator">
                    <span>Инфляция:</span>
                    <span>{gameData.economic_indicators.inflation}%</span>
                  </div>
                  <div className="indicator">
                    <span>Безработица:</span>
                    <span>{gameData.economic_indicators.unemployment}%</span>
                  </div>
                </div>
              </div>
            )}
            
            <button onClick={handleNewGame} className="new-game-button">
              🎮 Создать новую игру
            </button>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
