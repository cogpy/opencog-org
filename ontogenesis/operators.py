"""
Differential operators for kernel reproduction and transformation.
"""

from typing import Tuple
import numpy as np

from .core import OntogeneticKernel, KernelGene, GeneType


def apply_chain_rule_kernel(kernel: OntogeneticKernel) -> OntogeneticKernel:
    """
    Apply chain rule for self-composition.
    
    (f∘f)' = f'(f(x)) · f'(x)
    
    Args:
        kernel: Input kernel
    
    Returns:
        Composed kernel
    """
    coeffs = np.array(kernel.base_kernel.coefficients)
    
    # Chain rule composition
    composed_coeffs = coeffs * (1 + coeffs * 0.15)
    composed_coeffs = np.clip(composed_coeffs, 0.01, 1.0)
    
    kernel.base_kernel.coefficients = composed_coeffs.tolist()
    return kernel


def apply_product_rule_kernel(kernel1: OntogeneticKernel,
                              kernel2: OntogeneticKernel) -> OntogeneticKernel:
    """
    Apply product rule for combining kernels.
    
    (f·g)' = f'·g + f·g'
    
    Args:
        kernel1: First kernel
        kernel2: Second kernel
    
    Returns:
        Combined kernel
    """
    coeffs1 = np.array(kernel1.base_kernel.coefficients)
    coeffs2 = np.array(kernel2.base_kernel.coefficients)
    
    # Ensure same length
    max_len = max(len(coeffs1), len(coeffs2))
    if len(coeffs1) < max_len:
        coeffs1 = np.pad(coeffs1, (0, max_len - len(coeffs1)), constant_values=0.5)
    if len(coeffs2) < max_len:
        coeffs2 = np.pad(coeffs2, (0, max_len - len(coeffs2)), constant_values=0.5)
    
    # Product rule
    combined_coeffs = coeffs1 * coeffs2 + coeffs1 * coeffs2
    combined_coeffs = np.clip(combined_coeffs, 0.01, 1.0)
    
    kernel1.base_kernel.coefficients = combined_coeffs.tolist()
    return kernel1


def apply_quotient_rule_kernel(kernel: OntogeneticKernel,
                               constraint_weight: float = 1.0) -> OntogeneticKernel:
    """
    Apply quotient rule for refinement.
    
    (f/g)' = (f'·g - f·g') / g²
    
    Args:
        kernel: Input kernel
        constraint_weight: Constraint strength
    
    Returns:
        Refined kernel
    """
    coeffs = np.array(kernel.base_kernel.coefficients)
    
    # Quotient rule refinement
    refined_coeffs = coeffs / (constraint_weight + 0.1)
    refined_coeffs = np.clip(refined_coeffs, 0.01, 1.0)
    
    kernel.base_kernel.coefficients = refined_coeffs.tolist()
    return kernel


def crossover(parent1: OntogeneticKernel,
             parent2: OntogeneticKernel,
             point: Optional[int] = None) -> Tuple[OntogeneticKernel, OntogeneticKernel]:
    """
    Single-point crossover for genetic recombination.
    
    Args:
        parent1: First parent
        parent2: Second parent
        point: Crossover point (random if None)
    
    Returns:
        Two offspring kernels
    """
    coeffs1 = np.array(parent1.base_kernel.coefficients)
    coeffs2 = np.array(parent2.base_kernel.coefficients)
    
    # Determine crossover point
    min_len = min(len(coeffs1), len(coeffs2))
    if point is None:
        point = np.random.randint(1, min_len)
    
    # Create offspring
    offspring1_coeffs = np.concatenate([coeffs1[:point], coeffs2[point:min_len]])
    offspring2_coeffs = np.concatenate([coeffs2[:point], coeffs1[point:min_len]])
    
    # Create offspring kernels
    from .core import GeneratedKernel, KernelGenome
    
    offspring1 = OntogeneticKernel(
        base_kernel=GeneratedKernel(
            order=len(offspring1_coeffs),
            coefficients=offspring1_coeffs.tolist(),
            domain=parent1.base_kernel.domain
        ),
        genome=KernelGenome(
            generation=max(parent1.genome.generation, parent2.genome.generation) + 1,
            lineage=[parent1.genome.id, parent2.genome.id]
        )
    )
    
    offspring2 = OntogeneticKernel(
        base_kernel=GeneratedKernel(
            order=len(offspring2_coeffs),
            coefficients=offspring2_coeffs.tolist(),
            domain=parent2.base_kernel.domain
        ),
        genome=KernelGenome(
            generation=max(parent1.genome.generation, parent2.genome.generation) + 1,
            lineage=[parent1.genome.id, parent2.genome.id]
        )
    )
    
    return offspring1, offspring2


def mutate(kernel: OntogeneticKernel, rate: float = 0.1) -> None:
    """
    Apply random mutation to kernel.
    
    Args:
        kernel: Kernel to mutate
        rate: Mutation probability per gene
    """
    # Mutate genes
    for gene in kernel.genome.genes:
        gene.mutate(rate=rate)
    
    # Mutate coefficients
    coeffs = np.array(kernel.base_kernel.coefficients)
    
    for i in range(len(coeffs)):
        if np.random.random() < rate:
            # Gaussian mutation
            coeffs[i] += np.random.randn() * 0.15
            coeffs[i] = np.clip(coeffs[i], 0.01, 1.0)
    
    kernel.base_kernel.coefficients = coeffs.tolist()


# For compatibility with import
from typing import Optional
