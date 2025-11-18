"""
Evolution framework for ontogenetic kernels.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Callable, Optional
import numpy as np

from .core import OntogeneticKernel, initialize_ontogenetic_kernel, self_reproduce, self_optimize_kernel


@dataclass
class EvolutionConfig:
    """Configuration for evolutionary process."""
    population_size: int = 20
    mutation_rate: float = 0.15
    crossover_rate: float = 0.8
    elitism_rate: float = 0.1
    max_generations: int = 50
    fitness_threshold: float = 0.9
    diversity_pressure: float = 0.2


@dataclass
class OntogenesisConfig:
    """Complete ontogenesis configuration."""
    evolution: EvolutionConfig = field(default_factory=EvolutionConfig)
    seed_kernels: List[OntogeneticKernel] = field(default_factory=list)
    fitness_function: Optional[Callable] = None


@dataclass
class GenerationResult:
    """Results from one generation of evolution."""
    generation: int
    population: List[OntogeneticKernel]
    best_fitness: float
    average_fitness: float
    diversity: float
    best_kernel: OntogeneticKernel


def run_ontogenesis(config: OntogenesisConfig) -> List[GenerationResult]:
    """
    Run complete ontogenesis evolution process.
    
    Args:
        config: Ontogenesis configuration
    
    Returns:
        List of generation results
    """
    # Initialize population
    if config.seed_kernels:
        population = config.seed_kernels
    else:
        population = [initialize_ontogenetic_kernel() 
                     for _ in range(config.evolution.population_size)]
    
    results = []
    
    for gen in range(config.evolution.max_generations):
        # Evaluate fitness
        fitnesses = [evaluate_kernel_fitness(k, population, config.fitness_function) 
                    for k in population]
        
        # Record generation results
        best_idx = np.argmax(fitnesses)
        best_fitness = fitnesses[best_idx]
        avg_fitness = np.mean(fitnesses)
        diversity = calculate_population_diversity(population)
        
        gen_result = GenerationResult(
            generation=gen,
            population=population.copy(),
            best_fitness=best_fitness,
            average_fitness=avg_fitness,
            diversity=diversity,
            best_kernel=population[best_idx]
        )
        results.append(gen_result)
        
        # Check convergence
        if best_fitness >= config.evolution.fitness_threshold:
            print(f"Converged at generation {gen} with fitness {best_fitness:.4f}")
            break
        
        # Evolve to next generation
        population = evolve_population(
            population, 
            fitnesses, 
            config.evolution
        )
    
    return results


def evolve_population(population: List[OntogeneticKernel],
                     fitnesses: List[float],
                     config: EvolutionConfig) -> List[OntogeneticKernel]:
    """
    Evolve population to next generation.
    
    Args:
        population: Current population
        fitnesses: Fitness scores
        config: Evolution configuration
    
    Returns:
        Next generation population
    """
    next_generation = []
    
    # Elitism: keep best individuals
    num_elite = int(len(population) * config.elitism_rate)
    elite_indices = np.argsort(fitnesses)[-num_elite:]
    for idx in elite_indices:
        next_generation.append(population[idx])
    
    # Generate offspring
    while len(next_generation) < len(population):
        # Tournament selection
        parent1 = tournament_selection(population, fitnesses)
        parent2 = tournament_selection(population, fitnesses)
        
        # Reproduction
        if np.random.random() < config.crossover_rate:
            offspring = self_reproduce(parent1, parent2, method='crossover')
        else:
            offspring = self_reproduce(parent1, parent2, method='mutation')
        
        # Mutation
        if np.random.random() < config.mutation_rate:
            for gene in offspring.genome.genes:
                gene.mutate(rate=config.mutation_rate)
        
        next_generation.append(offspring)
    
    # Trim to population size
    next_generation = next_generation[:len(population)]
    
    # Optimize mature individuals
    for kernel in next_generation:
        if kernel.maturity > 0.5:
            self_optimize_kernel(kernel, iterations=2)
    
    # Update development stages
    for kernel in next_generation:
        kernel.genome.age += 1
        if kernel.genome.age % 5 == 0:
            kernel.maturity = min(1.0, kernel.maturity + 0.1)
    
    return next_generation


def evaluate_kernel_fitness(kernel: OntogeneticKernel,
                           population: List[OntogeneticKernel],
                           custom_fitness: Optional[Callable] = None) -> float:
    """
    Evaluate fitness of a kernel.
    
    Args:
        kernel: Kernel to evaluate
        population: Full population for diversity calculation
        custom_fitness: Optional custom fitness function
    
    Returns:
        Fitness score between 0 and 1
    """
    if custom_fitness:
        return custom_fitness(kernel)
    
    # Default fitness calculation
    coeffs = np.array(kernel.base_kernel.coefficients)
    
    # Grip component: coefficient quality
    optimal_range = (coeffs > 0.1) & (coeffs < 0.9)
    grip = np.mean(optimal_range)
    
    # Stability component: variance
    stability = 1.0 - min(1.0, np.std(coeffs))
    
    # Efficiency component: simplicity (fewer extreme values)
    efficiency = 1.0 - np.mean(np.abs(coeffs - 0.5))
    
    # Novelty component: genetic diversity
    novelty = calculate_kernel_diversity(kernel, population)
    
    # Symmetry component: balance
    symmetry = 1.0 - abs(np.mean(coeffs) - 0.5)
    
    # Weighted combination
    fitness = (
        grip * 0.4 +
        stability * 0.2 +
        efficiency * 0.2 +
        novelty * 0.1 +
        symmetry * 0.1
    )
    
    kernel.genome.fitness = fitness
    return float(fitness)


def tournament_selection(population: List[OntogeneticKernel],
                        fitnesses: List[float],
                        tournament_size: int = 3) -> OntogeneticKernel:
    """
    Select individual via tournament selection.
    
    Args:
        population: Population to select from
        fitnesses: Fitness scores
        tournament_size: Number of individuals in tournament
    
    Returns:
        Selected individual
    """
    # Random tournament
    indices = np.random.choice(len(population), tournament_size, replace=False)
    tournament_fitnesses = [fitnesses[i] for i in indices]
    
    winner_idx = indices[np.argmax(tournament_fitnesses)]
    return population[winner_idx]


def calculate_population_diversity(population: List[OntogeneticKernel]) -> float:
    """
    Calculate genetic diversity of population.
    
    Args:
        population: Population to analyze
    
    Returns:
        Diversity score between 0 and 1
    """
    if len(population) < 2:
        return 0.0
    
    # Calculate pairwise distances
    distances = []
    for i in range(len(population)):
        for j in range(i + 1, len(population)):
            dist = _genetic_distance(population[i], population[j])
            distances.append(dist)
    
    # Average distance as diversity measure
    diversity = np.mean(distances) if distances else 0.0
    return min(1.0, diversity)


def calculate_kernel_diversity(kernel: OntogeneticKernel,
                               population: List[OntogeneticKernel]) -> float:
    """
    Calculate how diverse a kernel is relative to population.
    
    Args:
        kernel: Kernel to evaluate
        population: Population for comparison
    
    Returns:
        Diversity score between 0 and 1
    """
    if len(population) <= 1:
        return 0.5
    
    distances = []
    for other in population:
        if other is kernel:
            continue
        distances.append(_genetic_distance(kernel, other))
    
    avg_distance = np.mean(distances) if distances else 0.5
    return min(1.0, avg_distance)


def _genetic_distance(kernel1: OntogeneticKernel,
                     kernel2: OntogeneticKernel) -> float:
    """
    Calculate genetic distance between two kernels.
    
    Uses Euclidean distance in coefficient space.
    """
    coeffs1 = np.array(kernel1.base_kernel.coefficients)
    coeffs2 = np.array(kernel2.base_kernel.coefficients)
    
    # Pad shorter array if needed
    max_len = max(len(coeffs1), len(coeffs2))
    if len(coeffs1) < max_len:
        coeffs1 = np.pad(coeffs1, (0, max_len - len(coeffs1)))
    if len(coeffs2) < max_len:
        coeffs2 = np.pad(coeffs2, (0, max_len - len(coeffs2)))
    
    distance = np.linalg.norm(coeffs1 - coeffs2)
    return float(distance)
