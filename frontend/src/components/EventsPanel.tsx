import React from 'react';
import { GameEvent } from '../types/game';
import './EventsPanel.css';

interface EventsPanelProps {
  events?: GameEvent[];
}

const EventsPanel: React.FC<EventsPanelProps> = ({ events }) => {
  const safeEvents = Array.isArray(events) ? events : [];

  const getEventIcon = (eventType: string) => {
    switch (eventType) {
      case 'natural_disaster':
        return '🌪️';
      case 'economic_crisis':
        return '📉';
      case 'sanctions':
        return '🚫';
      case 'international_conflict':
        return '⚔️';
      case 'commodity_price_change':
        return '💰';
      case 'social_protest':
        return '📢';
      default:
        return '📰';
    }
  };

  const getImpactText = (impact: number, type: string) => {
    if (impact === 0) return '';
    
    const sign = impact > 0 ? '+' : '';
    const value = Math.abs(impact);
    
    switch (type) {
      case 'gdp_impact':
        return `ВВП: ${sign}${value.toFixed(1)}%`;
      case 'inflation_impact':
        return `Инфляция: ${sign}${value.toFixed(1)}%`;
      case 'unemployment_impact':
        return `Безработица: ${sign}${value.toFixed(1)}%`;
      case 'rating_impact':
        return `Рейтинг: ${sign}${value.toFixed(1)}%`;
      default:
        return '';
    }
  };

  return (
    <div className="events-panel">
      <h3>События</h3>
      
      {safeEvents.length === 0 ? (
        <div className="no-events">
          <p>Событий нет</p>
        </div>
      ) : (
        <div className="events-list">
          {safeEvents.map((event, index) => (
            <div key={index} className="event-card">
              <div className="event-header">
                <span className="event-icon">{getEventIcon(event.event_type)}</span>
                <h4 className="event-title">{event.title}</h4>
              </div>
              
              <p className="event-description">{event.description}</p>
              
              <div className="event-impacts">
                {getImpactText(event.gdp_impact, 'gdp_impact') && (
                  <span className="impact-item">{getImpactText(event.gdp_impact, 'gdp_impact')}</span>
                )}
                {getImpactText(event.inflation_impact, 'inflation_impact') && (
                  <span className="impact-item">{getImpactText(event.inflation_impact, 'inflation_impact')}</span>
                )}
                {getImpactText(event.unemployment_impact, 'unemployment_impact') && (
                  <span className="impact-item">{getImpactText(event.unemployment_impact, 'unemployment_impact')}</span>
                )}
                {getImpactText(event.rating_impact, 'rating_impact') && (
                  <span className="impact-item">{getImpactText(event.rating_impact, 'rating_impact')}</span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default EventsPanel; 