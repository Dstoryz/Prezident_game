from datetime import datetime
from typing import Dict, List

class AgentPerformanceMetrics:
    def __init__(self):
        self.metrics = {
            'tasks_completed': 0,
            'tasks_failed': 0,
            'response_time': 0,
            'quality_score': 0,
            'collaboration_score': 0
        }
    
    def calculate_efficiency(self, agent_name: str) -> float:
        """Расчет эффективности агента"""
        completed = self.metrics['tasks_completed']
        failed = self.metrics['tasks_failed']
        total = completed + failed
        
        if total == 0:
            return 0.0
        
        success_rate = completed / total
        quality_bonus = self.metrics['quality_score'] * 0.2
        collaboration_bonus = self.metrics['collaboration_score'] * 0.1
        
        return min(1.0, success_rate + quality_bonus + collaboration_bonus)
    
    def identify_bottlenecks(self) -> List[str]:
        """Выявление узких мест"""
        bottlenecks = []
        
        if self.metrics['response_time'] > 300:  # 5 минут
            bottlenecks.append("Медленная реакция агентов")
        
        if self.metrics['tasks_failed'] > self.metrics['tasks_completed'] * 0.2:
            bottlenecks.append("Высокий процент неудачных задач")
        
        if self.metrics['quality_score'] < 0.7:
            bottlenecks.append("Низкое качество работы")
        
        return bottlenecks
