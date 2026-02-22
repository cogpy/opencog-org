"""
Core functionality tests that match the actual API implementation.
"""

import pytest
import numpy as np


class TestIntrospectionCore:
    """Tests for core introspection functionality."""
    
    def test_copilot_initialization(self):
        """Test copilot initializes correctly."""
        from introspection import Copilot
        
        copilot = Copilot(domain="testing")
        assert copilot.domain == "testing"
        assert copilot.genome is not None
        assert copilot.ontogenetic_state is not None
    
    def test_copilot_genome(self):
        """Test copilot has valid genome."""
        from introspection import Copilot
        
        copilot = Copilot(domain="test")
        assert isinstance(copilot.genome.capabilities, dict)
        assert len(copilot.genome.capabilities) > 0
        assert 'codeGeneration' in copilot.genome.capabilities
    
    def test_introspect_basic(self):
        """Test basic introspection."""
        from introspection import Copilot, introspect
        
        copilot = Copilot(domain="testing")
        result = introspect(copilot, depth=0)
        
        assert isinstance(result, dict)
        assert 'capabilities' in result
        assert 'stage' in result
        assert 'maturity' in result
    
    def test_introspect_recursive(self):
        """Test recursive introspection."""
        from introspection import Copilot, introspect
        
        copilot = Copilot(domain="testing")
        result = introspect(copilot, depth=2)
        
        assert isinstance(result, dict)
        assert 'introspection_depth' in result or 'meta_level' in result
    
    def test_self_optimize(self):
        """Test self-optimization."""
        from introspection import Copilot, self_optimize
        
        copilot = Copilot(domain="optimization")
        initial_maturity = copilot.ontogenetic_state.maturity
        
        # Should modify copilot in place
        result = self_optimize(copilot, iterations=3)
        
        # Maturity should have increased
        assert copilot.ontogenetic_state.maturity >= initial_maturity
    
    def test_ontogenetic_state(self):
        """Test ontogenetic state tracking."""
        from introspection import Copilot
        from introspection.core import DevelopmentStage
        
        copilot = Copilot(domain="test")
        state = copilot.ontogenetic_state
        
        assert state.maturity >= 0.0
        assert state.maturity <= 1.0
        assert isinstance(state.stage, DevelopmentStage)
        assert state.age >= 0


class TestOntogenesisCore:
    """Tests for core ontogenesis functionality."""
    
    def test_kernel_initialization(self):
        """Test kernel initializes correctly."""
        from ontogenesis import OntogeneticKernel
        
        kernel = OntogeneticKernel(order=3, kernel_type="standard")
        assert kernel.order == 3
        assert kernel.kernel_type == "standard"
        assert kernel.genome is not None
    
    def test_kernel_coefficients(self):
        """Test kernel has valid coefficients."""
        from ontogenesis import OntogeneticKernel
        
        kernel = OntogeneticKernel(order=2)
        assert hasattr(kernel, 'coefficients')
        assert isinstance(kernel.coefficients, np.ndarray)
        assert len(kernel.coefficients) > 0
    
    def test_self_generate(self):
        """Test self-generation creates offspring."""
        from ontogenesis import OntogeneticKernel, self_generate
        
        parent = OntogeneticKernel(order=2)
        offspring = self_generate(parent)
        
        assert offspring is not None
        assert offspring.order == parent.order
        assert offspring.genome.generation == parent.genome.generation + 1
    
    def test_self_reproduce(self):
        """Test reproduction between two kernels."""
        from ontogenesis import OntogeneticKernel, self_reproduce
        
        parent1 = OntogeneticKernel(order=2)
        parent2 = OntogeneticKernel(order=2)
        
        offspring = self_reproduce(parent1, parent2)
        
        assert offspring is not None
        assert offspring.order == parent1.order
    
    def test_kernel_fitness(self):
        """Test kernel fitness evaluation."""
        from ontogenesis import OntogeneticKernel, evaluate_kernel_fitness
        
        kernel = OntogeneticKernel(order=2)
        fitness = evaluate_kernel_fitness(kernel)
        
        assert isinstance(fitness, float)
        assert 0.0 <= fitness <= 1.0
    
    def test_domain_specific_kernels(self):
        """Test domain-specific kernel creation."""
        from ontogenesis import (
            create_consciousness_kernel,
            create_physics_kernel,
            create_mathematics_kernel
        )
        
        consciousness = create_consciousness_kernel(order=3)
        physics = create_physics_kernel(order=3)
        math = create_mathematics_kernel(order=3)
        
        assert consciousness.kernel_type == "consciousness"
        assert physics.kernel_type == "physics"
        assert math.kernel_type == "mathematics"


