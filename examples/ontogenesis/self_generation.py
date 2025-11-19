#!/usr/bin/env python3
"""
Example: Self-Generating Kernels

Demonstrates kernel self-generation through recursive composition.
"""

import sys
sys.path.insert(0, '/home/runner/work/opencog-org/opencog-org')

from ontogenesis import (
    create_consciousness_kernel,
    self_generate,
    self_optimize_kernel,
    self_reproduce
)


def main():
    print("=" * 60)
    print("Self-Generating Kernels Example")
    print("=" * 60)
    
    # Create initial kernel
    print("\n1. Creating initial consciousness kernel...")
    ancestor = create_consciousness_kernel(order=4)
    
    print(f"  Ancestor ID: {ancestor.genome.id}")
    print(f"  Generation: {ancestor.genome.generation}")
    print(f"  Coefficients: {[f'{c:.3f}' for c in ancestor.base_kernel.coefficients]}")
    
    # Generate lineage through self-generation
    print("\n2. Generating lineage (5 generations)...")
    lineage = [ancestor]
    current = ancestor
    
    for i in range(5):
        offspring = self_generate(current)
        lineage.append(offspring)
        
        print(f"\n  Generation {i+1}:")
        print(f"    ID: {offspring.genome.id}")
        print(f"    Parent: {offspring.genome.lineage[-1] if offspring.genome.lineage else 'none'}")
        print(f"    Coefficients: {[f'{c:.3f}' for c in offspring.base_kernel.coefficients]}")
        print(f"    Stage: {offspring.development_stage.value}")
        
        current = offspring
    
    # Self-optimization
    print("\n3. Self-optimizing final kernel...")
    final_kernel = lineage[-1]
    
    print(f"\n  Before optimization:")
    print(f"    Maturity: {final_kernel.maturity:.3f}")
    print(f"    Coefficients: {[f'{c:.3f}' for c in final_kernel.base_kernel.coefficients]}")
    
    self_optimize_kernel(final_kernel, iterations=5)
    
    print(f"\n  After optimization:")
    print(f"    Maturity: {final_kernel.maturity:.3f}")
    print(f"    Stage: {final_kernel.development_stage.value}")
    print(f"    Coefficients: {[f'{c:.3f}' for c in final_kernel.base_kernel.coefficients]}")
    
    # Self-reproduction with two kernels
    print("\n4. Self-reproduction (crossover)...")
    parent1 = lineage[2]
    parent2 = lineage[4]
    
    print(f"\n  Parent 1: {parent1.genome.id}")
    print(f"    Coefficients: {[f'{c:.3f}' for c in parent1.base_kernel.coefficients]}")
    
    print(f"\n  Parent 2: {parent2.genome.id}")
    print(f"    Coefficients: {[f'{c:.3f}' for c in parent2.base_kernel.coefficients]}")
    
    child = self_reproduce(parent1, parent2, method='crossover')
    
    print(f"\n  Child: {child.genome.id}")
    print(f"    Generation: {child.genome.generation}")
    print(f"    Lineage: {child.genome.lineage}")
    print(f"    Coefficients: {[f'{c:.3f}' for c in child.base_kernel.coefficients]}")
    
    # Lineage summary
    print("\n5. Lineage Summary:")
    print(f"\n  Total generations: {len(lineage)}")
    print(f"  Ancestor ID: {lineage[0].genome.id}")
    print(f"  Final descendant ID: {lineage[-1].genome.id}")
    print(f"  Final maturity: {lineage[-1].maturity:.3f}")
    print(f"  Final stage: {lineage[-1].development_stage.value}")
    
    # Show genetic drift
    print("\n6. Genetic Drift Analysis:")
    ancestor_coeffs = lineage[0].base_kernel.coefficients
    final_coeffs = lineage[-1].base_kernel.coefficients
    
    print(f"\n  {'Coefficient':>12} | {'Ancestor':>10} | {'Final':>10} | {'Change':>10}")
    print("  " + "-" * 50)
    
    for i, (a, f) in enumerate(zip(ancestor_coeffs, final_coeffs)):
        change = f - a
        print(f"  {'b'+str(i+1):>12} | {a:10.4f} | {f:10.4f} | {change:10.4f}")
    
    print("\n" + "=" * 60)
    print("✅ Self-generation complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
