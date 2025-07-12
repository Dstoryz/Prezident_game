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
    education_priority: parameters.education_priority ?? 20.0,
    healthcare_priority: parameters.healthcare_priority ?? 20.0,
    defense_priority: parameters.defense_priority ?? 20.0,
    infrastructure_priority: parameters.infrastructure_priority ?? 20.0,
    social_priority: parameters.social_priority ?? 20.0,
    reserve_ratio: parameters.reserve_ratio ?? 0.1,
    refinance_rate: parameters.refinance_rate ?? 0.05,
    printing_press_active: parameters.printing_press_active ?? false,
  });

  // Состояние для сворачивания секций
  const [expandedSections, setExpandedSections] = useState({
    main: true,
    budget: false,
    monetary: false
  });

  const handleParameterChange = (key: keyof GameParameters, value: number | boolean) => {
    setLocalParameters(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleNextTurn = () => {
    console.log('ParametersPanel: отправляем параметры на следующий ход:', localParameters);
    onNextTurn(localParameters);
  };

  const resetToDefaults = () => {
    setLocalParameters({
      interest_rate: 5.0,
      tax_rate: 20.0,
      government_spending: 25.0,
      customs_duty: 5.0,
      education_priority: 20.0,
      healthcare_priority: 20.0,
      defense_priority: 20.0,
      infrastructure_priority: 20.0,
      social_priority: 20.0,
      social_transfers: 0,
      reserve_ratio: 0.1,
      refinance_rate: 0.05,
      printing_press_active: false,
    });
  };

  const toggleSection = (section: keyof typeof expandedSections) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  // Проверяем сумму бюджетных приоритетов
  const totalPriority = localParameters.education_priority + 
                       localParameters.healthcare_priority + 
                       localParameters.defense_priority + 
                       localParameters.infrastructure_priority + 
                       localParameters.social_priority;

  const isPriorityValid = totalPriority <= 100;

  return (
    <div className="parameters-panel">
      <h3>Параметры управления</h3>
      
      {/* Основные экономические параметры */}
      <div className="parameter-section">
        <div 
          className="section-header"
          onClick={() => toggleSection('main')}
        >
          <h4>🎯 Основные параметры</h4>
          <span className={`expand-icon ${expandedSections.main ? 'expanded' : ''}`}>
            ▼
          </span>
        </div>
        
        {expandedSections.main && (
          <div className="section-content">
            <div className="parameter-group">
              <label>
                Ключевая ставка: {localParameters.interest_rate}%
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
              <small>Выплаты населению, поддерживают спрос и настроение</small>
            </div>
          </div>
        )}
      </div>

      {/* Бюджетные приоритеты */}
      <div className="parameter-section">
        <div 
          className="section-header"
          onClick={() => toggleSection('budget')}
        >
          <h4>💰 Бюджетные приоритеты (сумма: {totalPriority.toFixed(1)}%)</h4>
          <span className={`expand-icon ${expandedSections.budget ? 'expanded' : ''}`}>
            ▼
          </span>
        </div>
        
        {expandedSections.budget && (
          <div className="section-content">
            {!isPriorityValid && (
              <div className="priority-warning">
                ⚠️ Сумма приоритетов превышает 100%!
              </div>
            )}
            
            <div className="parameter-group">
              <label>
                Образование и наука: {localParameters.education_priority}%
                <input
                  type="range"
                  min="0"
                  max="40"
                  step="1"
                  value={localParameters.education_priority}
                  onChange={(e) => handleParameterChange('education_priority', parseFloat(e.target.value))}
                  disabled={loading}
                />
              </label>
              <small>Влияет на технологический прогресс и качество рабочей силы</small>
            </div>

            <div className="parameter-group">
              <label>
                Здравоохранение: {localParameters.healthcare_priority}%
                <input
                  type="range"
                  min="0"
                  max="40"
                  step="1"
                  value={localParameters.healthcare_priority}
                  onChange={(e) => handleParameterChange('healthcare_priority', parseFloat(e.target.value))}
                  disabled={loading}
                />
              </label>
              <small>Влияет на продолжительность жизни и демографию</small>
            </div>

            <div className="parameter-group">
              <label>
                Оборона: {localParameters.defense_priority}%
                <input
                  type="range"
                  min="0"
                  max="40"
                  step="1"
                  value={localParameters.defense_priority}
                  onChange={(e) => handleParameterChange('defense_priority', parseFloat(e.target.value))}
                  disabled={loading}
                />
              </label>
              <small>Влияет на безопасность и международные отношения</small>
            </div>

            <div className="parameter-group">
              <label>
                Инфраструктура: {localParameters.infrastructure_priority}%
                <input
                  type="range"
                  min="0"
                  max="40"
                  step="1"
                  value={localParameters.infrastructure_priority}
                  onChange={(e) => handleParameterChange('infrastructure_priority', parseFloat(e.target.value))}
                  disabled={loading}
                />
              </label>
              <small>Влияет на производительность и экономический рост</small>
            </div>

            <div className="parameter-group">
              <label>
                Социальная защита: {localParameters.social_priority}%
                <input
                  type="range"
                  min="0"
                  max="40"
                  step="1"
                  value={localParameters.social_priority}
                  onChange={(e) => handleParameterChange('social_priority', parseFloat(e.target.value))}
                  disabled={loading}
                />
              </label>
              <small>Влияет на социальную стабильность и настроение населения</small>
            </div>
          </div>
        )}
      </div>

      {/* Монетарные параметры */}
      <div className="parameter-section">
        <div 
          className="section-header"
          onClick={() => toggleSection('monetary')}
        >
          <h4>🏦 Монетарная политика</h4>
          <span className={`expand-icon ${expandedSections.monetary ? 'expanded' : ''}`}>
            ▼
          </span>
        </div>
        
        {expandedSections.monetary && (
          <div className="section-content">
            <div className="parameter-group">
              <label>
                Резервные требования: {(localParameters.reserve_ratio * 100).toFixed(1)}%
                <input
                  type="range"
                  min="5"
                  max="20"
                  step="0.5"
                  value={localParameters.reserve_ratio * 100}
                  onChange={(e) => handleParameterChange('reserve_ratio', parseFloat(e.target.value) / 100)}
                  disabled={loading}
                />
              </label>
              <small>Влияет на денежную массу и кредитную активность</small>
            </div>

            <div className="parameter-group">
              <label>
                Ставка рефинансирования: {(localParameters.refinance_rate * 100).toFixed(2)}%
                <input
                  type="range"
                  min="1"
                  max="15"
                  step="0.1"
                  value={localParameters.refinance_rate * 100}
                  onChange={(e) => handleParameterChange('refinance_rate', parseFloat(e.target.value) / 100)}
                  disabled={loading}
                />
              </label>
              <small>Влияет на стоимость кредитов для банков</small>
            </div>

            <div className="parameter-group checkbox-group">
              <label>
                <input
                  type="checkbox"
                  checked={localParameters.printing_press_active}
                  onChange={(e) => handleParameterChange('printing_press_active', e.target.checked)}
                  disabled={loading}
                />
                Печатный станок (эмиссия денег)
              </label>
              <small>Включает эмиссию для покрытия дефицита бюджета (риск инфляции)</small>
            </div>
          </div>
        )}
      </div>

      <div className="parameter-actions">
        <button 
          onClick={handleNextTurn} 
          disabled={loading || !isPriorityValid}
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

      {!isPriorityValid && (
        <div className="error-message">
          ❌ Сумма бюджетных приоритетов не может превышать 100%
        </div>
      )}
    </div>
  );
};

export default ParametersPanel; 