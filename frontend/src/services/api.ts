import axios from 'axios';
import { GameSession, NextTurnRequest, ApiResponse } from '../types/game';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Добавляем интерцептор для автоматического добавления токена авторизации
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Интерцептор для обработки ошибок авторизации
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Токен истёк, пробуем обновить
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/token/refresh/`, {
            refresh: refreshToken,
          });
          localStorage.setItem('access_token', response.data.access);
          
          // Повторяем оригинальный запрос
          error.config.headers.Authorization = `Bearer ${response.data.access}`;
          return api.request(error.config);
        } catch (refreshError) {
          // Не удалось обновить токен, перенаправляем на страницу входа
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.reload();
        }
      }
    }
    return Promise.reject(error);
  }
);

export const gameApi = {
  // Начать новую игру
  startGame: async (): Promise<ApiResponse<GameSession>> => {
    const response = await api.post('/game/start/');
    return response.data;
  },

  // Получить состояние игры
  getGameState: async (gameId: number): Promise<ApiResponse<GameSession>> => {
    const response = await api.get(`/game/${gameId}/state/`);
    return response.data;
  },

  // Сделать следующий ход
  nextTurn: async (gameId: number, parameters: NextTurnRequest): Promise<ApiResponse<GameSession>> => {
    const response = await api.post(`/game/${gameId}/next-turn/`, parameters);
    return response.data;
  },

  // Получить историю игры
  getGameHistory: async (gameId: number) => {
    const response = await api.get(`/game/${gameId}/history/`);
    return response.data;
  },
}; 