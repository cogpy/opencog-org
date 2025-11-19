"""
Differential operators for introspective cognition.

Implements mathematical operators as cognitive operations:
- Chain Rule: Recursive composition (understanding of understanding)
- Product Rule: Combining knowledge streams
- Quotient Rule: Refinement through constraints
"""

from typing import Dict, Any
import numpy as np


def apply_chain_rule(state: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply chain rule for recursive composition.
    
    (f∘g)' = f'(g(x)) · g'(x)
    
    Understanding of understanding - meta-cognition.
    
    Args:
        state: Current introspective state
        context: Additional context information
    
    Returns:
        Enhanced state with composed understanding
    """
    # Create enhanced state by composing with context
    enhanced = state.copy()
    
    if 'capabilities' in state:
        # Amplify capabilities through self-reflection
        for cap, value in state['capabilities'].items():
            # Chain: apply understanding to itself
            # f'(g(x)) * g'(x) approximated as value * (1 + value)
            enhanced['capabilities'][cap] = value * (1 + value * 0.1)
            enhanced['capabilities'][cap] = min(1.0, enhanced['capabilities'][cap])
    
    # Add meta-cognitive awareness
    enhanced['meta_level'] = state.get('meta_level', 0) + 1
    enhanced['introspection_depth'] = state.get('maturity', 0.5)
    
    return enhanced


def apply_product_rule(stream1: Dict[str, Any], stream2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply product rule for combining knowledge streams.
    
    (f·g)' = f'·g + f·g'
    
    Analysis and synthesis mutually inform each other.
    
    Args:
        stream1: First knowledge stream
        stream2: Second knowledge stream
    
    Returns:
        Combined knowledge with cross-pollination
    """
    combined = {}
    
    # Combine capabilities from both streams
    caps1 = stream1.get('capabilities', {})
    caps2 = stream2.get('capabilities', {})
    
    all_caps = set(caps1.keys()) | set(caps2.keys())
    combined['capabilities'] = {}
    
    for cap in all_caps:
        v1 = caps1.get(cap, 0.5)
        v2 = caps2.get(cap, 0.5)
        # Product rule: f'*g + f*g'
        # Approximate derivatives as values themselves
        combined['capabilities'][cap] = v1 * v2 + v1 * v2
        combined['capabilities'][cap] = min(1.0, combined['capabilities'][cap])
    
    # Combine other attributes
    combined['maturity'] = (stream1.get('maturity', 0.5) + stream2.get('maturity', 0.5)) / 2
    combined['stage'] = stream1.get('stage', 'embryonic')
    
    return combined


def apply_quotient_rule(solution: Dict[str, Any], constraints: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply quotient rule for refinement through constraints.
    
    (f/g)' = (f'·g - f·g') / g²
    
    Refining solutions within constraints.
    
    Args:
        solution: Proposed solution state
        constraints: Domain constraints
    
    Returns:
        Refined solution respecting constraints
    """
    refined = solution.copy()
    
    # Apply constraints as normalization
    constraint_weight = constraints.get('weight', 1.0)
    
    if 'capabilities' in solution:
        for cap, value in solution['capabilities'].items():
            # Quotient rule refinement
            # Normalize by constraint strength
            refined['capabilities'][cap] = value / (constraint_weight + 0.1)
            refined['capabilities'][cap] = min(1.0, refined['capabilities'][cap])
    
    # Add constraint awareness
    refined['constrained'] = True
    refined['constraint_satisfaction'] = 0.8
    
    return refined


def optimize_grip(state: Dict[str, Any], domain: str) -> Dict[str, Any]:
    """
    Optimize grip on problem domain.
    
    Grip measures how well current understanding matches domain requirements.
    Perfect grip → Perfect computation
    
    Args:
        state: Current cognitive state
        domain: Problem domain identifier
    
    Returns:
        State with optimized grip on domain
    """
    optimized = state.copy()
    
    # Domain-specific optimization
    domain_weights = _get_domain_weights(domain)
    
    if 'capabilities' in state:
        for cap, value in state['capabilities'].items():
            weight = domain_weights.get(cap, 1.0)
            # Amplify domain-relevant capabilities
            optimized['capabilities'][cap] = value * weight
            optimized['capabilities'][cap] = min(1.0, optimized['capabilities'][cap])
    
    # Calculate grip score
    if 'capabilities' in optimized:
        grip_score = np.mean(list(optimized['capabilities'].values()))
        optimized['grip'] = float(grip_score)
    
    optimized['domain'] = domain
    
    return optimized


def _get_domain_weights(domain: str) -> Dict[str, float]:
    """
    Get capability weights for specific domain.
    
    Different domains emphasize different capabilities.
    """
    domain_profiles = {
        'general': {
            'codeGeneration': 1.0,
            'debugging': 1.0,
            'refactoring': 1.0,
            'documentation': 1.0,
            'testing': 1.0,
            'architecture': 1.0
        },
        'research': {
            'codeGeneration': 0.7,
            'debugging': 0.8,
            'refactoring': 0.6,
            'documentation': 1.3,
            'testing': 0.9,
            'architecture': 1.2
        },
        'production': {
            'codeGeneration': 1.2,
            'debugging': 1.3,
            'refactoring': 1.1,
            'documentation': 1.0,
            'testing': 1.4,
            'architecture': 1.2
        },
        'prototype': {
            'codeGeneration': 1.4,
            'debugging': 0.9,
            'refactoring': 0.7,
            'documentation': 0.6,
            'testing': 0.8,
            'architecture': 1.1
        }
    }
    
    return domain_profiles.get(domain, domain_profiles['general'])
