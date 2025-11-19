"""
Core ontogenesis functionality for self-generating kernels.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum
import uuid
import numpy as np


class DevelopmentStage(Enum):
    """Life stages of ontogenetic kernels."""
    EMBRYONIC = "embryonic"
    JUVENILE = "juvenile"
    MATURE = "mature"
    SENESCENT = "senescent"


class GeneType(Enum):
    """Types of kernel genes."""
    COEFFICIENT = "coefficient"  # Mutable B-series coefficients
    OPERATOR = "operator"         # Mutable differential operators
    SYMMETRY = "symmetry"         # Immutable symmetry preservers
    PRESERVATION = "preservation" # Immutable conserved quantities


@dataclass
class KernelGene:
    """Individual gene in kernel genome."""
    gene_type: GeneType
    name: str
    value: float
    mutable: bool = True
    
    def mutate(self, rate: float = 0.1) -> None:
        """Mutate gene value if mutable."""
        if self.mutable and np.random.random() < rate:
            # Gaussian mutation
            self.value += np.random.randn() * 0.2
            self.value = max(0.0, min(1.0, self.value))


@dataclass
class KernelGenome:
    """
    The "DNA" of a kernel.
    
    Contains genetic information for B-series coefficients and operators.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    generation: int = 0
    lineage: List[str] = field(default_factory=list)
    genes: List[KernelGene] = field(default_factory=list)
    fitness: float = 0.0
    age: int = 0
    
    def __post_init__(self):
        if not self.genes:
            # Initialize with default genes
            self._initialize_default_genes()
    
    def _initialize_default_genes(self):
        """Initialize default gene set."""
        # B-series coefficient genes (order 4)
        # Following A000081 sequence: 1, 1, 2, 4
        for i in range(4):
            self.genes.append(KernelGene(
                gene_type=GeneType.COEFFICIENT,
                name=f"b{i+1}",
                value=np.random.uniform(0.3, 0.9),
                mutable=True
            ))
        
        # Operator genes
        for op in ['chain', 'product', 'quotient']:
            self.genes.append(KernelGene(
                gene_type=GeneType.OPERATOR,
                name=op,
                value=np.random.uniform(0.5, 1.0),
                mutable=True
            ))
    
    def get_coefficients(self) -> List[float]:
        """Extract B-series coefficients."""
        return [g.value for g in self.genes if g.gene_type == GeneType.COEFFICIENT]
    
    def get_operator_weights(self) -> Dict[str, float]:
        """Extract operator weights."""
        return {g.name: g.value for g in self.genes if g.gene_type == GeneType.OPERATOR}


@dataclass
class GeneratedKernel:
    """Base kernel structure."""
    order: int
    coefficients: List[float]
    domain: str = "general"
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OntogeneticKernel:
    """
    Kernel with ontogenetic capabilities.
    
    Can self-generate, self-optimize, and reproduce.
    """
    base_kernel: GeneratedKernel
    genome: KernelGenome = field(default_factory=KernelGenome)
    development_stage: DevelopmentStage = DevelopmentStage.EMBRYONIC
    maturity: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'genome_id': self.genome.id,
            'generation': self.genome.generation,
            'order': self.base_kernel.order,
            'coefficients': self.base_kernel.coefficients,
            'domain': self.base_kernel.domain,
            'stage': self.development_stage.value,
            'maturity': self.maturity,
            'fitness': self.genome.fitness
        }


def initialize_ontogenetic_kernel(kernel: Optional[GeneratedKernel] = None, 
                                  order: int = 4) -> OntogeneticKernel:
    """
    Initialize a kernel with ontogenetic capabilities.
    
    Args:
        kernel: Base kernel (if None, creates default)
        order: Order of the kernel
    
    Returns:
        Ontogenetic kernel ready for evolution
    """
    if kernel is None:
        # Create default kernel
        coeffs = np.random.uniform(0.1, 0.5, order).tolist()
        kernel = GeneratedKernel(
            order=order,
            coefficients=coeffs,
            domain="general"
        )
    
    genome = KernelGenome(generation=0)
    
    return OntogeneticKernel(
        base_kernel=kernel,
        genome=genome,
        development_stage=DevelopmentStage.EMBRYONIC,
        maturity=0.0
    )


def self_generate(parent: OntogeneticKernel) -> OntogeneticKernel:
    """
    Kernel generates offspring through recursive self-composition.
    
    Applies chain rule: (f∘f)' = f'(f(x)) · f'(x)
    
    Args:
        parent: Parent kernel
    
    Returns:
        Offspring kernel
    """
    # Create offspring genome
    offspring_genome = KernelGenome(
        generation=parent.genome.generation + 1,
        lineage=parent.genome.lineage + [parent.genome.id]
    )
    
    # Copy and mutate genes
    for parent_gene in parent.genome.genes:
        offspring_gene = KernelGene(
            gene_type=parent_gene.gene_type,
            name=parent_gene.name,
            value=parent_gene.value,
            mutable=parent_gene.mutable
        )
        offspring_gene.mutate(rate=0.1)
        offspring_genome.genes.append(offspring_gene)
    
    # Apply chain rule to coefficients
    parent_coeffs = np.array(parent.base_kernel.coefficients)
    # f'(f(x)) * f'(x) approximated as composition
    offspring_coeffs = parent_coeffs * (1 + parent_coeffs * 0.1)
    offspring_coeffs = np.clip(offspring_coeffs, 0.01, 1.0)
    
    offspring_kernel = GeneratedKernel(
        order=parent.base_kernel.order,
        coefficients=offspring_coeffs.tolist(),
        domain=parent.base_kernel.domain
    )
    
    return OntogeneticKernel(
        base_kernel=offspring_kernel,
        genome=offspring_genome,
        development_stage=DevelopmentStage.EMBRYONIC,
        maturity=0.0
    )


