import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import './CreateGameForm.css';

interface CreateGameFormProps {
  onGameCreated: (gameData: any) => void;
}

interface GameFormData {
  player_name: string;
  difficulty: 'easy' | 'medium' | 'hard';
  gdp: number;
  population: number;
  inflation: number;
  unemployment: number;
  budget_deficit: number;
}

const CreateGameForm: React.FC<CreateGameFormProps> = ({ onGameCreated }) => {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    player_name: '',
    difficulty: 'enhanced', // всегда расширенная модель
    gdp: 60000000000,
    population: 9400000,
    inflation: 6,
    unemployment: 4,
    budget_deficit: 0.0
  });
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'player_name' ? value : parseFloat(value)
    }));
  };

  const handleLogout = async () => {
    await logout();
    navigate('/auth');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/api/game/start/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const gameData = await response.json();
      onGameCreated(gameData);
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ошибка при создании игры');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="create-game-form">
      <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 16 }}>
        <button onClick={handleLogout} className="logout-btn" style={{ background: '#dc3545', color: 'white', border: 'none', borderRadius: 8, padding: '8px 18px', fontWeight: 600, cursor: 'pointer' }}>
          Выйти
        </button>
      </div>
      <h2>🎮 Создать новую игру</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="player_name">Имя игрока:</label>
          <input
            type="text"
            id="player_name"
            name="player_name"
            value={formData.player_name}
            onChange={handleInputChange}
            required
            placeholder="Введите ваше имя"
          />
        </div>

        {/* Удаляю/комментирую выпадающий список выбора сложности */}
        {/*
        <div className="form-group">
          <label htmlFor="difficulty">Сложность:</label>
          <select
            id="difficulty"
            name="difficulty"
            value={formData.difficulty}
            onChange={handleInputChange}
          >
            <option value="easy">Легкая</option>
            <option value="medium">Средняя</option>
            <option value="hard">Сложная</option>
          </select>
        </div>
        */}

        <div className="form-group">
          <label htmlFor="gdp">Начальный ВВП:</label>
          <input
            type="number"
            id="gdp"
            name="gdp"
            value={formData.gdp}
            onChange={handleInputChange}
            min="100000"
            step="100000"
          />
        </div>

        <div className="form-group">
          <label htmlFor="population">Население:</label>
          <input
            type="number"
            id="population"
            name="population"
            value={formData.population}
            onChange={handleInputChange}
            min="10000"
            step="10000"
          />
        </div>

        <div className="form-group">
          <label htmlFor="inflation">Инфляция (%):</label>
          <input
            type="number"
            id="inflation"
            name="inflation"
            value={formData.inflation}
            onChange={handleInputChange}
            min="0"
            max="50"
            step="0.1"
          />
        </div>

        <div className="form-group">
          <label htmlFor="unemployment">Безработица (%):</label>
          <input
            type="number"
            id="unemployment"
            name="unemployment"
            value={formData.unemployment}
            onChange={handleInputChange}
            min="0"
            max="30"
            step="0.1"
          />
        </div>

        <div className="form-group">
          <label htmlFor="budget_deficit">Дефицит бюджета (%):</label>
          <input
            type="number"
            id="budget_deficit"
            name="budget_deficit"
            value={formData.budget_deficit}
            onChange={handleInputChange}
            min="-10"
            max="20"
            step="0.1"
          />
        </div>

        {error && <div className="error-message">❌ {error}</div>}

        <button type="submit" disabled={loading} className="submit-button">
          {loading ? '🔄 Создание игры...' : '🚀 Начать игру'}
        </button>
      </form>
    </div>
  );
};

export default CreateGameForm;
