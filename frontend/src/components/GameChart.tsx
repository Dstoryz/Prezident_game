import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { gameApi } from '../services/api';
import { EconomicIndicators } from '../types/game';
import './GameChart.css';

interface GameChartProps {
  gameId: number;
  refreshTrigger?: number; // Добавляем триггер для обновления
}

interface ChartData {
  turn: number;
  gdp_growth: number;
  inflation: number;
  unemployment: number;
  president_rating: number;
}

const GameChart: React.FC<GameChartProps> = ({ gameId, refreshTrigger = 0 }) => {
  const [chartData, setChartData] = useState<ChartData[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadChartData();
  }, [gameId, refreshTrigger]); // Добавляем refreshTrigger в зависимости

  const loadChartData = React.useCallback(async () => {
    setLoading(true);
    try {
      const response = await gameApi.getGameHistory(gameId);
      if (response.success && response.indicators_history) {
        const data = response.indicators_history.map((indicator: EconomicIndicators, index: number) => ({
          turn: index + 1,
          gdp_growth: indicator.gdp_growth,
          inflation: indicator.inflation,
          unemployment: indicator.unemployment,
          president_rating: indicator.president_rating,
        }));
        setChartData(data);
      }
    } catch (error) {
      console.error('Ошибка загрузки данных графика:', error);
    } finally {
      setLoading(false);
    }
  }, [gameId]);

  if (loading) {
    return (
      <div className="game-chart">
        <h3>Динамика показателей</h3>
        <div className="loading">Загрузка данных...</div>
      </div>
    );
  }

  if (chartData.length === 0) {
    return (
      <div className="game-chart">
        <h3>Динамика показателей</h3>
        <div className="no-data">
          <p>Данных для графика пока нет</p>
          <button onClick={loadChartData}>Обновить</button>
        </div>
      </div>
    );
  }

  return (
    <div className="game-chart">
      <h3>Динамика показателей</h3>
      
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="turn" 
            label={{ value: 'Ход', position: 'insideBottom', offset: -5 }}
          />
          <YAxis />
          <Tooltip 
            formatter={(value: number, name: string) => [
              `${value.toFixed(2)}%`, 
              name === 'gdp_growth' ? 'Рост ВВП' :
              name === 'inflation' ? 'Инфляция' :
              name === 'unemployment' ? 'Безработица' :
              name === 'president_rating' ? 'Рейтинг президента' : name
            ]}
            labelFormatter={(label) => `Ход ${label}`}
          />
          <Legend />
          
          <Line 
            type="monotone" 
            dataKey="gdp_growth" 
            stroke="#8884d8" 
            strokeWidth={2}
            name="Рост ВВП"
          />
          <Line 
            type="monotone" 
            dataKey="inflation" 
            stroke="#82ca9d" 
            strokeWidth={2}
            name="Инфляция"
          />
          <Line 
            type="monotone" 
            dataKey="unemployment" 
            stroke="#ffc658" 
            strokeWidth={2}
            name="Безработица"
          />
          <Line 
            type="monotone" 
            dataKey="president_rating" 
            stroke="#ff7300" 
            strokeWidth={3}
            name="Рейтинг президента"
          />
        </LineChart>
      </ResponsiveContainer>
      
      <div className="chart-controls">
        <button onClick={loadChartData}>Обновить данные</button>
      </div>
    </div>
  );
};

export default GameChart; 