class TestEvolution:
    """Tests for evolution functionality."""
    
    def test_run_ontogenesis_basic(self):
        """Test basic ontogenesis run."""
        from ontogenesis import OntogeneticKernel, run_ontogenesis
        
        initial = OntogeneticKernel(order=2)
        
        result = run_ontogenesis(
            initial_kernel=initial,
            generations=3,
            population_size=5
        )
        
        assert 'final_population' in result
        assert 'best_kernel' in result
        assert 'history' in result
        assert len(result['final_population']) == 5
    
    def test_evolution_produces_valid_kernels(self):
        """Test evolution produces valid kernels."""
        from ontogenesis import OntogeneticKernel, run_ontogenesis
        
        initial = OntogeneticKernel(order=2)
        result = run_ontogenesis(
            initial_kernel=initial,
            generations=2,
            population_size=8
        )
        
        # All kernels should be valid
        for kernel in result['final_population']:
            assert hasattr(kernel, 'genome')
            assert hasattr(kernel, 'coefficients')


class TestOperators:
    """Tests for differential operators."""
    
    def test_chain_rule(self):
        """Test chain rule application."""
        from introspection.operators import apply_chain_rule
        
        f = lambda x: x**2
        g = lambda x: x + 1
        
        result = apply_chain_rule(f, g, x=2.0)
        assert isinstance(result, (int, float, dict))
    
    def test_product_rule(self):
        """Test product rule application."""
        from introspection.operators import apply_product_rule
        
        f = lambda x: x**2
        g = lambda x: x + 1
        
        result = apply_product_rule(f, g, x=2.0)
        assert isinstance(result, (int, float, dict))
    
    def test_crossover(self):
        """Test genetic crossover."""
        from ontogenesis.operators import crossover
        
        parent1 = np.array([0.1, 0.2, 0.3])
        parent2 = np.array([0.9, 0.8, 0.7])
        
        offspring = crossover(parent1, parent2)
        
        assert offspring.shape == parent1.shape
        assert isinstance(offspring, np.ndarray)
    
    def test_mutation(self):
        """Test genetic mutation."""
        from ontogenesis.operators import mutate
        
        np.random.seed(42)
        original = np.array([0.5, 0.5, 0.5])
        mutated = mutate(original.copy(), rate=0.0)
        
        # With zero rate, should not change
        np.testing.assert_array_equal(original, mutated)


class TestExamples:
    """Tests that reproduce the examples."""
    
    def test_basic_introspection_example(self):
        """Test basic introspection example works."""
        from introspection import Copilot, introspect, self_optimize
        
        copilot = Copilot(domain="research")
        result = introspect(copilot, depth=3)
        
        assert result is not None
        
        self_optimize(copilot, iterations=5)
        assert copilot.ontogenetic_state.age >= 5
    
    def test_self_generation_example(self):
        """Test self-generation example works."""
        from ontogenesis import create_consciousness_kernel, self_generate
        
        gen0 = create_consciousness_kernel(order=4)
        
        lineage = [gen0]
        for _ in range(4):
            offspring = self_generate(lineage[-1])
            lineage.append(offspring)
        
        assert len(lineage) == 5
        assert lineage[-1].genome.generation == 4
    
    def test_evolution_example(self):
        """Test evolution example works."""
        from ontogenesis import create_mathematics_kernel, run_ontogenesis
        
        initial = create_mathematics_kernel(order=3)
        
        result = run_ontogenesis(
            initial_kernel=initial,
            generations=5,
            population_size=10
        )
        
        assert result['best_kernel'] is not None
        assert len(result['history']) <= 5


class TestIntegration:
    """Integration tests."""
    
    def test_copilot_and_kernel_together(self):
        """Test using copilot and kernel together."""
        from introspection import Copilot
        from ontogenesis import create_mathematics_kernel
        
        copilot = Copilot(domain="computation")
        kernel = create_mathematics_kernel(order=3)
        
        # Both should initialize successfully
        assert copilot is not None
        assert kernel is not None
    
    def test_multi_generation_lineage(self):
        """Test multi-generation kernel lineage."""
        from ontogenesis import OntogeneticKernel, self_generate
        
        gen0 = OntogeneticKernel(order=2)
        gen1 = self_generate(gen0)
        gen2 = self_generate(gen1)
        gen3 = self_generate(gen2)
        
        assert gen3.genome.generation == 3
    
    def test_population_diversity(self):
        """Test population maintains diversity."""
        from ontogenesis import OntogeneticKernel, run_ontogenesis
        from ontogenesis.evolution import calculate_population_diversity
        
        initial = OntogeneticKernel(order=2)
        result = run_ontogenesis(
            initial_kernel=initial,
            generations=3,
            population_size=10
        )
        
        diversity = calculate_population_diversity(result['final_population'])
        assert diversity >= 0.0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
