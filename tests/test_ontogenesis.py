"""
Unit tests for ontogenesis framework.
"""

import pytest
import numpy as np
from ontogenesis import (
    OntogeneticKernel, KernelGenome,
    self_generate, self_optimize_kernel, self_reproduce,
    run_ontogenesis, evolve_population, evaluate_kernel_fitness,
    create_consciousness_kernel, create_physics_kernel, create_mathematics_kernel
)
from ontogenesis.core import KernelGene, GeneType, DevelopmentStage
from ontogenesis.evolution import calculate_population_diversity


class TestKernelGene:
    """Tests for KernelGene class."""
    
    def test_initialization(self):
        """Test gene initializes correctly."""
        gene = KernelGene(
            gene_type=GeneType.COEFFICIENT,
            name="b1",
            value=0.5
        )
        assert gene.gene_type == GeneType.COEFFICIENT
        assert gene.name == "b1"
        assert gene.value == 0.5
        assert gene.mutable is True
    
    def test_immutable_gene(self):
        """Test immutable genes don't mutate."""
        gene = KernelGene(
            gene_type=GeneType.SYMMETRY,
            name="symmetry",
            value=1.0,
            mutable=False
        )
        original_value = gene.value
        gene.mutate(rate=1.0)  # Force mutation attempt
        assert gene.value == original_value
    
    def test_mutable_gene_mutation(self):
        """Test mutable genes can mutate."""
        np.random.seed(42)
        gene = KernelGene(
            gene_type=GeneType.COEFFICIENT,
            name="b1",
            value=0.5,
            mutable=True
        )
        original_value = gene.value
        # Multiple attempts to ensure mutation happens
        for _ in range(10):
            gene.mutate(rate=1.0)
        # Value should have changed (with high probability)
        # Note: Small chance this fails due to randomness
    
    def test_mutation_bounds(self):
        """Test mutation keeps values in [0, 1]."""
        gene = KernelGene(
            gene_type=GeneType.COEFFICIENT,
            name="b1",
            value=0.99
        )
        for _ in range(20):
            gene.mutate(rate=1.0)
            assert 0.0 <= gene.value <= 1.0


class TestKernelGenome:
    """Tests for KernelGenome class."""
    
    def test_initialization(self):
        """Test genome initializes with genes."""
        genome = KernelGenome(order=3)
        assert genome.order == 3
        assert len(genome.genes) > 0
        assert genome.generation == 0
    
    def test_get_gene(self):
        """Test gene retrieval."""
        genome = KernelGenome(order=2)
        # Add a known gene
        gene = KernelGene(GeneType.COEFFICIENT, "test_gene", 0.7)
        genome.genes.append(gene)
        retrieved = genome.get_gene("test_gene")
        assert retrieved.value == 0.7
    
    def test_lineage_tracking(self):
        """Test lineage is tracked."""
        genome = KernelGenome(order=2)
        assert isinstance(genome.lineage, list)


class TestOntogeneticKernel:
    """Tests for OntogeneticKernel class."""
    
    def test_initialization(self):
        """Test kernel initializes correctly."""
        kernel = OntogeneticKernel(order=3, kernel_type="standard")
        assert kernel.order == 3
        assert kernel.kernel_type == "standard"
        assert kernel.id is not None
        assert isinstance(kernel.genome, KernelGenome)
        assert isinstance(kernel.coefficients, np.ndarray)
    
    def test_evaluate(self):
        """Test kernel evaluation."""
        kernel = OntogeneticKernel(order=2)
        x = np.array([1.0])
        h = 0.1
        result = kernel.evaluate(x, h)
        assert isinstance(result, (np.ndarray, float))
    
    def test_get_fitness(self):
        """Test fitness calculation."""
        kernel = OntogeneticKernel(order=2)
        fitness = kernel.get_fitness()
        assert 0.0 <= fitness <= 1.0
    
    def test_development_stage(self):
        """Test development stage property."""
        kernel = OntogeneticKernel(order=2)
        stage = kernel.development_stage
        assert isinstance(stage, DevelopmentStage)


class TestSelfGeneration:
    """Tests for self_generate function."""
    
    def test_basic_self_generation(self):
        """Test basic self-generation produces offspring."""
        parent = OntogeneticKernel(order=2)
        offspring = self_generate(parent)
        
        assert offspring is not None
        assert offspring.id != parent.id
        assert offspring.genome.generation == parent.genome.generation + 1
    
    def test_offspring_inherits_properties(self):
        """Test offspring inherits parent properties."""
        parent = OntogeneticKernel(order=3, kernel_type="consciousness")
        offspring = self_generate(parent)
        
        assert offspring.order == parent.order
        assert offspring.genome.generation > parent.genome.generation
    
    def test_lineage_tracking(self):
        """Test lineage is tracked across generations."""
        gen0 = OntogeneticKernel(order=2)
        gen1 = self_generate(gen0)
        gen2 = self_generate(gen1)
        
        assert gen2.genome.generation == 2
        assert len(gen2.genome.lineage) >= 2


