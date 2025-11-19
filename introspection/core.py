"""
Core introspection functionality implementing recursive self-awareness.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum
import numpy as np


class DevelopmentStage(Enum):
    """Ontogenetic development stages."""
    EMBRYONIC = "embryonic"
    JUVENILE = "juvenile"
    MATURE = "mature"
    SENESCENT = "senescent"


@dataclass
class CopilotGenome:
    """
    The "DNA" of the copilot agent.
    
    Capabilities represent proficiency levels in various domains.
    Genetic weights influence behavior and learning.
    """
    capabilities: Dict[str, float] = field(default_factory=lambda: {
        'codeGeneration': 0.7,
        'debugging': 0.6,
        'refactoring': 0.5,
        'documentation': 0.6,
        'testing': 0.5,
        'architecture': 0.4
    })
    
    operatorGenes: Dict[str, float] = field(default_factory=lambda: {
        'chainRule': 0.8,      # Recursive composition ability
        'productRule': 0.7,    # Combining insights
        'quotientRule': 0.6    # Refinement through division
    })
    
    cognitivePrimitives: Dict[str, float] = field(default_factory=lambda: {
        'analysis': 0.7,
        'synthesis': 0.6,
        'abstraction': 0.5,
        'concretization': 0.6
    })
    
    generation: int = 0
    lineage: List[str] = field(default_factory=list)
    fitness: float = 0.0


@dataclass
class OntogeneticState:
    """
    Current developmental state of the copilot.
    """
    stage: DevelopmentStage = DevelopmentStage.EMBRYONIC
    maturity: float = 0.0  # 0.0 to 1.0
    age: int = 0  # Iterations
    development_history: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class Copilot:
    """
    Self-aware copilot with introspective capabilities.
    """
    genome: CopilotGenome = field(default_factory=CopilotGenome)
    ontogenetic_state: OntogeneticState = field(default_factory=OntogeneticState)
    context: Dict[str, Any] = field(default_factory=dict)
    domain: str = "general"
    
    # Performance metrics
    tests_passing: int = 0
    total_tests: int = 0
    lint_errors: int = 0
    documentation_coverage: float = 0.0
    iterations_to_solution: int = 0
    redundant_operations: int = 0
    total_operations: int = 0


def introspect(copilot: Copilot, depth: int = 1) -> Dict[str, Any]:
    """
    Recursive introspection: understand understanding.
    
    Implements: self.copilot(n) = introspection.self.copilot(n-1)
    
    Args:
        copilot: The copilot instance to introspect
        depth: Recursion depth (how many levels of meta-cognition)
    
    Returns:
        Introspective analysis of current state
    """
    if depth == 0:
        # Base case: return current capabilities
        return {
            'capabilities': copilot.genome.capabilities.copy(),
            'stage': copilot.ontogenetic_state.stage.value,
            'maturity': copilot.ontogenetic_state.maturity
        }
    
    # Recursive case: introspect on previous introspection
    previous = introspect(copilot, depth - 1)
    
    # Apply chain rule: understand(understand(state))
    from .operators import apply_chain_rule
    current = apply_chain_rule(previous, copilot.context)
    
    # Optimize grip on problem
    from .operators import optimize_grip
    optimized = optimize_grip(current, copilot.domain)
    
    return optimized


def self_optimize(copilot: Copilot, iterations: int = 5, learning_rate: float = 0.01) -> None:
    """
    Self-optimization through gradient ascent on grip function.
    
    Args:
        copilot: The copilot to optimize
        iterations: Number of optimization cycles
        learning_rate: Rate of capability adjustment
    """
    for i in range(iterations):
        # Evaluate current grip
        grip = evaluate_grip(copilot)
        
        # Compute gradient (simplified: based on current performance)
        gradient = _compute_grip_gradient(copilot)
        
        # Update capabilities via gradient ascent
        for capability in copilot.genome.capabilities:
            copilot.genome.capabilities[capability] += learning_rate * gradient.get(capability, 0)
            # Clamp to [0, 1]
            copilot.genome.capabilities[capability] = max(0.0, min(1.0, 
                copilot.genome.capabilities[capability]))
        
        # Progress development
        copilot.ontogenetic_state.maturity = min(1.0, 
            copilot.ontogenetic_state.maturity + 0.1)
        copilot.ontogenetic_state.age += 1
        
        # Update development stage based on maturity
        _update_development_stage(copilot)
        
        # Record development event
        copilot.ontogenetic_state.development_history.append({
            'iteration': i,
            'grip': grip,
            'stage': copilot.ontogenetic_state.stage.value,
            'maturity': copilot.ontogenetic_state.maturity
        })


def evaluate_grip(copilot: Copilot) -> float:
    """
    Evaluate the copilot's "grip" on the problem domain.
    
    Grip = understanding * 0.3 + correctness * 0.3 + efficiency * 0.2 +
           completeness * 0.1 + elegance * 0.1
    
    Returns:
        Grip score between 0 and 1
    """
    # Understanding: average of cognitive primitives
    understanding = np.mean(list(copilot.genome.cognitivePrimitives.values()))
    
    # Correctness: based on test passage
    correctness = (copilot.tests_passing / copilot.total_tests 
                   if copilot.total_tests > 0 else 0.5)
    
    # Efficiency: based on operations
    efficiency = (1.0 - (copilot.redundant_operations / copilot.total_operations)
                  if copilot.total_operations > 0 else 0.5)
    
    # Completeness: based on maturity
    completeness = copilot.ontogenetic_state.maturity
    
    # Elegance: based on documentation and low lint errors
    elegance = copilot.documentation_coverage * (1.0 - min(1.0, copilot.lint_errors / 100.0))
    
    grip = (understanding * 0.3 + 
            correctness * 0.3 + 
            efficiency * 0.2 + 
            completeness * 0.1 + 
            elegance * 0.1)
    
    return float(grip)


def evaluate_fitness(copilot: Copilot, population: Optional[List[Copilot]] = None) -> float:
    """
    Comprehensive fitness evaluation.
    
    Args:
        copilot: The copilot to evaluate
        population: Optional population for novelty calculation
    
    Returns:
        Fitness score between 0 and 1
    """
    # Task completion metrics
    task_success = (copilot.tests_passing / copilot.total_tests 
                    if copilot.total_tests > 0 else 0.5)
    
    # Code quality metrics
    code_quality = ((1.0 - min(1.0, copilot.lint_errors / 100.0)) * 
                    copilot.documentation_coverage)
    
    # Efficiency metrics
    efficiency = ((1.0 / max(1, copilot.iterations_to_solution)) * 
                  (1.0 - (copilot.redundant_operations / 
                          max(1, copilot.total_operations))))
    
    # Novelty (genetic diversity)
    novelty = _genetic_diversity(copilot, population) if population else 0.5
    
    # Weighted combination
    fitness = (task_success * 0.4 + 
               code_quality * 0.3 + 
               efficiency * 0.2 + 
               novelty * 0.1)
    
    copilot.genome.fitness = fitness
    return float(fitness)


def _compute_grip_gradient(copilot: Copilot) -> Dict[str, float]:
    """
    Compute gradient for grip optimization.
    
    Simplified gradient based on current performance gaps.
    """
    gradient = {}
    
    # If tests are failing, increase debugging capability
    if copilot.tests_passing < copilot.total_tests:
        gradient['debugging'] = 0.1
        gradient['codeGeneration'] = 0.05
    
    # If lint errors exist, increase refactoring
    if copilot.lint_errors > 0:
        gradient['refactoring'] = 0.08
    
    # If documentation is low, increase documentation capability
    if copilot.documentation_coverage < 0.7:
        gradient['documentation'] = 0.07
    
    # Always improve architecture understanding
    gradient['architecture'] = 0.03
    
    return gradient


def _update_development_stage(copilot: Copilot) -> None:
    """Update development stage based on maturity."""
    maturity = copilot.ontogenetic_state.maturity
    
    if maturity < 0.25:
        copilot.ontogenetic_state.stage = DevelopmentStage.EMBRYONIC
    elif maturity < 0.6:
        copilot.ontogenetic_state.stage = DevelopmentStage.JUVENILE
    elif maturity < 0.9:
        copilot.ontogenetic_state.stage = DevelopmentStage.MATURE
    else:
        copilot.ontogenetic_state.stage = DevelopmentStage.SENESCENT


def _genetic_diversity(copilot: Copilot, population: Optional[List[Copilot]]) -> float:
    """
    Calculate genetic diversity relative to population.
    
    Returns average distance from population.
    """
    if not population or len(population) <= 1:
        return 0.5
    
    # Calculate Euclidean distance in capability space
    distances = []
    for other in population:
        if other is copilot:
            continue
        
        dist = 0.0
        for cap in copilot.genome.capabilities:
            diff = copilot.genome.capabilities[cap] - other.genome.capabilities.get(cap, 0)
            dist += diff ** 2
        
        distances.append(np.sqrt(dist))
    
    # Return normalized average distance
    avg_dist = np.mean(distances) if distances else 0.5
    return min(1.0, avg_dist)
