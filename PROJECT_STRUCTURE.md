# 📁 Структура проекта Prezident_project

## Корень проекта
- README.md — главное описание
- PROJECT_STRUCTURE.md — структура проекта (этот файл)
- archive/ — архив устаревших и неиспользуемых файлов
- docs/ — документация, спецификации, отчёты

## Каталог agents/
- supervisor_agent.md         — Агент-надзиратель (контроль и корректировка)
- architect_agent.md          — Агент-архитектор (координация и планирование)
- backend_agent.md            — Бэкенд-агент (API, бизнес-логика)
- frontend_agent.md           — Фронтенд-агент (UI/UX)
- testing_agent.md            — Агент-тестировщик (качество и тесты)
- devops_agent.md             — Агент-DevOps (инфраструктура, CI/CD)
- analyst_agent.md            — Агент-аналитик (данные, отчёты)
- start_supervisor_system.sh  — Запуск оркестра агентов с надзирателем
- start_optimized_agents.sh   — Запуск оптимизированной системы агентов
- start_agents.sh             — Запуск базовой системы агентов
- metrics/                    — Метрики эффективности агентов
- monitoring/                 — Дашборд и система алертов
- scripts/                    — Вспомогательные скрипты

## Каталог backend/
- auth_app/                   — Модуль аутентификации (Django)
- game/                       — Игровая логика, модели, сервисы
- prezident_game/             — Django-проект (настройки, запуск)
- requirements.txt            — Зависимости Python

## Каталог frontend/
- src/                        — Исходники React-приложения
- public/                     — Публичные файлы (иконки, manifest и т.д.)
- package.json                — Зависимости Node.js

## Каталог archive/
- simple_test.py, test_economic_model.py, ... — устаревшие тесты и скрипты

## Каталог docs/
- development_plan.md, macro_model_description.md, ... — документация, спецификации, отчёты

---

**Все агенты и скрипты должны использовать этот файл как источник истины для построения путей и поиска файлов!**

- Для Python: используйте os.path.join(BASE_DIR, ...)
- Для Bash: используйте $PROJECT_ROOT/путь/к/файлу
- Для Node.js: используйте path.join(__dirname, ...)

**Обновляйте этот файл при изменении структуры проекта!** 