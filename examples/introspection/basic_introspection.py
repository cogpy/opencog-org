#!/usr/bin/env python3
"""
Example: Basic Introspection

Demonstrates recursive introspection and self-optimization of a copilot.
"""

import sys
sys.path.insert(0, '/home/runner/work/opencog-org/opencog-org')

from introspection import (
    Copilot, 
    CopilotGenome,
    introspect,
    self_optimize,
    evaluate_fitness,
    evaluate_grip
)
from introspection.metrics import IntrospectionMetrics


def main():
    print("=" * 60)
    print("Copilot Introspection Example")
    print("=" * 60)
    
    # Create a copilot instance
    print("\n1. Creating copilot with initial capabilities...")
    copilot = Copilot(domain="research")
    
    print("\nInitial Capabilities:")
    for capability, value in copilot.genome.capabilities.items():
        print(f"  {capability}: {value:.3f}")
    
    # Perform recursive introspection
    print("\n2. Performing recursive introspection (depth=3)...")
    result = introspect(copilot, depth=3)
    
    print("\nIntrospection Result:")
    print(f"  Meta-level: {result.get('meta_level', 0)}")
    print(f"  Introspection depth: {result.get('introspection_depth', 0):.3f}")
    print(f"  Stage: {result.get('stage', 'unknown')}")
    
    # Initialize metrics tracker
    metrics = IntrospectionMetrics()
    
    # Self-optimization
    print("\n3. Running self-optimization (5 iterations)...")
    for i in range(5):
        grip = evaluate_grip(copilot)
        fitness = evaluate_fitness(copilot)
        
        metrics.record_iteration(grip, fitness, copilot.genome.capabilities)
        
        print(f"\n  Iteration {i+1}:")
        print(f"    Grip: {grip:.3f}")
        print(f"    Fitness: {fitness:.3f}")
        print(f"    Stage: {copilot.ontogenetic_state.stage.value}")
        print(f"    Maturity: {copilot.ontogenetic_state.maturity:.3f}")
        
        self_optimize(copilot, iterations=1)
    
    # Final state
    print("\n4. Final copilot state:")
    print("\nFinal Capabilities:")
    for capability, value in copilot.genome.capabilities.items():
        print(f"  {capability}: {value:.3f}")
    
    print(f"\nFinal Stage: {copilot.ontogenetic_state.stage.value}")
    print(f"Final Maturity: {copilot.ontogenetic_state.maturity:.3f}")
    
    # Metrics summary
    print("\n5. Metrics Summary:")
    stats = metrics.get_statistics()
    for key, value in stats.items():
        if isinstance(value, bool):
            print(f"  {key}: {value}")
        else:
            print(f"  {key}: {value:.3f}")
    
    print("\n" + "=" * 60)
    print("✅ Introspection complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
