import axios from 'axios';
import { GameSession, NextTurnRequest, ApiResponse } from '../types/game';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Интерцептор для добавления токена к запросам
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
      // Пытаемся обновить токен
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/dj-rest-auth/token/refresh/`, {
            refresh: refreshToken
          });
          localStorage.setItem('access_token', response.data.access);
          // Повторяем оригинальный запрос
          const originalRequest = error.config;
          originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
          return api(originalRequest);
        } catch (refreshError) {
          // Не удалось обновить токен, просто сбрасываем токены
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
        }
      } else {
        // Нет токена, просто сбрасываем токены
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
      }
    }
    return Promise.reject(error);
  }
);

export const authApi = {
  // Регистрация
  register: async (userData: { email: string; password: string }) => {
    const response = await api.post('/dj-rest-auth/registration/', userData);
    if (response.data.access) {
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
    }
    return response.data;
  },

  // Вход
  login: async (credentials: { email: string; password: string }) => {
    const response = await api.post('/dj-rest-auth/login/', credentials);
    if (response.data.access) {
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
    }
    return response.data;
  },

  // Выход
  logout: async () => {
    try {
      await api.post('/dj-rest-auth/logout/');
      // Только при успешном выходе удаляем токены
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    } catch (error) {
      console.error('Ошибка при выходе:', error);
      // При ошибке токены НЕ удаляем, чтобы пользователь мог продолжить работу
    }
  },

  // Получить информацию о пользователе
  getUser: async () => {
    const response = await api.get('/dj-rest-auth/user/');
    return response.data;
  },
};

export const gameApi = {
  // Начать новую игру
  startGame: async (initialParameters = {}) => {
    const response = await api.post('/game/start/', { initial_parameters: initialParameters });
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