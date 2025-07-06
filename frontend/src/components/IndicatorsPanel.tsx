import React from 'react';
import { EconomicIndicators } from '../types/game';
import './IndicatorsPanel.css';

interface IndicatorsPanelProps {
  indicators: EconomicIndicators;
}

const IndicatorsPanel: React.FC<IndicatorsPanelProps> = ({ indicators }) => {
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
      </div>
    </div>
  );
};

export default IndicatorsPanel; 