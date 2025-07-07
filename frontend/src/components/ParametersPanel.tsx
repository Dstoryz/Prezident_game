import React, { useState } from 'react';
import { GameParameters } from '../types/game';
import './ParametersPanel.css';

interface ParametersPanelProps {
  parameters: GameParameters;
  onNextTurn: (parameters: Partial<GameParameters>) => void;
  loading: boolean;
}

const ParametersPanel: React.FC<ParametersPanelProps> = ({ 
  parameters, 
  onNextTurn, 
  loading 
}) => {
  const [localParameters, setLocalParameters] = useState<GameParameters>({
    ...parameters,
    social_transfers: parameters.social_transfers ?? 0,
  });

  const handleParameterChange = (key: keyof GameParameters, value: number) => {
    setLocalParameters(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleNextTurn = () => {
    onNextTurn(localParameters);
  };

  const resetToDefaults = () => {
    setLocalParameters({
      interest_rate: 5.0,
      tax_rate: 20.0,
      government_spending: 25.0,
      customs_duty: 5.0,
      social_transfers: 0,
    });
  };

  return (
    <div className="parameters-panel">
      <h3>Параметры управления</h3>
      
      <div className="parameter-group">
        <label>
          Процентная ставка: {localParameters.interest_rate}%
          <input
            type="range"
            min="0"
            max="20"
            step="0.5"
            value={localParameters.interest_rate}
            onChange={(e) => handleParameterChange('interest_rate', parseFloat(e.target.value))}
            disabled={loading}
          />
        </label>
        <small>Высокая ставка снижает инфляцию, но увеличивает безработицу</small>
      </div>

      <div className="parameter-group">
        <label>
          Налоговая нагрузка: {localParameters.tax_rate}%
          <input
            type="range"
            min="0"
            max="50"
            step="1"
            value={localParameters.tax_rate}
            onChange={(e) => handleParameterChange('tax_rate', parseFloat(e.target.value))}
            disabled={loading}
          />
        </label>
        <small>Высокие налоги снижают инвестиции и настроение населения</small>
      </div>

      <div className="parameter-group">
        <label>
          Государственные расходы: {localParameters.government_spending}%
          <input
            type="range"
            min="10"
            max="50"
            step="1"
            value={localParameters.government_spending}
            onChange={(e) => handleParameterChange('government_spending', parseFloat(e.target.value))}
            disabled={loading}
          />
        </label>
        <small>Расходы стимулируют рост ВВП, но могут вызвать инфляцию</small>
      </div>

      <div className="parameter-group">
        <label>
          Таможенные пошлины: {localParameters.customs_duty}%
          <input
            type="range"
            min="0"
            max="20"
            step="0.5"
            value={localParameters.customs_duty}
            onChange={(e) => handleParameterChange('customs_duty', parseFloat(e.target.value))}
            disabled={loading}
          />
        </label>
        <small>Пошлины влияют на внешнюю торговлю</small>
      </div>

      <div className="parameter-group">
        <label>
          Социальные трансферты: {localParameters.social_transfers} млн $
          <input
            type="range"
            min="0"
            max="1000"
            step="10"
            value={localParameters.social_transfers}
            onChange={(e) => handleParameterChange('social_transfers', parseFloat(e.target.value))}
            disabled={loading}
          />
        </label>
        <small>Выплаты населению, поддерживают спрос и настроение, но увеличивают расходы бюджета</small>
      </div>

      <div className="parameter-actions">
        <button 
          onClick={handleNextTurn} 
          disabled={loading}
          className="next-turn-btn"
        >
          {loading ? 'Обработка...' : 'Следующий ход'}
        </button>
        
        <button 
          onClick={resetToDefaults} 
          disabled={loading}
          className="reset-btn"
        >
          Сбросить
        </button>
      </div>
    </div>
  );
};

export default ParametersPanel; 