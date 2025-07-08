import React, { useState, useEffect } from 'react';
import { GameSession, EconomicIndicators, BudgetData } from '../types/game';
import './EnhancedGameDashboard.css';

interface EnhancedGameDashboardProps {
  gameId: number;
  onNextTurn: (parameters: any) => void;
}

interface EnhancedIndicators extends EconomicIndicators {
  industry_output: number;
  services_output: number;
  exchange_rate: number;
  external_debt: number;
  population: number;
  interest_rate: number;
}

interface EnhancedBudgetData extends BudgetData {
  gold_reserves: number;
  external_debt: number;
}

interface CrisisInfo {
  type: string;
  description: string;
  effects: any;
}

interface EnhancedGameData {
  id: number;
  turn: number;
  indicators: EnhancedIndicators;
  budget: EnhancedBudgetData;
  crisis?: CrisisInfo;
  model_type: string;
}

const EnhancedGameDashboard: React.FC<EnhancedGameDashboardProps> = ({ gameId, onNextTurn }) => {
  const [gameData, setGameData] = useState<EnhancedGameData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCrisis, setShowCrisis] = useState(false);

  // Параметры управления
  const [parameters, setParameters] = useState({
    interest_rate: 5.0,
    tax_rate: 20.0,
    government_spending: 25.0,
    customs_duty: 5.0,
    education_priority: 20.0,
    healthcare_priority: 20.0,
    defense_priority: 20.0,
    infrastructure_priority: 20.0,
    social_priority: 20.0,
    social_transfers: 0.0,
    reserve_ratio: 0.1,
    refinance_rate: 0.05,
    printing_press_active: false
  });

  useEffect(() => {
    loadGameState();
  }, [gameId]);

  const loadGameState = async () => {
    try {
      setLoading(true);
      const response = await fetch(`/api/game/enhanced/${gameId}/enhanced_state/`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setGameData(data.game);
        
        // Показываем кризис, если он есть
        if (data.game.crisis) {
          setShowCrisis(true);
        }
      } else {
        setError('Ошибка загрузки состояния игры');
      }
    } catch (err) {
      setError('Ошибка подключения к серверу');
    } finally {
      setLoading(false);
    }
  };

  const handleNextTurn = async () => {
    try {
      setLoading(true);
      const response = await fetch(`/api/game/enhanced/${gameId}/next_enhanced_turn/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({ parameters })
      });

      if (response.ok) {
        const data = await response.json();
        setGameData(data.game);
        
        // Показываем кризис, если он произошел
        if (data.game.crisis) {
          setShowCrisis(true);
        }
        
        onNextTurn(parameters);
      } else {
        setError('Ошибка выполнения хода');
      }
    } catch (err) {
      setError('Ошибка подключения к серверу');
    } finally {
      setLoading(false);
    }
  };

  const handleParameterChange = (name: string, value: number | boolean) => {
    setParameters(prev => ({
      ...prev,
      [name]: value
    }));
  };

  if (loading) {
    return <div className="enhanced-dashboard loading">Загрузка...</div>;
  }

  if (error) {
    return <div className="enhanced-dashboard error">Ошибка: {error}</div>;
  }

  if (!gameData) {
    return <div className="enhanced-dashboard error">Данные игры не найдены</div>;
  }

  const { indicators, budget, crisis } = gameData;

  return (
    <div className="enhanced-dashboard">
      <div className="dashboard-header">
        <h2>Расширенная экономическая модель</h2>
        <div className="turn-info">
          <span>Ход: {gameData.turn}</span>
          <span>Тип модели: {gameData.model_type}</span>
        </div>
      </div>

      {/* Кризисное уведомление */}
      {crisis && showCrisis && (
        <div className="crisis-alert">
          <div className="crisis-header">
            <h3>🚨 Кризис: {crisis.type}</h3>
            <button onClick={() => setShowCrisis(false)}>✕</button>
          </div>
          <p>{crisis.description}</p>
          <div className="crisis-effects">
            <h4>Эффекты:</h4>
            <ul>
              {Object.entries(crisis.effects).map(([key, value]) => (
                <li key={key}>
                  <span>{key}: {String(value)}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      <div className="dashboard-grid">
        {/* Основные экономические показатели */}
        <div className="dashboard-section main-indicators">
          <h3>Основные показатели</h3>
          <div className="indicators-grid">
            <div className="indicator">
              <label>ВВП (общий)</label>
              <span className="value">{indicators.gdp_absolute.toFixed(2)} млн $</span>
              <span className={`change ${indicators.gdp_growth >= 0 ? 'positive' : 'negative'}`}>
                {indicators.gdp_growth >= 0 ? '+' : ''}{indicators.gdp_growth.toFixed(2)}%
              </span>
            </div>
            
            <div className="indicator">
              <label>Промышленность</label>
              <span className="value">{indicators.industry_output.toFixed(2)} млн $</span>
              <span className="share">({((indicators.industry_output / indicators.gdp_absolute) * 100).toFixed(1)}%)</span>
            </div>
            
            <div className="indicator">
              <label>Услуги</label>
              <span className="value">{indicators.services_output.toFixed(2)} млн $</span>
              <span className="share">({((indicators.services_output / indicators.gdp_absolute) * 100).toFixed(1)}%)</span>
            </div>
            
            <div className="indicator">
              <label>Инфляция</label>
              <span className={`value ${indicators.inflation > 5 ? 'negative' : 'positive'}`}>
                {indicators.inflation.toFixed(2)}%
              </span>
            </div>
            
            <div className="indicator">
              <label>Безработица</label>
              <span className={`value ${indicators.unemployment > 8 ? 'negative' : 'positive'}`}>
                {indicators.unemployment.toFixed(2)}%
              </span>
            </div>
            
            <div className="indicator">
              <label>Рейтинг президента</label>
              <span className={`value ${indicators.president_rating > 50 ? 'positive' : 'negative'}`}>
                {indicators.president_rating.toFixed(1)}%
              </span>
            </div>
          </div>
        </div>

        {/* Финансовые показатели */}
        <div className="dashboard-section financial">
          <h3>Финансовая система</h3>
          <div className="indicators-grid">
            <div className="indicator">
              <label>Ключевая ставка</label>
              <span className="value">{indicators.interest_rate.toFixed(2)}%</span>
            </div>
            
            <div className="indicator">
              <label>Обменный курс</label>
              <span className="value">{indicators.exchange_rate.toFixed(3)}</span>
            </div>
            
            <div className="indicator">
              <label>Денежная масса</label>
              <span className="value">{indicators.money_supply.toFixed(2)} млн $</span>
            </div>
            
            <div className="indicator">
              <label>Золотой запас</label>
              <span className="value">{indicators.gold_reserves.toFixed(2)} млн $</span>
            </div>
            
            <div className="indicator">
              <label>Внешний долг</label>
              <span className={`value ${indicators.external_debt > 0 ? 'negative' : 'positive'}`}>
                {indicators.external_debt.toFixed(2)} млн $
              </span>
            </div>
            
            <div className="indicator">
              <label>Население</label>
              <span className="value">{indicators.population.toFixed(2)} млн чел.</span>
            </div>
          </div>
        </div>

        {/* Бюджетные показатели */}
        <div className="dashboard-section budget">
          <h3>Бюджет</h3>
          <div className="indicators-grid">
            <div className="indicator">
              <label>Доходы</label>
              <span className="value positive">{budget.total_revenue.toFixed(2)} млн $</span>
            </div>
            
            <div className="indicator">
              <label>Расходы</label>
              <span className="value negative">{budget.total_spending.toFixed(2)} млн $</span>
            </div>
            
            <div className="indicator">
              <label>Баланс</label>
              <span className={`value ${budget.budget_balance >= 0 ? 'positive' : 'negative'}`}>
                {budget.budget_balance >= 0 ? '+' : ''}{budget.budget_balance.toFixed(2)} млн $
              </span>
            </div>
            
            <div className="indicator">
              <label>Соц. трансферты</label>
              <span className="value">{(budget.social_transfers || 0).toFixed(2)} млн $</span>
            </div>
            
            <div className="indicator">
              <label>Накопления</label>
              <span className="value">{budget.accumulated_reserves.toFixed(2)} млн $</span>
            </div>
          </div>
        </div>

        {/* Параметры управления */}
        <div className="dashboard-section controls">
          <h3>Параметры управления</h3>
          <div className="controls-grid">
            <div className="control-group">
              <label>Ключевая ставка (%)</label>
              <input
                type="range"
                min="0"
                max="20"
                step="0.5"
                value={parameters.interest_rate}
                onChange={(e) => handleParameterChange('interest_rate', parseFloat(e.target.value))}
              />
              <span className="control-value">{parameters.interest_rate}%</span>
            </div>

            <div className="control-group">
              <label>Налоговая ставка (%)</label>
              <input
                type="range"
                min="0"
                max="50"
                step="1"
                value={parameters.tax_rate}
                onChange={(e) => handleParameterChange('tax_rate', parseFloat(e.target.value))}
              />
              <span className="control-value">{parameters.tax_rate}%</span>
            </div>

            <div className="control-group">
              <label>Гос. расходы (%)</label>
              <input
                type="range"
                min="10"
                max="50"
                step="1"
                value={parameters.government_spending}
                onChange={(e) => handleParameterChange('government_spending', parseFloat(e.target.value))}
              />
              <span className="control-value">{parameters.government_spending}%</span>
            </div>

            <div className="control-group">
              <label>Соц. трансферты (млн $)</label>
              <input
                type="range"
                min="0"
                max="200"
                step="10"
                value={parameters.social_transfers}
                onChange={(e) => handleParameterChange('social_transfers', parseFloat(e.target.value))}
              />
              <span className="control-value">{parameters.social_transfers} млн $</span>
            </div>

            <div className="control-group">
              <label>
                <input
                  type="checkbox"
                  checked={parameters.printing_press_active}
                  onChange={(e) => handleParameterChange('printing_press_active', e.target.checked)}
                />
                Печатный станок
              </label>
            </div>
          </div>

          <button 
            className="next-turn-btn"
            onClick={handleNextTurn}
            disabled={loading}
          >
            {loading ? 'Выполняется...' : 'Следующий ход'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default EnhancedGameDashboard; 