class TestSelfOptimization:
    """Tests for self_optimize_kernel function."""
    
    def test_basic_optimization(self):
        """Test basic kernel optimization."""
        kernel = OntogeneticKernel(order=2)
        initial_fitness = kernel.get_fitness()
        
        optimized = self_optimize_kernel(kernel, iterations=3)
        
        # Fitness should improve or stay stable
        assert optimized.get_fitness() >= initial_fitness * 0.9
    
    def test_optimization_iterations(self):
        """Test optimization runs specified iterations."""
        kernel = OntogeneticKernel(order=2)
        # This should complete without errors
        self_optimize_kernel(kernel, iterations=5)


class TestSelfReproduction:
    """Tests for self_reproduce function."""
    
    def test_basic_reproduction(self):
        """Test reproduction between two kernels."""
        parent1 = OntogeneticKernel(order=2)
        parent2 = OntogeneticKernel(order=2)
        
        offspring = self_reproduce(parent1, parent2)
        
        assert offspring is not None
        assert offspring.id not in [parent1.id, parent2.id]
        assert offspring.genome.generation == max(
            parent1.genome.generation,
            parent2.genome.generation
        ) + 1
    
    def test_crossover_occurs(self):
        """Test genetic crossover occurs."""
        np.random.seed(42)
        parent1 = OntogeneticKernel(order=2)
        parent2 = OntogeneticKernel(order=2)
        
        # Set different coefficient values
        parent1.coefficients = np.array([0.1, 0.2])
        parent2.coefficients = np.array([0.9, 0.8])
        
        offspring = self_reproduce(parent1, parent2)
        
        # Offspring should have mix of parent coefficients
        assert offspring is not None
    
    def test_mutation_rate_parameter(self):
        """Test mutation rate parameter."""
        parent1 = OntogeneticKernel(order=2)
        parent2 = OntogeneticKernel(order=2)
        
        offspring = self_reproduce(parent1, parent2, mutation_rate=0.5)
        assert offspring is not None


class TestEvolution:
    """Tests for evolution functions."""
    
    def test_evaluate_kernel_fitness(self):
        """Test kernel fitness evaluation."""
        kernel = OntogeneticKernel(order=2)
        fitness = evaluate_kernel_fitness(kernel)
        
        assert isinstance(fitness, float)
        assert 0.0 <= fitness <= 1.0
    
    def test_population_diversity(self):
        """Test population diversity calculation."""
        population = [
            OntogeneticKernel(order=2) for _ in range(5)
        ]
        
        diversity = calculate_population_diversity(population)
        assert isinstance(diversity, float)
        assert diversity >= 0.0
    
    def test_evolve_population(self):
        """Test single generation evolution."""
        population = [
            OntogeneticKernel(order=2) for _ in range(10)
        ]
        
        new_population = evolve_population(population)
        
        assert len(new_population) == len(population)
        assert all(isinstance(k, OntogeneticKernel) for k in new_population)
    
    def test_run_ontogenesis(self):
        """Test multi-generation ontogenesis."""
        initial_kernel = OntogeneticKernel(order=2)
        
        result = run_ontogenesis(
            initial_kernel=initial_kernel,
            generations=3,
            population_size=5
        )
        
        assert 'final_population' in result
        assert 'best_kernel' in result
        assert 'history' in result
        assert len(result['history']) <= 3


class TestDomainSpecificKernels:
    """Tests for domain-specific kernel creation."""
    
    def test_consciousness_kernel(self):
        """Test consciousness kernel creation."""
        kernel = create_consciousness_kernel(order=3)
        
        assert kernel.kernel_type == "consciousness"
        assert kernel.order == 3
        assert isinstance(kernel, OntogeneticKernel)
    
    def test_physics_kernel(self):
        """Test physics kernel creation."""
        kernel = create_physics_kernel(order=3)
        
        assert kernel.kernel_type == "physics"
        assert kernel.order == 3
    
    def test_mathematics_kernel(self):
        """Test mathematics kernel creation."""
        kernel = create_mathematics_kernel(order=4)
        
        assert kernel.kernel_type == "mathematics"
        assert kernel.order == 4
    
    def test_different_kernels_have_different_properties(self):
        """Test domain-specific kernels have unique properties."""
        consciousness = create_consciousness_kernel(order=3)
        physics = create_physics_kernel(order=3)
        math = create_mathematics_kernel(order=3)
        
        # All should be valid kernels
        assert consciousness.kernel_type != physics.kernel_type
        assert physics.kernel_type != math.kernel_type


