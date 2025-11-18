#!/usr/bin/env python3
"""
Example: Ontogenesis Evolution

Demonstrates self-generating kernels evolving over multiple generations.
"""

import sys
sys.path.insert(0, '/home/runner/work/opencog-org/opencog-org')

from ontogenesis import (
    OntogenesisConfig,
    EvolutionConfig,
    run_ontogenesis,
    create_consciousness_kernel,
    create_physics_kernel,
    create_mathematics_kernel
)


def main():
    print("=" * 60)
    print("Ontogenesis Evolution Example")
    print("=" * 60)
    
    # Create seed kernels
    print("\n1. Creating seed kernels...")
    consciousness = create_consciousness_kernel(order=4)
    physics = create_physics_kernel(order=4)
    mathematics = create_mathematics_kernel(order=4)
    
    print(f"\n  Consciousness kernel: {consciousness.genome.id}")
    print(f"    Coefficients: {[f'{c:.3f}' for c in consciousness.base_kernel.coefficients]}")
    
    print(f"\n  Physics kernel: {physics.genome.id}")
    print(f"    Coefficients: {[f'{c:.3f}' for c in physics.base_kernel.coefficients]}")
    
    print(f"\n  Mathematics kernel: {mathematics.genome.id}")
    print(f"    Coefficients: {[f'{c:.3f}' for c in mathematics.base_kernel.coefficients]}")
    
    # Configure evolution
    print("\n2. Configuring evolution...")
    config = OntogenesisConfig(
        evolution=EvolutionConfig(
            population_size=15,
            mutation_rate=0.15,
            crossover_rate=0.8,
            elitism_rate=0.15,
            max_generations=20,
            fitness_threshold=0.85,
            diversity_pressure=0.2
        ),
        seed_kernels=[consciousness, physics, mathematics]
    )
    
    print(f"  Population size: {config.evolution.population_size}")
    print(f"  Max generations: {config.evolution.max_generations}")
    print(f"  Fitness threshold: {config.evolution.fitness_threshold}")
    
    # Run evolution
    print("\n3. Running ontogenesis evolution...")
    print("\n" + "-" * 60)
    
    generations = run_ontogenesis(config)
    
    print("-" * 60)
    
    # Analyze results
    print("\n4. Evolution Results:")
    print("\nGeneration Summary:")
    print(f"  {'Gen':>4} | {'Best Fit':>8} | {'Avg Fit':>8} | {'Diversity':>9} | {'Best Stage':>12}")
    print("  " + "-" * 60)
    
    for gen in generations:
        print(f"  {gen.generation:4d} | "
              f"{gen.best_fitness:8.4f} | "
              f"{gen.average_fitness:8.4f} | "
              f"{gen.diversity:9.4f} | "
              f"{gen.best_kernel.development_stage.value:>12}")
    
    # Best kernel analysis
    best_gen = generations[-1]
    best_kernel = best_gen.best_kernel
    
    print("\n5. Best Kernel Analysis:")
    print(f"  Genome ID: {best_kernel.genome.id}")
    print(f"  Generation: {best_kernel.genome.generation}")
    print(f"  Lineage depth: {len(best_kernel.genome.lineage)}")
    print(f"  Fitness: {best_kernel.genome.fitness:.4f}")
    print(f"  Development stage: {best_kernel.development_stage.value}")
    print(f"  Maturity: {best_kernel.maturity:.3f}")
    print(f"  Domain: {best_kernel.base_kernel.domain}")
    
    print("\n  Coefficients:")
    for i, coeff in enumerate(best_kernel.base_kernel.coefficients):
        print(f"    b{i+1}: {coeff:.4f}")
    
    # Evolution statistics
    print("\n6. Evolution Statistics:")
    initial_fitness = generations[0].best_fitness
    final_fitness = generations[-1].best_fitness
    improvement = final_fitness - initial_fitness
    
    print(f"  Initial best fitness: {initial_fitness:.4f}")
    print(f"  Final best fitness: {final_fitness:.4f}")
    print(f"  Total improvement: {improvement:.4f} ({improvement/initial_fitness*100:.1f}%)")
    print(f"  Generations completed: {len(generations)}")
    print(f"  Final diversity: {best_gen.diversity:.4f}")
    
    print("\n" + "=" * 60)
    print("✅ Ontogenesis evolution complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
