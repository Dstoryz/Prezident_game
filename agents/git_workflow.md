# 🔄 Git Workflow для системы агентов

## 🎯 Git стратегия для проекта

### Модель ветвления: Git Flow
```
main (production)
├── develop (integration)
├── feature/frontend-*
├── feature/backend-*
├── feature/testing-*
├── hotfix/*
└── release/*
```

## 📋 Git команды для агентов

### 🏗️ Архитектор-агент (Git Master)

#### Инициализация и настройка
```bash
# Инициализация репозитория
git init
git add .
git commit -m "🎯 Initial commit: Project structure and agents setup"

# Настройка .gitignore
git add .gitignore
git commit -m "📝 Add .gitignore for Python and Node.js"

# Создание основной ветки develop
git checkout -b develop
git push -u origin develop
```

#### Управление ветками
```bash
# Создание feature веток для агентов
git checkout -b feature/frontend-setup
git checkout -b feature/backend-setup
git checkout -b feature/testing-setup

# Слияние feature веток
git checkout develop
git merge feature/frontend-setup
git merge feature/backend-setup
git merge feature/testing-setup
```

#### Релизы и hotfix
```bash
# Создание релизной ветки
git checkout -b release/v1.0.0
git checkout main
git merge release/v1.0.0
git tag -a v1.0.0 -m "Release version 1.0.0"

# Hotfix для критических багов
git checkout -b hotfix/critical-bug
# исправления
git checkout main
git merge hotfix/critical-bug
```

### 🎨 Фронтенд-агент

#### Рабочий процесс
```bash
# Создание feature ветки
git checkout develop
git pull origin develop
git checkout -b feature/frontend-game-dashboard

# Разработка
# ... работа над компонентами ...

# Коммиты с префиксами
git add src/components/GameDashboard.tsx
git commit -m "🎨 Add GameDashboard component with basic layout"

git add src/components/ParameterControls.tsx
git commit -m "🎨 Add ParameterControls with sliders and inputs"

git add src/services/api.ts
git commit -m "🔗 Add API service for game integration"

# Push и создание Pull Request
git push origin feature/frontend-game-dashboard
```

#### Префиксы коммитов
- `🎨` - UI/UX изменения
- `🔗` - API интеграция
- `⚡` - Оптимизация производительности
- `🐛` - Исправление багов
- `📱` - Адаптивность
- `🧪` - Тесты

### ⚙️ Бэкенд-агент

#### Рабочий процесс
```bash
# Создание feature ветки
git checkout develop
git pull origin develop
git checkout -b feature/backend-game-models

# Разработка
# ... работа над моделями и API ...

# Коммиты с префиксами
git add game/models.py
git commit -m "🗄️ Add GameSession and GameParameters models"

git add game/views.py
git commit -m "🔌 Add API views for game management"

git add game/services/economic_logic.py
git commit -m "🧮 Implement economic calculation logic"

git add game/serializers.py
git commit -m "📊 Add serializers for API responses"

# Push и создание Pull Request
git push origin feature/backend-game-models
```

#### Префиксы коммитов
- `🗄️` - Модели данных
- `🔌` - API эндпоинты
- `🧮` - Бизнес-логика
- `📊` - Сериализаторы
- `🔒` - Безопасность
- `⚡` - Оптимизация
- `🐛` - Исправление багов

### 🐛 Агент-тестировщик

#### Рабочий процесс
```bash
# Создание feature ветки
git checkout develop
git pull origin develop
git checkout -b feature/testing-api-endpoints

# Тестирование и исправления
# ... работа над тестами ...

# Коммиты с префиксами
git add tests/test_api.py
git commit -m "🧪 Add API endpoint tests"

git add tests/test_economic_logic.py
git commit -m "🧪 Add economic logic validation tests"

git add .github/workflows/tests.yml
git commit -m "🔧 Add CI/CD pipeline for automated testing"

# Push и создание Pull Request
git push origin feature/testing-api-endpoints
```

#### Префиксы коммитов
- `🧪` - Тесты
- `🔧` - CI/CD
- `🐛` - Исправление багов
- `📊` - Метрики качества
- `🔒` - Тесты безопасности

---

## 📋 Git Workflow по этапам

### 1. Планирование (Архитектор-агент)
```bash
# Создание веток для спринта
git checkout develop
git pull origin develop

# Создание веток для каждого агента
git checkout -b feature/sprint-1-frontend
git checkout -b feature/sprint-1-backend
git checkout -b feature/sprint-1-testing

# Push веток
git push origin feature/sprint-1-frontend
git push origin feature/sprint-1-backend
git push origin feature/sprint-1-testing
```

### 2. Разработка (Агенты)
```bash
# Каждый агент работает в своей ветке
git checkout feature/sprint-1-[agent-name]
git pull origin develop  # Получить последние изменения

# Регулярные коммиты
git add .
git commit -m "[префикс] [описание изменений]"

# Push изменений
git push origin feature/sprint-1-[agent-name]
```

### 3. Интеграция (Архитектор-агент)
```bash
# Слияние feature веток в develop
git checkout develop
git merge feature/sprint-1-frontend
git merge feature/sprint-1-backend
git merge feature/sprint-1-testing

# Тестирование интеграции
git push origin develop
```

### 4. Релиз (Архитектор-агент)
```bash
# Создание релизной ветки
git checkout -b release/v1.0.0
# Финальные исправления
git commit -m "🔧 Final fixes for release v1.0.0"

# Слияние в main
git checkout main
git merge release/v1.0.0
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin main --tags
```

---

## 🚀 Автоматизация с GitHub Actions

### CI/CD Pipeline
```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [develop, main]
  pull_request:
    branches: [develop]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          python manage.py test

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '16'
      - name: Install dependencies
        run: |
          cd frontend
          npm install
      - name: Run tests
        run: |
          cd frontend
          npm test
```

---

## 📊 Git метрики для архитектора

### Команды для анализа
```bash
# Статистика коммитов по агентам
git shortlog -sn --all

# Активность по дням
git log --pretty=format:"%ad" --date=short | sort | uniq -c

# Размер изменений
git diff --stat HEAD~10

# Время до слияния PR
git log --merges --pretty=format:"%H %ad %s" --date=short
```

### Метрики качества
- **Время до слияния PR** - < 2 дней
- **Размер PR** - < 500 строк
- **Частота коммитов** - 2-5 коммитов/день
- **Покрытие тестами** - > 80%

---

## 🎯 Команды для архитектора

### Управление Git
```bash
# Инициализация проекта
Архитектор-агент, инициализируй Git репозиторий

# Создание веток для спринта
Архитектор-агент, создай Git ветки для спринта #1

# Слияние feature веток
Архитектор-агент, проведи интеграцию feature веток

# Создание релиза
Архитектор-агент, создай релиз v1.0.0

# Анализ метрик
Архитектор-агент, проанализируй Git метрики команды
```

### Контроль качества
```bash
# Проверка PR
Архитектор-агент, проведи code review PR #[номер]

# Анализ конфликтов
Архитектор-агент, разреши Git конфликты в [ветка]

# Очистка веток
Архитектор-агент, очисти завершенные feature ветки
``` 