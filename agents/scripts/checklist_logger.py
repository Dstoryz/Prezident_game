#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
📊 Модуль для логирования результатов проверок туду листа
Автоматическое ведение журнала проверок и генерация отчетов
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class CheckStatus(Enum):
    """Статусы проверок"""
    PASSED = "✅"
    WARNING = "⚠️"
    FAILED = "❌"
    CRITICAL = "🚨"

@dataclass
class CheckResult:
    """Результат одной проверки"""
    timestamp: str
    category: str
    item: str
    status: CheckStatus
    details: Optional[str] = None
    agent: str = "testing_agent"
    duration: Optional[float] = None
    error_message: Optional[str] = None

class ChecklistLogger:
    """Логгер для ведения журнала проверок туду листа"""
    
    def __init__(self, log_file: str = "logs/checklist.log"):
        self.log_file = log_file
        self.results: List[CheckResult] = []
        self._ensure_log_directory()
    
    def _ensure_log_directory(self):
        """Создание директории для логов"""
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
    
    def log_check(self, category: str, item: str, status: CheckStatus, 
                  details: Optional[str] = None, duration: Optional[float] = None,
                  error_message: Optional[str] = None) -> None:
        """
        Логирование результата проверки
        
        Args:
            category: Категория проверки (например, "Аутентификация")
            item: Название проверяемого элемента
            status: Статус проверки
            details: Дополнительные детали
            duration: Время выполнения в секундах
            error_message: Сообщение об ошибке
        """
        result = CheckResult(
            timestamp=datetime.now().isoformat(),
            category=category,
            item=item,
            status=status,
            details=details,
            duration=duration,
            error_message=error_message
        )
        
        self.results.append(result)
        self._save_result(result)
        
        # Вывод в консоль
        status_emoji = status.value
        print(f"{status_emoji} {category}: {item}")
        if details:
            print(f"   📝 {details}")
        if error_message:
            print(f"   ❌ Ошибка: {error_message}")
        if duration:
            print(f"   ⏱️  Время: {duration:.2f}с")
    
    def _save_result(self, result: CheckResult) -> None:
        """Сохранение результата в файл"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                json.dump(asdict(result), f, ensure_ascii=False)
                f.write('\n')
        except Exception as e:
            print(f"Ошибка сохранения лога: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Получение статистики по результатам"""
        total = len(self.results)
        passed = len([r for r in self.results if r.status == CheckStatus.PASSED])
        warnings = len([r for r in self.results if r.status == CheckStatus.WARNING])
        failed = len([r for r in self.results if r.status == CheckStatus.FAILED])
        critical = len([r for r in self.results if r.status == CheckStatus.CRITICAL])
        
        return {
            'total_checks': total,
            'passed': passed,
            'warnings': warnings,
            'failed': failed,
            'critical_issues': critical,
            'success_rate': (passed / total * 100) if total > 0 else 0
        }
    
    def get_critical_issues(self) -> List[CheckResult]:
        """Получение критических проблем"""
        return [r for r in self.results if r.status == CheckStatus.CRITICAL]
    
    def get_failed_checks(self) -> List[CheckResult]:
        """Получение неудачных проверок"""
        return [r for r in self.results if r.status in [CheckStatus.FAILED, CheckStatus.CRITICAL]]
    
    def get_checks_by_category(self, category: str) -> List[CheckResult]:
        """Получение проверок по категории"""
        return [r for r in self.results if r.category == category]
    
    def generate_report(self, output_file: Optional[str] = None) -> str:
        """
        Генерация отчета по результатам проверок
        
        Args:
            output_file: Файл для сохранения отчета (опционально)
        
        Returns:
            Текст отчета
        """
        stats = self.get_statistics()
        critical_issues = self.get_critical_issues()
        failed_checks = self.get_failed_checks()
        
        # Группировка по категориям
        categories = {}
        for result in self.results:
            if result.category not in categories:
                categories[result.category] = []
            categories[result.category].append(result)
        
        # Формирование отчета
        report = []
        report.append("# 📋 Отчет о выполнении туду листа")
        report.append(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Версия: 1.0.0")
        report.append(f"Проверяющий: Агент-тестировщик")
        report.append("")
        
        # Статистика
        report.append("## 📊 Статистика")
        report.append(f"- Всего проверок: {stats['total_checks']}")
        report.append(f"- Пройдено: {stats['passed']} ✅")
        report.append(f"- Предупреждения: {stats['warnings']} ⚠️")
        report.append(f"- Ошибки: {stats['failed']} ❌")
        report.append(f"- Критические: {stats['critical_issues']} 🚨")
        report.append(f"- Процент успеха: {stats['success_rate']:.1f}%")
        report.append("")
        
        # Критические проблемы
        if critical_issues:
            report.append("## 🚨 Критические проблемы")
            for i, issue in enumerate(critical_issues, 1):
                report.append(f"{i}. **{issue.category}: {issue.item}**")
                if issue.error_message:
                    report.append(f"   Ошибка: {issue.error_message}")
                if issue.details:
                    report.append(f"   Детали: {issue.details}")
            report.append("")
        
        # Неудачные проверки
        if failed_checks:
            report.append("## ❌ Неудачные проверки")
            for check in failed_checks:
                report.append(f"- **{check.category}: {check.item}**")
                if check.error_message:
                    report.append(f"  - Ошибка: {check.error_message}")
            report.append("")
        
        # Результаты по категориям
        report.append("## 📂 Результаты по категориям")
        for category, checks in categories.items():
            passed = len([c for c in checks if c.status == CheckStatus.PASSED])
            total = len(checks)
            success_rate = (passed / total * 100) if total > 0 else 0
            
            report.append(f"### {category}")
            report.append(f"- Пройдено: {passed}/{total} ({success_rate:.1f}%)")
            
            # Детали по категории
            for check in checks:
                status_emoji = check.status.value
                report.append(f"- {status_emoji} {check.item}")
                if check.details:
                    report.append(f"  - {check.details}")
            report.append("")
        
        # Рекомендации
        report.append("## 💡 Рекомендации")
        if critical_issues:
            report.append("1. **НЕМЕДЛЕННО исправить критические проблемы**")
            for issue in critical_issues:
                report.append(f"   - {issue.category}: {issue.item}")
        else:
            report.append("1. ✅ Критических проблем не обнаружено")
        
        if stats['failed'] > 0:
            report.append("2. Исправить неудачные проверки")
        
        if stats['warnings'] > 0:
            report.append("3. Рассмотреть предупреждения")
        
        report.append("4. Запустить полную проверку после исправлений")
        report.append("")
        
        # Временные метрики
        durations = [r.duration for r in self.results if r.duration is not None]
        if durations:
            avg_duration = sum(durations) / len(durations)
            max_duration = max(durations)
            report.append("## ⏱️ Временные метрики")
            report.append(f"- Среднее время проверки: {avg_duration:.2f}с")
            report.append(f"- Максимальное время: {max_duration:.2f}с")
            report.append("")
        
        report_text = "\n".join(report)
        
        # Сохранение в файл
        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(report_text)
                print(f"📄 Отчет сохранен в {output_file}")
            except Exception as e:
                print(f"Ошибка сохранения отчета: {e}")
        
        return report_text
    
    def clear_logs(self) -> None:
        """Очистка всех логов"""
        self.results.clear()
        try:
            if os.path.exists(self.log_file):
                os.remove(self.log_file)
            print("🧹 Логи очищены")
        except Exception as e:
            print(f"Ошибка очистки логов: {e}")
    
    def load_from_file(self) -> None:
        """Загрузка результатов из файла"""
        if not os.path.exists(self.log_file):
            return
        
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        result = CheckResult(**data)
                        self.results.append(result)
            print(f"📂 Загружено {len(self.results)} результатов из {self.log_file}")
        except Exception as e:
            print(f"Ошибка загрузки логов: {e}")

# Глобальный экземпляр логгера
logger = ChecklistLogger()

# Функции-помощники для быстрого логирования
def log_success(category: str, item: str, details: Optional[str] = None, duration: Optional[float] = None):
    """Логирование успешной проверки"""
    logger.log_check(category, item, CheckStatus.PASSED, details, duration)

def log_warning(category: str, item: str, details: Optional[str] = None, duration: Optional[float] = None):
    """Логирование предупреждения"""
    logger.log_check(category, item, CheckStatus.WARNING, details, duration)

def log_error(category: str, item: str, error_message: str, details: Optional[str] = None, duration: Optional[float] = None):
    """Логирование ошибки"""
    logger.log_check(category, item, CheckStatus.FAILED, details, duration, error_message)

def log_critical(category: str, item: str, error_message: str, details: Optional[str] = None, duration: Optional[float] = None):
    """Логирование критической ошибки"""
    logger.log_check(category, item, CheckStatus.CRITICAL, details, duration, error_message)

if __name__ == "__main__":
    # Пример использования
    print("🧪 Тестирование ChecklistLogger")
    
    # Логирование различных результатов
    log_success("Системные требования", "Python 3.9+", "Версия 3.11.0", 0.5)
    log_success("Системные требования", "Node.js", "Версия 18.0.0", 0.3)
    log_warning("Зависимости", "Backend venv", "Создано автоматически", 2.1)
    log_error("API", "Регистрация", "401 Unauthorized", "Проблема с JWT токенами", 1.5)
    log_critical("База данных", "Миграции", "Ошибка подключения к БД", "PostgreSQL недоступен", 5.0)
    
    # Генерация отчета
    report = logger.generate_report("test_report.md")
    print("\n📊 Отчет сгенерирован:")
    print(report) 