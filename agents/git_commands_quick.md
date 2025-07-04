# ⚡ Быстрые Git команды для агентов

## 🚀 Быстрый старт Git

### Инициализация проекта (Архитектор-агент)
```bash
# 1. Инициализация
git init
git add .
git commit -m "🎯 Initial commit: Project structure and agents setup"

# 2. Создание ветки develop
git checkout -b develop

# 3. Если есть удаленный репозиторий
git remote add origin [URL]
git push -u origin develop
```

### Создание feature веток для спринта
```bash
# Архитектор создает ветки для всех агентов
git checkout develop
git pull origin develop

git checkout -b feature/sprint-1-frontend
git checkout -b feature/sprint-1-backend  
git checkout -b feature/sprint-1-testing

git push origin feature/sprint-1-frontend
git push origin feature/sprint-1-backend
git push origin feature/sprint-1-testing
```

---

## 📝 Ежедневные команды для агентов

### Фронтенд-агент
```bash
# Начало работы
git checkout feature/sprint-1-frontend
git pull origin develop

# Работа над задачами
git add src/components/GameDashboard.tsx
git commit -m "🎨 Add GameDashboard component"

git add src/services/api.ts
git commit -m "🔗 Add API service"

# Конец дня
git push origin feature/sprint-1-frontend
```

### Бэкенд-агент
```bash
# Начало работы
git checkout feature/sprint-1-backend
git pull origin develop

# Работа над задачами
git add game/models.py
git commit -m "🗄️ Add GameSession model"

git add game/views.py
git commit -m "🔌 Add game API views"

# Конец дня
git push origin feature/sprint-1-backend
```

### Агент-тестировщик
```bash
# Начало работы
git checkout feature/sprint-1-testing
git pull origin develop

# Работа над задачами
git add tests/test_api.py
git commit -m "🧪 Add API tests"

git add .github/workflows/ci.yml
git commit -m "🔧 Add CI pipeline"

# Конец дня
git push origin feature/sprint-1-testing
```

---

## 🔄 Интеграция (Архитектор-агент)

### Слияние feature веток
```bash
# Переключение на develop
git checkout develop
git pull origin develop

# Слияние веток агентов
git merge feature/sprint-1-frontend
git merge feature/sprint-1-backend
git merge feature/sprint-1-testing

# Push изменений
git push origin develop
```

### Разрешение конфликтов
```bash
# Если есть конфликты
git status  # посмотреть конфликтующие файлы
# Редактировать файлы, убрать маркеры конфликтов
git add [файлы]
git commit -m "🔧 Resolve merge conflicts"
```

---

## 🏷️ Создание релиза

### Подготовка релиза
```bash
# Создание релизной ветки
git checkout develop
git pull origin develop
git checkout -b release/v1.0.0

# Финальные исправления
git commit -m "🔧 Final fixes for v1.0.0"

# Слияние в main
git checkout main
git merge release/v1.0.0
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin main --tags
```

---

## 🧹 Очистка веток

### Удаление завершенных feature веток
```bash
# Локально
git branch -d feature/sprint-1-frontend
git branch -d feature/sprint-1-backend
git branch -d feature/sprint-1-testing

# На удаленном репозитории
git push origin --delete feature/sprint-1-frontend
git push origin --delete feature/sprint-1-backend
git push origin --delete feature/sprint-1-testing
```

---

## 📊 Полезные команды

### Просмотр истории
```bash
# Последние коммиты
git log --oneline -10

# Статистика по агентам
git shortlog -sn --all

# Изменения в файле
git log -p [файл]
```

### Отмена изменений
```bash
# Отмена последнего коммита
git reset --soft HEAD~1

# Отмена изменений в файле
git checkout -- [файл]

# Отмена всех изменений
git reset --hard HEAD
```

### Временное сохранение
```bash
# Сохранить изменения
git stash

# Посмотреть сохраненные изменения
git stash list

# Применить сохраненные изменения
git stash pop
```

---

## 🎯 Команды для архитектора

### Управление Git
```bash
# Инициализация
Архитектор-агент, инициализируй Git репозиторий

# Создание веток для спринта
Архитектор-агент, создай Git ветки для спринта #[номер]

# Интеграция
Архитектор-агент, проведи интеграцию feature веток

# Релиз
Архитектор-агент, создай релиз v[версия]

# Очистка
Архитектор-агент, очисти завершенные feature ветки
```

### Анализ и контроль
```bash
# Анализ активности
Архитектор-агент, проанализируй Git активность команды

# Проверка качества
Архитектор-агент, проведи code review всех PR

# Метрики
Архитектор-агент, рассчитай Git метрики производительности
```

---

## ⚠️ Важные правила

### Для всех агентов:
1. **Всегда начинайте с `git pull`** - получайте последние изменения
2. **Коммитьте часто** - 2-5 коммитов в день
3. **Используйте префиксы** - 🎨🔗🗄️🔌🧮🧪🔧
4. **Пишите понятные сообщения** - что сделано, а не "fix"
5. **Не коммитьте в develop напрямую** - только через feature ветки

### Для архитектора:
1. **Контролируйте слияния** - проверяйте код перед слиянием
2. **Следите за конфликтами** - разрешайте их быстро
3. **Создавайте релизы** - отмечайте важные версии тегами
4. **Очищайте ветки** - удаляйте завершенные feature ветки
5. **Анализируйте метрики** - следите за производительностью команды 