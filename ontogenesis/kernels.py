"""
Pre-defined kernel generators for specific domains.
"""

import numpy as np
from .core import GeneratedKernel, OntogeneticKernel, KernelGenome, initialize_ontogenetic_kernel


def create_consciousness_kernel(order: int = 4) -> OntogeneticKernel:
    """
    Create kernel optimized for consciousness-related computations.
    
    Emphasizes recursive self-reference and meta-cognitive operations.
    
    Args:
        order: Order of the kernel
    
    Returns:
        Consciousness-optimized ontogenetic kernel
    """
    # Coefficients emphasizing recursion
    coeffs = [0.25, 0.35, 0.45, 0.55][:order]
    
    kernel = GeneratedKernel(
        order=order,
        coefficients=coeffs,
        domain="consciousness",
        properties={
            'recursive_depth': 'high',
            'self_reference': True,
            'meta_cognitive': True
        }
    )
    
    onto_kernel = initialize_ontogenetic_kernel(kernel, order)
    onto_kernel.base_kernel.properties['specialization'] = 'consciousness'
    
    return onto_kernel


def create_physics_kernel(order: int = 4) -> OntogeneticKernel:
    """
    Create kernel optimized for physics simulations.
    
    Emphasizes energy conservation and symmetry preservation.
    
    Args:
        order: Order of the kernel
    
    Returns:
        Physics-optimized ontogenetic kernel
    """
    # Symplectic-friendly coefficients
    coeffs = [0.20, 0.30, 0.40, 0.50][:order]
    
    kernel = GeneratedKernel(
        order=order,
        coefficients=coeffs,
        domain="physics",
        properties={
            'symplectic': True,
            'energy_conserving': True,
            'time_reversible': True
        }
    )
    
    onto_kernel = initialize_ontogenetic_kernel(kernel, order)
    onto_kernel.base_kernel.properties['specialization'] = 'physics'
    
    return onto_kernel


def create_mathematics_kernel(order: int = 4) -> OntogeneticKernel:
    """
    Create kernel optimized for pure mathematics.
    
    Emphasizes precision and convergence properties.
    
    Args:
        order: Order of the kernel
    
    Returns:
        Mathematics-optimized ontogenetic kernel
    """
    # High-precision coefficients
    coeffs = [0.15, 0.25, 0.35, 0.45][:order]
    
    kernel = GeneratedKernel(
        order=order,
        coefficients=coeffs,
        domain="mathematics",
        properties={
            'high_precision': True,
            'convergent': True,
            'stable': True
        }
    )
    
    onto_kernel = initialize_ontogenetic_kernel(kernel, order)
    onto_kernel.base_kernel.properties['specialization'] = 'mathematics'
    
    return onto_kernel


def create_general_purpose_kernel(order: int = 4) -> OntogeneticKernel:
    """
    Create balanced general-purpose kernel.
    
    Args:
        order: Order of the kernel
    
    Returns:
        General-purpose ontogenetic kernel
    """
    # Balanced coefficients
    coeffs = np.linspace(0.2, 0.6, order).tolist()
    
    kernel = GeneratedKernel(
        order=order,
        coefficients=coeffs,
        domain="general",
        properties={
            'balanced': True,
            'versatile': True
        }
    )
    
    onto_kernel = initialize_ontogenetic_kernel(kernel, order)
    onto_kernel.base_kernel.properties['specialization'] = 'general'
    
    return onto_kernel
