import React from 'react';
import { EconomicIndicators } from '../types/game';
import { BudgetData } from '../types/game';
import './IndicatorsPanel.css';

interface IndicatorsPanelProps {
  indicators: EconomicIndicators;
  budget?: BudgetData | null;
}

const IndicatorsPanel: React.FC<IndicatorsPanelProps> = ({ indicators, budget }) => {
  const getRatingColor = (rating: number) => {
    if (rating >= 70) return 'excellent';
    if (rating >= 50) return 'good';
    if (rating >= 30) return 'warning';
    return 'danger';
  };

  const getIndicatorColor = (value: number, type: 'positive' | 'negative' | 'neutral') => {
    if (type === 'positive') {
      return value > 0 ? 'positive' : 'negative';
    }
    if (type === 'negative') {
      return value < 0 ? 'positive' : 'negative';
    }
    return 'neutral';
  };

  return (
    <div className="indicators-panel">
      <h3>Экономические показатели</h3>
      
      <div className="indicators-grid">
        <div className="indicator-card main">
          <h4>Рейтинг президента</h4>
          <div className={`indicator-value ${getRatingColor(indicators.president_rating)}`}>
            {indicators.president_rating.toFixed(1)}%
          </div>
          <small>Поддержка населения</small>
        </div>

        <div className="indicator-card">
          <h4>Рост ВВП</h4>
          <div className={`indicator-value ${getIndicatorColor(indicators.gdp_growth, 'positive')}`}>
            {indicators.gdp_growth > 0 ? '+' : ''}{indicators.gdp_growth.toFixed(2)}%
          </div>
          <small>Темп роста экономики</small>
        </div>

        <div className="indicator-card">
          <h4>Инфляция</h4>
          <div className={`indicator-value ${getIndicatorColor(indicators.inflation, 'negative')}`}>
            {indicators.inflation.toFixed(2)}%
          </div>
          <small>Рост цен</small>
        </div>

        <div className="indicator-card">
          <h4>Безработица</h4>
          <div className={`indicator-value ${getIndicatorColor(indicators.unemployment, 'negative')}`}>
            {indicators.unemployment.toFixed(2)}%
          </div>
          <small>Уровень безработицы</small>
        </div>

        <div className="indicator-card">
          <h4>Инвестиции</h4>
          <div className="indicator-value neutral">
            {indicators.investments.toFixed(2)}%
          </div>
          <small>% от ВВП</small>
        </div>

        <div className="indicator-card">
          <h4>Настроение</h4>
          <div className={`indicator-value ${getRatingColor(indicators.public_mood)}`}>
            {indicators.public_mood.toFixed(1)}%
          </div>
          <small>Настроение населения</small>
        </div>

        <div className="indicator-card">
          <h4>Экспорт</h4>
          <div className="indicator-value neutral">
            {indicators.export_volume.toFixed(2)}%
          </div>
          <small>Объем экспорта</small>
        </div>

        <div className="indicator-card">
          <h4>Импорт</h4>
          <div className="indicator-value neutral">
            {indicators.import_volume.toFixed(2)}%
          </div>
          <small>Объем импорта</small>
        </div>

        <div className="indicator-card">
          <h4>Численность населения</h4>
          <div className="indicator-value neutral">
            {(indicators.population ?? 0).toLocaleString()} чел.
          </div>
          <small>Всего жителей</small>
        </div>
      </div>
      {budget && (
        <div className="budget-panel">
          <h4>Бюджет (млн $)</h4>
          <div className="budget-grid">
            <div className="budget-item">
              <span className="budget-label">Доходы:</span>
              <span className="budget-value">{(budget?.total_revenue ?? 0).toLocaleString()} млн $</span>
            </div>
            <div className="budget-item">
              <span className="budget-label">Расходы:</span>
              <span className="budget-value">{(budget?.total_spending ?? 0).toLocaleString()} млн $</span>
            </div>
            <div className="budget-item">
              <span className="budget-label">Баланс:</span>
              <span className="budget-value" style={{color: (budget?.budget_balance ?? 0) >= 0 ? '#4caf50' : '#e53935'}}>
                {(budget?.budget_balance ?? 0) >= 0 ? '+' : ''}{(budget?.budget_balance ?? 0).toLocaleString()} млн $
              </span>
            </div>
            <div className="budget-item">
              <span className="budget-label">Соц. трансферты:</span>
              <span className="budget-value">{(budget?.social_transfers ?? 0).toLocaleString()} млн $</span>
            </div>
          </div>
        </div>
      )}

      {/* Новые экономические параметры */}
      <div className="extra-indicators-panel">
        <h4>Банковская система и денежная масса</h4>
        <div className="extra-indicators-grid">
          <div className="extra-indicator-item">
            <span className="extra-label">Денежная масса:</span>
            <span className="extra-value">{(indicators.money_supply ?? 0).toLocaleString()} млн $</span>
          </div>
          <div className="extra-indicator-item">
            <span className="extra-label">Золотой запас:</span>
            <span className="extra-value">{(indicators.gold_reserves ?? 0).toLocaleString()} млн $</span>
          </div>
          <div className="extra-indicator-item">
            <span className="extra-label">Резервные требования:</span>
            <span className="extra-value">{((indicators.reserve_ratio ?? 0) * 100).toFixed(1)}%</span>
          </div>
          <div className="extra-indicator-item">
            <span className="extra-label">Ставка рефинансирования:</span>
            <span className="extra-value">{((indicators.refinance_rate ?? 0) * 100).toFixed(2)}%</span>
          </div>
          <div className="extra-indicator-item">
            <span className="extra-label">Печатный станок:</span>
            <span className="extra-value" style={{color: indicators.printing_press_active ? '#4caf50' : '#e53935'}}>
              {indicators.printing_press_active ? 'ВКЛ' : 'ВЫКЛ'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default IndicatorsPanel; 