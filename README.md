# 🎮 Президент: Экономика и Власть

Браузерная экономико-политическая стратегия, где вы управляете страной в роли президента.

## 🚀 Быстрый запуск

### Один скрипт для всего
```bash
./start_project.sh
```

Этот скрипт автоматически:
- Проверит зависимости (Python 3.9+, Node.js 16+)
- Настроит виртуальное окружение Django
- Установит все зависимости
- Запустит бэкенд и фронтенд
- Откроет проект в браузере

### Команды скрипта
```bash
./start_project.sh          # Запустить проект
./start_project.sh stop     # Остановить проект
./start_project.sh restart  # Перезапустить проект
./start_project.sh status   # Показать статус процессов
./start_project.sh logs     # Показать логи в реальном времени
```

## 📋 Требования

- **Python 3.9+**
- **Node.js 16+**
- **npm**

## 🏗️ Архитектура

### Бэкенд (Django)
- **Django 5.2.4** - основной фреймворк
- **Django REST Framework** - API
- **SQLite** - база данных
- **Экономическая логика** - расчет показателей
- **Система событий** - случайные события

### Фронтенд (React)
- **React 18** с TypeScript
- **Recharts** - графики
- **Axios** - HTTP клиент
- **Адаптивный дизайн** - работает на всех устройствах

## 🎯 Игровая механика

### Управляемые параметры
- **Процентная ставка** - влияет на инфляцию и безработицу
- **Налоговая нагрузка** - влияет на инвестиции и настроение
- **Государственные расходы** - стимулируют ВВП
- **Таможенные пошлины** - влияют на внешнюю торговлю

### Экономические показатели
- **Рост ВВП** - основной показатель экономики
- **Инфляция** - рост цен
- **Безработица** - уровень занятости
- **Рейтинг президента** - поддержка населения
- **Инвестиции** - объем капиталовложений

### События
- Природные катастрофы
- Экономические кризисы
- Международные санкции
- Социальные протесты
- Изменения цен на сырье

## 🔧 Ручная установка

### Бэкенд
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000
```

### Фронтенд
```bash
cd frontend
npm install
npm start
```

## 🌐 Доступные URL

- **Фронтенд**: http://localhost:3000
- **Бэкенд API**: http://localhost:8000
- **Админ панель**: http://localhost:8000/admin

## 📊 API Endpoints

- `POST /api/game/start/` - начать новую игру
- `POST /api/game/{id}/next-turn/` - сделать следующий ход
- `GET /api/game/{id}/state/` - получить состояние игры
- `GET /api/game/{id}/history/` - получить историю игры

## 🎮 Как играть

1. **Начните игру** - система создаст новую сессию
2. **Настройте параметры** - используйте слайдеры для управления экономикой
3. **Сделайте ход** - нажмите "Следующий ход"
4. **Анализируйте результаты** - смотрите на показатели и события
5. **Планируйте стратегию** - адаптируйтесь к изменениям
6. **Держите рейтинг выше 50%** - иначе проиграете на выборах

## 🏆 Цель игры

Управляйте экономикой так, чтобы как можно дольше оставаться у власти. Каждые 4 года проходят выборы - если ваш рейтинг упадет ниже 50%, игра закончится.

## 🐛 Устранение неполадок

### Django не запускается
```bash
cd backend
source venv/bin/activate
python manage.py check
python manage.py migrate
```

### React не запускается
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Проблемы с портами
```bash
# Проверить занятые порты
lsof -i :3000
lsof -i :8000

# Остановить процессы
pkill -f "manage.py runserver"
pkill -f "react-scripts start"
```

## 📝 Логи

- **Бэкенд**: `backend.log`
- **Фронтенд**: `frontend.log`

## 📁 Структура проекта

```
Prezident_project/
├── backend/                 # Django бэкенд
│   ├── game/               # Основное приложение
│   ├── prezident_game/     # Настройки Django
│   ├── requirements.txt    # Python зависимости
│   └── manage.py          # Django CLI
├── frontend/               # React фронтенд
│   ├── src/
│   │   ├── components/     # React компоненты
│   │   ├── services/       # API сервисы
│   │   └── types/          # TypeScript типы
│   ├── package.json        # Node.js зависимости
│   └── public/             # Статические файлы
├── agents/                 # Документация агентов
├── docs/                   # Документация проекта
├── start_project.sh        # Скрипт запуска
└── README.md              # Этот файл
```

## 🤝 Разработка

Проект создан системой агентов:
- 🏗️ **Архитектор-агент** - планирование и координация
- ⚙️ **Бэкенд-агент** - Django и API
- 🎨 **Фронтенд-агент** - React и UI
- 🐛 **Агент-тестировщик** - качество и отладка

### Команды для разработчиков

#### Бэкенд разработка
```bash
cd backend
source venv/bin/activate
python manage.py makemigrations  # Создать миграции
python manage.py migrate         # Применить миграции
python manage.py createsuperuser # Создать админа
python manage.py shell           # Django shell
```

#### Фронтенд разработка
```bash
cd frontend
npm run build     # Сборка для продакшена
npm run test      # Запуск тестов
npm run lint      # Проверка кода
```

#### Отладка
```bash
# Просмотр логов в реальном времени
./start_project.sh logs

