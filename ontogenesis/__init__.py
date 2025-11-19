"""
Ontogenesis Framework for OpenCog Organization

Self-generating, evolving kernels through recursive application of differential operators.
Implements the mathematical structures described in ONTOGENESIS.md agent specification.
"""

from .core import (
    KernelGenome,
    OntogeneticKernel,
    GeneratedKernel,
    initialize_ontogenetic_kernel,
    self_generate,
    self_optimize_kernel,
    self_reproduce
)

from .evolution import (
    OntogenesisConfig,
    EvolutionConfig,
    run_ontogenesis,
    evolve_population,
    evaluate_kernel_fitness
)

from .operators import (
    apply_chain_rule_kernel,
    apply_product_rule_kernel,
    apply_quotient_rule_kernel,
    crossover,
    mutate
)

from .kernels import (
    create_consciousness_kernel,
    create_physics_kernel,
    create_mathematics_kernel
)

__version__ = "1.0.0"
__all__ = [
    'KernelGenome',
    'OntogeneticKernel',
    'GeneratedKernel',
    'initialize_ontogenetic_kernel',
    'self_generate',
    'self_optimize_kernel',
    'self_reproduce',
    'OntogenesisConfig',
    'EvolutionConfig',
    'run_ontogenesis',
    'evolve_population',
    'evaluate_kernel_fitness',
    'apply_chain_rule_kernel',
    'apply_product_rule_kernel',
    'apply_quotient_rule_kernel',
    'crossover',
    'mutate',
    'create_consciousness_kernel',
    'create_physics_kernel',
    'create_mathematics_kernel'
]