def self_optimize_kernel(kernel: OntogeneticKernel, iterations: int = 5) -> None:
    """
    Kernel optimizes itself through grip improvement.
    
    Args:
        kernel: Kernel to optimize
        iterations: Number of optimization cycles
    """
    for i in range(iterations):
        # Evaluate current grip
        grip = _evaluate_kernel_grip(kernel)
        
        # Compute gradient
        gradient = _compute_kernel_gradient(kernel)
        
        # Update coefficients
        coeffs = np.array(kernel.base_kernel.coefficients)
        coeffs += 0.01 * gradient
        coeffs = np.clip(coeffs, 0.01, 1.0)
        kernel.base_kernel.coefficients = coeffs.tolist()
        
        # Progress maturity
        kernel.maturity = min(1.0, kernel.maturity + 0.1)
        kernel.genome.age += 1
        
        # Update development stage
        _update_kernel_stage(kernel)


def self_reproduce(parent1: OntogeneticKernel, 
                   parent2: OntogeneticKernel,
                   method: str = 'crossover') -> OntogeneticKernel:
    """
    Two kernels reproduce to create offspring.
    
    Args:
        parent1: First parent
        parent2: Second parent
        method: Reproduction method ('crossover', 'mutation', 'cloning')
    
    Returns:
        Offspring kernel
    """
    if method == 'crossover':
        return _crossover_kernels(parent1, parent2)
    elif method == 'mutation':
        offspring = self_generate(parent1)
        # Apply additional mutation
        for gene in offspring.genome.genes:
            gene.mutate(rate=0.2)
        return offspring
    elif method == 'cloning':
        return self_generate(parent1)
    else:
        raise ValueError(f"Unknown reproduction method: {method}")


def _crossover_kernels(parent1: OntogeneticKernel, 
                       parent2: OntogeneticKernel) -> OntogeneticKernel:
    """Perform genetic crossover between two kernels."""
    # Create offspring genome
    offspring_genome = KernelGenome(
        generation=max(parent1.genome.generation, parent2.genome.generation) + 1,
        lineage=[parent1.genome.id, parent2.genome.id]
    )
    
    # Single-point crossover
    crossover_point = len(parent1.genome.genes) // 2
    
    for i in range(len(parent1.genome.genes)):
        if i < crossover_point:
            source_gene = parent1.genome.genes[i]
        else:
            # Handle different lengths
            idx = i if i < len(parent2.genome.genes) else i % len(parent2.genome.genes)
            source_gene = parent2.genome.genes[idx]
        
        offspring_gene = KernelGene(
            gene_type=source_gene.gene_type,
            name=source_gene.name,
            value=source_gene.value,
            mutable=source_gene.mutable
        )
        offspring_genome.genes.append(offspring_gene)
    
    # Combine coefficients
    coeffs1 = np.array(parent1.base_kernel.coefficients)
    coeffs2 = np.array(parent2.base_kernel.coefficients)
    
    # Average with some noise
    offspring_coeffs = (coeffs1 + coeffs2) / 2.0
    offspring_coeffs += np.random.randn(len(offspring_coeffs)) * 0.05
    offspring_coeffs = np.clip(offspring_coeffs, 0.01, 1.0)
    
    offspring_kernel = GeneratedKernel(
        order=parent1.base_kernel.order,
        coefficients=offspring_coeffs.tolist(),
        domain=parent1.base_kernel.domain
    )
    
    return OntogeneticKernel(
        base_kernel=offspring_kernel,
        genome=offspring_genome,
        development_stage=DevelopmentStage.EMBRYONIC,
        maturity=0.0
    )


def _evaluate_kernel_grip(kernel: OntogeneticKernel) -> float:
    """Evaluate kernel's grip on domain."""
    # Simplified grip: based on coefficient quality and maturity
    coeffs = np.array(kernel.base_kernel.coefficients)
    
    # Prefer moderate, balanced coefficients
    optimal_range = (coeffs > 0.1) & (coeffs < 0.9)
    quality = np.mean(optimal_range)
    
    # Combine with maturity
    grip = quality * 0.6 + kernel.maturity * 0.4
    
    return float(grip)


def _compute_kernel_gradient(kernel: OntogeneticKernel) -> np.ndarray:
    """Compute gradient for kernel optimization."""
    coeffs = np.array(kernel.base_kernel.coefficients)
    
    # Move coefficients toward optimal range
    gradient = np.zeros_like(coeffs)
    
    for i, c in enumerate(coeffs):
        if c < 0.3:
            gradient[i] = 0.1  # Increase
        elif c > 0.7:
            gradient[i] = -0.1  # Decrease
        else:
            gradient[i] = 0.02  # Small positive nudge
    
    return gradient


def _update_kernel_stage(kernel: OntogeneticKernel) -> None:
    """Update kernel development stage based on maturity."""
    if kernel.maturity < 0.25:
        kernel.development_stage = DevelopmentStage.EMBRYONIC
    elif kernel.maturity < 0.6:
        kernel.development_stage = DevelopmentStage.JUVENILE
    elif kernel.maturity < 0.9:
        kernel.development_stage = DevelopmentStage.MATURE
    else:
        kernel.development_stage = DevelopmentStage.SENESCENT