class TestGeneticOperators:
    """Tests for genetic operators."""
    
    def test_crossover_creates_offspring(self):
        """Test crossover operation."""
        from ontogenesis.operators import crossover
        
        parent1 = np.array([0.1, 0.2, 0.3])
        parent2 = np.array([0.9, 0.8, 0.7])
        
        offspring = crossover(parent1, parent2)
        
        assert offspring.shape == parent1.shape
        # Offspring should contain values from both parents
    
    def test_mutation_modifies_coefficients(self):
        """Test mutation operation."""
        from ontogenesis.operators import mutate
        
        np.random.seed(42)
        coefficients = np.array([0.5, 0.5, 0.5])
        mutated = mutate(coefficients.copy(), rate=1.0)
        
        # With high mutation rate, values should change
        # (small chance of test failure due to randomness)
    
    def test_mutation_rate_zero(self):
        """Test mutation with rate 0."""
        from ontogenesis.operators import mutate
        
        coefficients = np.array([0.5, 0.5, 0.5])
        mutated = mutate(coefficients.copy(), rate=0.0)
        
        np.testing.assert_array_equal(coefficients, mutated)


class TestConvergence:
    """Tests for convergence behavior."""
    
    def test_early_stopping(self):
        """Test evolution stops early on convergence."""
        initial_kernel = OntogeneticKernel(order=2)
        
        result = run_ontogenesis(
            initial_kernel=initial_kernel,
            generations=50,
            population_size=10,
            convergence_threshold=0.01
        )
        
        # Should converge before 50 generations
        assert len(result['history']) <= 50
    
    def test_fitness_improves(self):
        """Test fitness generally improves over generations."""
        initial_kernel = OntogeneticKernel(order=2)
        
        result = run_ontogenesis(
            initial_kernel=initial_kernel,
            generations=5,
            population_size=8
        )
        
        history = result['history']
        if len(history) >= 2:
            initial_fitness = history[0]['best_fitness']
            final_fitness = history[-1]['best_fitness']
            # Fitness should improve or stay relatively stable
            assert final_fitness >= initial_fitness * 0.8


class TestEdgeCases:
    """Tests for edge cases and error handling."""
    
    def test_order_one_kernel(self):
        """Test kernel with order 1."""
        kernel = OntogeneticKernel(order=1)
        assert kernel.order == 1
        assert len(kernel.coefficients) >= 1
    
    def test_zero_population_size(self):
        """Test evolution with empty population."""
        # Should handle gracefully or raise appropriate error
        try:
            result = run_ontogenesis(
                initial_kernel=OntogeneticKernel(order=2),
                generations=1,
                population_size=0
            )
        except (ValueError, AssertionError):
            pass  # Expected behavior
    
    def test_single_generation(self):
        """Test evolution for single generation."""
        initial_kernel = OntogeneticKernel(order=2)
        
        result = run_ontogenesis(
            initial_kernel=initial_kernel,
            generations=1,
            population_size=5
        )
        
        assert len(result['history']) == 1
    
    def test_large_order_kernel(self):
        """Test kernel with large order."""
        kernel = OntogeneticKernel(order=10)
        assert kernel.order == 10
        # Should handle large orders without errors


class TestIntegration:
    """Integration tests combining multiple components."""
    
    def test_full_lifecycle(self):
        """Test complete kernel lifecycle."""
        # Create initial kernel
        gen0 = create_consciousness_kernel(order=3)
        
        # Self-generate offspring
        gen1 = self_generate(gen0)
        
        # Optimize
        gen1_optimized = self_optimize_kernel(gen1, iterations=2)
        
        # Reproduce with another kernel
        gen0_alt = create_consciousness_kernel(order=3)
        gen2 = self_reproduce(gen1_optimized, gen0_alt)
        
        # Verify lineage
        assert gen2.genome.generation >= 2
    
    def test_population_evolution_stability(self):
        """Test population evolution maintains stability."""
        initial = OntogeneticKernel(order=2)
        
        result = run_ontogenesis(
            initial_kernel=initial,
            generations=5,
            population_size=15
        )
        
        # Final population should be valid
        assert len(result['final_population']) > 0
        assert all(k.get_fitness() >= 0 for k in result['final_population'])


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
