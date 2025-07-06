import React, { useState } from 'react';
import { GameEvent, EconomicIndicators } from '../types/game';
import './GameTips.css';

interface GameTipsProps {
  currentEvent?: GameEvent;
  indicators?: EconomicIndicators;
  parameters: {
    interest_rate: number;
    tax_rate: number;
    government_spending: number;
    customs_duty: number;
  };
}

const GameTips: React.FC<GameTipsProps> = ({ currentEvent, indicators, parameters }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const getEventExplanation = (event: GameEvent) => {
    const explanations: { [key: string]: string } = {
      'economic_crisis': 'Экономический кризис снижает доверие инвесторов и потребителей. Необходимо принимать меры для стабилизации экономики.',
      'oil_price_shock': 'Резкое изменение цен на нефть влияет на экспорт и инфляцию. Нужно адаптировать экономическую политику.',
      'natural_disaster': 'Природная катастрофа требует дополнительных расходов на восстановление и может временно снизить экономическую активность.',
      'political_scandal': 'Политический скандал снижает рейтинг президента и доверие к правительству.',
      'trade_war': 'Торговая война влияет на экспорт/импорт и может потребовать изменения таможенной политики.',
      'inflation_spike': 'Рост инфляции снижает покупательную способность населения и требует монетарных мер.',
      'recession': 'Рецессия характеризуется снижением экономической активности и требует стимулирующих мер.',
      'boom': 'Экономический бум может привести к перегреву экономики и требует сдерживающих мер.',
      'election_year': 'Год выборов требует особого внимания к социальным программам и рейтингу.',
      'corruption_case': 'Дело о коррупции подрывает доверие к власти и требует прозрачности.',
    };

    return explanations[event.event_type] || 'Это событие влияет на экономическую ситуацию в стране.';
  };

  const getEconomicAnalysis = () => {
    if (!indicators) return null;

    const analysis = [];

    // Анализ ВВП
    if (indicators.gdp_growth > 3) {
      analysis.push('✅ Экономика растет высокими темпами');
    } else if (indicators.gdp_growth > 0) {
      analysis.push('📈 Экономика растет умеренно');
    } else {
      analysis.push('⚠️ Экономика в рецессии');
    }

    // Анализ инфляции
    if (indicators.inflation > 8) {
      analysis.push('🔥 Высокая инфляция требует срочных мер');
    } else if (indicators.inflation > 4) {
      analysis.push('📊 Умеренная инфляция в пределах нормы');
    } else {
      analysis.push('❄️ Низкая инфляция, возможен риск дефляции');
    }

    // Анализ безработицы
    if (indicators.unemployment > 8) {
      analysis.push('👥 Высокая безработица требует стимулирования занятости');
    } else if (indicators.unemployment > 5) {
      analysis.push('📋 Безработица на умеренном уровне');
    } else {
      analysis.push('🎯 Низкая безработица - хороший показатель');
    }

    // Анализ рейтинга
    if (indicators.president_rating > 70) {
      analysis.push('👑 Высокий рейтинг президента');
    } else if (indicators.president_rating > 50) {
      analysis.push('📊 Средний рейтинг президента');
    } else {
      analysis.push('⚠️ Низкий рейтинг президента требует действий');
    }

    return analysis;
  };

  const getRecommendations = () => {
    if (!indicators) return [];

    const recommendations = [];

    // Рекомендации по процентной ставке
    if (indicators.inflation > 6) {
      recommendations.push('💡 Рекомендуется повысить процентную ставку для борьбы с инфляцией');
    } else if (indicators.gdp_growth < 0) {
      recommendations.push('💡 Рекомендуется снизить процентную ставку для стимулирования экономики');
    }

    // Рекомендации по налогам
    if (indicators.unemployment > 7) {
      recommendations.push('💡 Снижение налогов может стимулировать занятость');
    } else if (parameters.government_spending > 30) {
      recommendations.push('💡 Повышение налогов может снизить дефицит бюджета');
    }

    // Рекомендации по госрасходам
    if (indicators.gdp_growth < 1) {
      recommendations.push('💡 Увеличение госрасходов может стимулировать экономический рост');
    } else if (indicators.inflation > 5) {
      recommendations.push('💡 Снижение госрасходов может помочь контролировать инфляцию');
    }

    // Рекомендации по таможенным пошлинам
    if (indicators.import_volume > indicators.export_volume * 1.5) {
      recommendations.push('💡 Повышение таможенных пошлин может улучшить торговый баланс');
    } else if (indicators.export_volume < indicators.import_volume * 0.7) {
      recommendations.push('💡 Снижение таможенных пошлин может стимулировать экспорт');
    }

    return recommendations;
  };

  const getParameterTips = () => {
    return [
      {
        name: 'Процентная ставка',
        current: parameters.interest_rate,
        description: 'Влияет на кредитование и инфляцию. Высокая ставка сдерживает инфляцию, но замедляет рост.',
        range: '2-15%'
      },
      {
        name: 'Налоговая ставка',
        current: parameters.tax_rate,
        description: 'Влияет на доходы бюджета и экономическую активность. Высокие налоги снижают стимулы к работе.',
        range: '10-50%'
      },
      {
        name: 'Госрасходы',
        current: parameters.government_spending,
        description: 'Влияет на экономический рост и дефицит бюджета. Высокие расходы стимулируют экономику.',
        range: '15-40%'
      },
      {
        name: 'Таможенные пошлины',
        current: parameters.customs_duty,
        description: 'Влияет на торговый баланс и цены на импорт. Высокие пошлины защищают местных производителей.',
        range: '0-25%'
      }
    ];
  };

  return (
    <div className="game-tips">
      <div className="tips-header" onClick={() => setIsExpanded(!isExpanded)}>
        <h3>💡 Подсказки и рекомендации</h3>
        <span className="expand-icon">{isExpanded ? '▼' : '▶'}</span>
      </div>

      {isExpanded && (
        <div className="tips-content">
          {/* Текущее событие */}
          {currentEvent && (
            <div className="tip-section">
              <h4>🎯 Текущее событие: {currentEvent.title}</h4>
              <p className="event-description">{currentEvent.description}</p>
              <div className="event-explanation">
                <strong>Объяснение:</strong> {getEventExplanation(currentEvent)}
              </div>
              <div className="event-impacts">
                <strong>Воздействие:</strong>
                <ul>
                  {currentEvent.gdp_impact !== 0 && (
                    <li>ВВП: {currentEvent.gdp_impact > 0 ? '+' : ''}{currentEvent.gdp_impact}%</li>
                  )}
                  {currentEvent.inflation_impact !== 0 && (
                    <li>Инфляция: {currentEvent.inflation_impact > 0 ? '+' : ''}{currentEvent.inflation_impact}%</li>
                  )}
                  {currentEvent.unemployment_impact !== 0 && (
                    <li>Безработица: {currentEvent.unemployment_impact > 0 ? '+' : ''}{currentEvent.unemployment_impact}%</li>
                  )}
                  {currentEvent.rating_impact !== 0 && (
                    <li>Рейтинг: {currentEvent.rating_impact > 0 ? '+' : ''}{currentEvent.rating_impact}%</li>
                  )}
                </ul>
              </div>
            </div>
          )}

          {/* Анализ экономики */}
          {indicators && (
            <div className="tip-section">
              <h4>📊 Анализ экономической ситуации</h4>
              <div className="economic-analysis">
                {getEconomicAnalysis()?.map((item, index) => (
                  <div key={index} className="analysis-item">{item}</div>
                ))}
              </div>
            </div>
          )}

          {/* Рекомендации */}
          {indicators && (
            <div className="tip-section">
              <h4>🎯 Рекомендации по управлению</h4>
              <div className="recommendations">
                {getRecommendations().map((rec, index) => (
                  <div key={index} className="recommendation-item">{rec}</div>
                ))}
                {getRecommendations().length === 0 && (
                  <div className="no-recommendations">
                    Экономическая ситуация стабильна. Продолжайте текущую политику.
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Подсказки по параметрам */}
          <div className="tip-section">
            <h4>⚙️ Подсказки по параметрам управления</h4>
            <div className="parameter-tips">
              {getParameterTips().map((tip, index) => (
                <div key={index} className="parameter-tip">
                  <div className="parameter-header">
                    <span className="parameter-name">{tip.name}</span>
                    <span className="parameter-current">{tip.current}%</span>
                  </div>
                  <p className="parameter-description">{tip.description}</p>
                  <div className="parameter-range">Диапазон: {tip.range}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Общие советы */}
          <div className="tip-section">
            <h4>💭 Общие советы</h4>
            <div className="general-tips">
              <ul>
                <li>Балансируйте между экономическим ростом и стабильностью</li>
                <li>Следите за рейтингом президента - он влияет на исход выборов</li>
                <li>Адаптируйте политику к текущим событиям</li>
                <li>Не делайте резких изменений - экономика реагирует постепенно</li>
                <li>Учитывайте взаимосвязь между параметрами</li>
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default GameTips; 