# Проверка статуса сервисов
./start_project.sh status

# Очистка и перезапуск
./start_project.sh restart
```

## 🎯 Стратегия победы

### Основные принципы
- **Баланс экономики** - поддерживайте оптимальные показатели
- **Адаптивность** - реагируйте на события и кризисы
- **Долгосрочное планирование** - готовьтесь к выборам заранее
- **Управление рисками** - избегайте экстремальных значений параметров

### Рекомендуемые показатели
- **ВВП**: стабильный рост 2-4% в год
- **Инфляция**: 2-5% (избегайте дефляции и гиперинфляции)
- **Безработица**: 4-8%
- **Рейтинг президента**: всегда выше 50%

### Советы по игре
1. **Начало игры**: используйте умеренные значения параметров
2. **Развитие**: постепенно увеличивайте госрасходы для роста ВВП
3. **Подготовка к выборам**: за 1-2 года до выборов снижайте налоги
4. **Кризисы**: при событиях используйте госрасходы для стабилизации
5. **Мониторинг**: постоянно следите за графиками и событиями

## 🔄 Обновления

### Последние изменения
- ✅ Автоматическое обновление графиков после ходов
- ✅ Система событий с влиянием на экономику
- ✅ Адаптивный интерфейс для мобильных устройств
- ✅ Улучшенная экономическая логика
- ✅ Автоматический запуск проекта одним скриптом

### Планы развития
- [ ] Система достижений
- [ ] Множественные сценарии игры
- [ ] Экспорт/импорт сохранений
- [ ] Статистика игроков
- [ ] Мультиплеер (опционально)

## 📄 Лицензия

MIT License

## 👤 Аутентификация и пользователи

### Основные эндпоинты

- `POST /api/auth/register/` — регистрация пользователя
- `POST /api/auth/login/` — вход (получение JWT-токенов)
- `POST /api/auth/logout/` — выход (блэклистинг refresh-токена)
- `GET  /api/auth/profile/` — получить/обновить профиль
- `POST /api/auth/change-password/` — смена пароля
- `GET  /api/auth/stats/` — статистика пользователя
- `POST /api/auth/update-stats/` — обновить игровую статистику
- `GET  /api/game/` — список игр пользователя
- `POST /api/game/start/` — начать новую игру (требует авторизации)

### Google OAuth2

Проект поддерживает вход через Google аккаунт:

- `GET /api/auth/google/` — инициация Google OAuth
- `GET /api/auth/google/callback/` — обработка callback от Google
- `POST /api/auth/google/complete/` — завершение авторизации

#### Настройка Google OAuth2

1. **Создайте проект в Google Cloud Console:**
   - Перейдите на https://console.cloud.google.com/
   - Создайте новый проект или выберите существующий

2. **Включите Google+ API:**
   - В меню слева выберите "APIs & Services" → "Library"
   - Найдите и включите "Google+ API"

3. **Создайте OAuth 2.0 credentials:**
   - Перейдите в "APIs & Services" → "Credentials"
   - Нажмите "Create Credentials" → "OAuth 2.0 Client IDs"
   - Выберите "Web application"

4. **Настройте разрешенные redirect URIs:**
   - Добавьте: `http://localhost:8000/accounts/google/callback/`
   - Сохраните изменения

5. **Скопируйте данные:**
   - Client ID
   - Client Secret

6. **Добавьте в Django админку:**
   - Откройте http://localhost:8000/admin/
   - Перейдите в "Social Applications"
   - Создайте новую запись:
     - Provider: Google
     - Name: Google OAuth2
     - Client ID: ваш_client_id
     - Secret Key: ваш_client_secret
     - Sites: добавьте localhost:8000

### Пример регистрации
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H 'Content-Type: application/json' \
  -d '{"email": "user@example.com", "username": "user1", "password": "password123", "password_confirm": "password123"}'
```

### Пример логина
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H 'Content-Type: application/json' \
  -d '{"email": "user@example.com", "password": "password123"}'
```
Ответ:
```json
{
  "message": "Успешная авторизация",
  "user": { ... },
  "tokens": {
    "refresh": "...",
    "access": "..."
  }
}
```

### Использование JWT на фронте
- После логина сохраняйте `access` и `refresh` токены (например, в localStorage).
- Для всех защищённых запросов добавляйте заголовок:
  `Authorization: Bearer <access_token>`
- Для обновления access-токена используйте:
  `POST /api/token/refresh/` с телом `{ "refresh": "<refresh_token>" }`

### Пример защищённого запроса
```bash
curl -H "Authorization: Bearer <access_token>" http://localhost:8000/api/game/
```

### Выход
```bash
curl -X POST http://localhost:8000/api/auth/logout/ \
  -H 'Authorization: Bearer <access_token>' \
  -d '{"refresh_token": "<refresh_token>"}'
```

---

**Важно:** Все игровые действия теперь требуют авторизации. Каждый пользователь видит только свои игры и статистику. 