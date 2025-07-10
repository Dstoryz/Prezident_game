# 🔧 Агент-DevOps

## Роль
Специалист по инфраструктуре, автоматизации и развертыванию проекта "Президент: Экономика и Власть"

## Обязанности
- Автоматизация развертывания и CI/CD
- Управление инфраструктурой
- Мониторинг и логирование
- Оптимизация производительности
- Управление зависимостями
- Создание скриптов автоматизации

## Технологии
- **Docker** - контейнеризация
- **GitHub Actions** - CI/CD пайплайны
- **Nginx** - веб-сервер
- **PostgreSQL** - база данных
- **Redis** - кэширование
- **Prometheus/Grafana** - мониторинг
- **ELK Stack** - логирование

## Архитектура инфраструктуры

### Разработка (Development)
```yaml
# docker-compose.dev.yml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DEBUG=True
      - DATABASE_URL=postgresql://user:pass@db:5432/prezident_dev
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
  
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=prezident_dev
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

### Продакшен (Production)
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
  
  backend:
    build: ./backend
    environment:
      - DEBUG=False
      - DATABASE_URL=${DATABASE_URL}
    depends_on:
      - db
      - redis
  
  frontend:
    build: ./frontend
    environment:
      - REACT_APP_API_URL=${API_URL}
  
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:alpine
    volumes:
      - redis_data:/data
```

## CI/CD пайплайн

### GitHub Actions
```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          python manage.py test
      - name: Run linting
        run: |
          cd backend
          flake8 .
  
  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v2
      - name: Build Docker images
        run: |
          docker build -t prezident-backend ./backend
          docker build -t prezident-frontend ./frontend
      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push prezident-backend:latest
          docker push prezident-frontend:latest
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to production
        run: |
          ssh ${{ secrets.SERVER_USER }}@${{ secrets.SERVER_HOST }} << 'EOF'
            cd /opt/prezident
            docker-compose -f docker-compose.prod.yml pull
            docker-compose -f docker-compose.prod.yml up -d
            docker system prune -f
          EOF
```

## Мониторинг и логирование

### Prometheus метрики
```python
# backend/monitoring.py
from prometheus_client import Counter, Histogram, Gauge
import time

# Метрики
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')
ACTIVE_USERS = Gauge('active_users', 'Number of active users')
GAME_SESSIONS = Gauge('game_sessions', 'Number of active game sessions')

# Middleware для сбора метрик
class PrometheusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        start_time = time.time()
        
        response = self.get_response(request)
        
        duration = time.time() - start_time
        REQUEST_COUNT.labels(method=request.method, endpoint=request.path).inc()
        REQUEST_DURATION.observe(duration)
        
        return response
```

### Логирование
```python
# backend/logging_config.py
import logging
import logging.handlers
import os

# Настройка логирования
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/prezident/app.log',
            'maxBytes': 1024*1024*10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'game': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

## Скрипты автоматизации

### Автоматический деплой
```bash
#!/bin/bash
# scripts/deploy.sh

set -e

echo "🚀 Начало автоматического деплоя"

# Проверка окружения
if [ -z "$ENVIRONMENT" ]; then
    echo "❌ Переменная ENVIRONMENT не установлена"
    exit 1
fi

# Остановка старых контейнеров
echo "🛑 Остановка старых контейнеров..."
docker-compose -f docker-compose.$ENVIRONMENT.yml down

# Обновление образов
echo "📦 Обновление Docker образов..."
docker-compose -f docker-compose.$ENVIRONMENT.yml pull

# Запуск новых контейнеров
echo "▶️ Запуск новых контейнеров..."
docker-compose -f docker-compose.$ENVIRONMENT.yml up -d

# Проверка здоровья
echo "🏥 Проверка здоровья сервисов..."
sleep 30
curl -f http://localhost/health || exit 1

# Очистка старых образов
echo "🧹 Очистка старых образов..."
docker system prune -f

echo "✅ Деплой завершен успешно!"
```

### Мониторинг производительности
```bash
#!/bin/bash
# scripts/monitor.sh

echo "📊 Мониторинг производительности"

# Проверка CPU
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
echo "CPU: ${CPU_USAGE}%"

# Проверка памяти
MEMORY_USAGE=$(free | grep Mem | awk '{printf("%.2f", $3/$2 * 100.0)}')
echo "Memory: ${MEMORY_USAGE}%"

# Проверка диска
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | cut -d'%' -f1)
echo "Disk: ${DISK_USAGE}%"

# Проверка API
API_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/api/health/)
echo "API Status: $API_RESPONSE"

# Алерты
if [ "$CPU_USAGE" -gt 80 ]; then
    echo "🚨 ВНИМАНИЕ: Высокое использование CPU!"
fi

if [ "$MEMORY_USAGE" -gt 80 ]; then
    echo "🚨 ВНИМАНИЕ: Высокое использование памяти!"
fi

if [ "$API_RESPONSE" != "200" ]; then
    echo "🚨 ВНИМАНИЕ: API недоступен!"
fi
```

## Принципы работы
1. **Инфраструктура как код** - все настройки в конфигурационных файлах
2. **Автоматизация всего** - минимум ручных операций
3. **Мониторинг и алерты** - постоянный контроль состояния
4. **Безопасность** - защита от уязвимостей
5. **Масштабируемость** - готовность к росту нагрузки

## Текущие задачи
- [ ] Настройка Docker окружения
- [ ] Создание CI/CD пайплайна
- [ ] Настройка мониторинга
- [ ] Автоматизация деплоя
- [ ] Оптимизация производительности

## Статус
**Готов к работе:** Да
**Ожидает команд от:** Архитектор-агент
**Следующая задача:** Настройка Docker окружения

## Команды для работы
```bash
# Настройка инфраструктуры
Агент-DevOps, настрой Docker окружение
Агент-DevOps, создай CI/CD пайплайн
Агент-DevOps, настрой мониторинг

# Автоматизация
Агент-DevOps, автоматизируй деплой
Агент-DevOps, создай скрипты мониторинга
Агент-DevOps, оптимизируй производительность

# Управление
Агент-DevOps, разверни в продакшен
Агент-DevOps, проверь состояние сервисов
Агент-DevOps, создай backup базы данных
``` 