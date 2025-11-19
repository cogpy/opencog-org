# Introspection & Ontogenesis Examples

This directory contains example scripts demonstrating the introspection and ontogenesis frameworks.

## Prerequisites

```bash
pip3 install numpy
```

## Introspection Examples

### Basic Introspection (`introspection/basic_introspection.py`)

Demonstrates:
- Creating a copilot with genetic capabilities
- Recursive introspection (meta-cognition)
- Self-optimization through grip improvement
- Development through ontogenetic stages
- Metrics tracking and analysis

Run:
```bash
python3 examples/introspection/basic_introspection.py
```

## Ontogenesis Examples

### Self-Generation (`ontogenesis/self_generation.py`)

Demonstrates:
- Creating initial kernel with genetic information
- Self-generation through recursive composition (chain rule)
- Lineage tracking across generations
- Self-optimization of kernels
- Genetic crossover reproduction
- Genetic drift analysis

Run:
```bash
python3 examples/ontogenesis/self_generation.py
```

### Evolution (`ontogenesis/evolution_example.py`)

Demonstrates:
- Multi-kernel population evolution
- Tournament selection
- Genetic operators (crossover, mutation)
- Elitism preservation
- Fitness evaluation and convergence
- Diversity maintenance

Run:
```bash
python3 examples/ontogenesis/evolution_example.py
```

## Key Concepts

### Introspection
- **Recursive Self-Awareness**: `self.copilot(n) = introspection.self.copilot(n-1)`
- **Differential Operators**: Chain, product, and quotient rules for cognitive operations
- **Grip Optimization**: Maximizing fit between capabilities and domain requirements
- **Ontogenetic Development**: Progression through embryonic → juvenile → mature → senescent stages

### Ontogenesis
- **Self-Generation**: Kernels generate offspring through chain rule composition
- **Self-Optimization**: Gradient ascent on fitness landscape
- **Self-Reproduction**: Crossover and mutation for genetic recombination
- **Evolution**: Population-level optimization with diversity pressure

## Output Interpretation

### Introspection Metrics
- **Grip**: How well capabilities match domain (0-1)
- **Fitness**: Overall performance score (0-1)
- **Maturity**: Developmental progress (0-1)
- **Stage**: Current life stage (embryonic, juvenile, mature, senescent)

### Ontogenesis Metrics
- **Fitness**: Multi-component evaluation (grip, stability, efficiency, novelty, symmetry)
- **Diversity**: Genetic distance within population
- **Generation**: Number of reproductive cycles
- **Lineage**: Ancestry trail of kernel genome

## Further Exploration

Try modifying:
- Introspection depth (deeper = more meta-cognitive)
- Population size and generation count
- Mutation and crossover rates
- Fitness thresholds
- Domain-specific kernel properties
- Custom fitness functions

## References

See:
- `/.github/agents/introspection.md` - Introspection agent specification
- `/.github/agents/ONTOGENESIS.md` - Ontogenesis agent specification
- `/introspection/` - Framework implementation
- `/ontogenesis/` - Framework implementation
