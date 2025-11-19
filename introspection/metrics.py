"""
Metrics and measurement systems for introspection.
"""

from dataclasses import dataclass
from typing import Dict, List
import numpy as np


@dataclass
class GripComponents:
    """
    Components of the grip function.
    
    Grip measures how well the copilot's capabilities match domain requirements.
    """
    understanding: float  # Depth of problem comprehension
    correctness: float    # Solution accuracy
    efficiency: float     # Implementation quality
    completeness: float   # Coverage of requirements
    elegance: float       # Code quality and clarity
    
    def total_grip(self) -> float:
        """Calculate total grip score."""
        return (
            self.understanding * 0.3 +
            self.correctness * 0.3 +
            self.efficiency * 0.2 +
            self.completeness * 0.1 +
            self.elegance * 0.1
        )


@dataclass
class FitnessEvaluation:
    """
    Comprehensive fitness evaluation results.
    """
    task_success: float    # Task completion metric
    code_quality: float    # Code quality metric
    efficiency: float      # Efficiency metric
    novelty: float         # Genetic diversity metric
    
    overall_fitness: float
    
    @classmethod
    def calculate(cls, task_success: float, code_quality: float, 
                  efficiency: float, novelty: float) -> 'FitnessEvaluation':
        """Calculate fitness from components."""
        overall = (
            task_success * 0.4 +
            code_quality * 0.3 +
            efficiency * 0.2 +
            novelty * 0.1
        )
        
        return cls(
            task_success=task_success,
            code_quality=code_quality,
            efficiency=efficiency,
            novelty=novelty,
            overall_fitness=overall
        )


class IntrospectionMetrics:
    """
    Tracks and analyzes introspection metrics over time.
    """
    
    def __init__(self):
        self.history: List[Dict[str, float]] = []
        self.grip_history: List[float] = []
        self.fitness_history: List[float] = []
    
    def record_iteration(self, grip: float, fitness: float, 
                        capabilities: Dict[str, float]) -> None:
        """Record metrics for an iteration."""
        self.grip_history.append(grip)
        self.fitness_history.append(fitness)
        
        record = {
            'grip': grip,
            'fitness': fitness,
            **capabilities
        }
        self.history.append(record)
    
    def get_improvement_rate(self) -> float:
        """Calculate rate of improvement over time."""
        if len(self.grip_history) < 2:
            return 0.0
        
        # Linear regression slope
        x = np.arange(len(self.grip_history))
        y = np.array(self.grip_history)
        
        # Simple slope calculation
        if len(x) > 1:
            slope = (y[-1] - y[0]) / (x[-1] - x[0])
            return float(slope)
        
        return 0.0
    
    def get_convergence_status(self, threshold: float = 0.9) -> bool:
        """Check if metrics have converged to target."""
        if len(self.grip_history) < 3:
            return False
        
        recent_grips = self.grip_history[-3:]
        return all(g >= threshold for g in recent_grips)
    
    def get_statistics(self) -> Dict[str, float]:
        """Get statistical summary of metrics."""
        if not self.grip_history:
            return {
                'mean_grip': 0.0,
                'max_grip': 0.0,
                'min_grip': 0.0,
                'std_grip': 0.0,
                'improvement_rate': 0.0,
                'converged': False
            }
        
        return {
            'mean_grip': float(np.mean(self.grip_history)),
            'max_grip': float(np.max(self.grip_history)),
            'min_grip': float(np.min(self.grip_history)),
            'std_grip': float(np.std(self.grip_history)),
            'improvement_rate': self.get_improvement_rate(),
            'converged': self.get_convergence_status()
        }
    
    def get_capability_trends(self) -> Dict[str, List[float]]:
        """Get trend data for each capability."""
        if not self.history:
            return {}
        
        # Extract capability names
        first_record = self.history[0]
        capability_names = [k for k in first_record.keys() 
                           if k not in ['grip', 'fitness']]
        
        trends = {}
        for cap in capability_names:
            trends[cap] = [record.get(cap, 0.0) for record in self.history]
        
        return trends
