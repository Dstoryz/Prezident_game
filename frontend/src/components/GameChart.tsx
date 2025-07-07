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
  money_supply: number;
  gold_reserves: number;
  external_debt: number;
  population: number;
}

const availableLines = [
  { key: 'gdp_growth', name: 'Рост ВВП', color: '#8884d8', unit: '%' },
  { key: 'inflation', name: 'Инфляция', color: '#82ca9d', unit: '%' },
  { key: 'unemployment', name: 'Безработица', color: '#ffc658', unit: '%' },
  { key: 'president_rating', name: 'Рейтинг президента', color: '#ff7300', unit: '%' },
  { key: 'money_supply', name: 'Денежная масса', color: '#00bcd4', unit: 'млн $' },
  { key: 'gold_reserves', name: 'Золотой запас', color: '#ffd700', unit: 'млн $' },
  { key: 'external_debt', name: 'Внешний долг', color: '#b71c1c', unit: 'млн $' },
  { key: 'population', name: 'Население', color: '#4caf50', unit: 'чел.' },
];

const GameChart: React.FC<GameChartProps> = ({ gameId, refreshTrigger = 0 }) => {
  const [chartData, setChartData] = useState<ChartData[]>([]);
  const [loading, setLoading] = useState(false);
  const [visibleLines, setVisibleLines] = useState<string[]>(['gdp_growth', 'inflation', 'unemployment', 'president_rating']);

  useEffect(() => {
    loadChartData();
  }, [gameId, refreshTrigger]);

  const loadChartData = React.useCallback(async () => {
    setLoading(true);
    try {
      const response = await gameApi.getGameHistory(gameId);
      if (response.history && Array.isArray(response.history)) {
        const data = response.history
          .sort((a: any, b: any) => a.turn - b.turn)
          .map((item: any) => ({
            turn: item.turn,
            gdp_growth: item.indicators_data.gdp_growth,
            inflation: item.indicators_data.inflation,
            unemployment: item.indicators_data.unemployment,
            president_rating: item.indicators_data.president_rating,
            money_supply: item.indicators_data.money_supply,
            gold_reserves: item.indicators_data.gold_reserves,
            external_debt: item.indicators_data.external_debt,
            population: item.indicators_data.population,
          }));
        setChartData(data);
      }
    } catch (error) {
      console.error('Ошибка загрузки данных графика:', error);
    } finally {
      setLoading(false);
    }
  }, [gameId]);

  const handleLineToggle = (key: string) => {
    setVisibleLines((prev) =>
      prev.includes(key) ? prev.filter((k) => k !== key) : [...prev, key]
    );
  };

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
      <div className="chart-line-toggles">
        {availableLines.map((line) => (
          <label key={line.key} style={{ marginRight: 16 }}>
            <input
              type="checkbox"
              checked={visibleLines.includes(line.key)}
              onChange={() => handleLineToggle(line.key)}
            />
            <span style={{ color: line.color, marginLeft: 4 }}>{line.name}</span>
          </label>
        ))}
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="turn" 
            label={{ value: 'Ход', position: 'insideBottom', offset: -5 }}
          />
          <YAxis />
          <Tooltip 
            formatter={(value: number, name: string) => {
              const line = availableLines.find(l => l.key === name);
              return [
                typeof value === 'number' ? value.toLocaleString() : value,
                line ? line.name : name
              ];
            }}
            labelFormatter={(label) => `Ход ${label}`}
          />
          <Legend />
          {availableLines.filter(line => visibleLines.includes(line.key)).map(line => (
            <Line
              key={line.key}
              type="monotone"
              dataKey={line.key}
              stroke={line.color}
              strokeWidth={2}
              name={line.name}
              dot={false}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
      <div className="chart-controls">
        <button onClick={loadChartData}>Обновить данные</button>
      </div>
    </div>
  );
};

export default GameChart; 