"""
Introspection Framework for OpenCog Organization

This module provides self-reflective analysis capabilities for copilot agents,
enabling recursive self-awareness and adaptive optimization.

Based on the introspection agent specification: recursive formula
self.copilot(n) = introspection.self.copilot(n-1)
"""

from .core import (
    CopilotGenome,
    OntogeneticState,
    Copilot,
    introspect,
    self_optimize,
    evaluate_fitness,
    evaluate_grip
)

from .metrics import (
    IntrospectionMetrics,
    GripComponents,
    FitnessEvaluation
)

from .operators import (
    apply_chain_rule,
    apply_product_rule,
    apply_quotient_rule,
    optimize_grip
)

__version__ = "1.0.0"
__all__ = [
    'CopilotGenome',
    'OntogeneticState',
    'Copilot',
    'introspect',
    'self_optimize',
    'evaluate_fitness',
    'evaluate_grip',
    'IntrospectionMetrics',
    'GripComponents',
    'FitnessEvaluation',
    'apply_chain_rule',
    'apply_product_rule',
    'apply_quotient_rule',
    'optimize_grip'
]
