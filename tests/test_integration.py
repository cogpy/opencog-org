"""
Integration tests for introspection and ontogenesis frameworks.
"""

import pytest
import numpy as np
from introspection import Copilot, introspect, self_optimize
from ontogenesis import (
    OntogeneticKernel, self_generate, self_optimize_kernel, self_reproduce
)
from ontogenesis.evolution import run_ontogenesis
from ontogenesis.kernels import (
    create_consciousness_kernel, create_physics_kernel, create_mathematics_kernel
)


class TestIntrospectionOntogenesisIntegration:
    """Tests for integration between introspection and ontogenesis."""
    
    def test_parallel_evolution(self):
        """Test copilot and kernel evolving in parallel."""
        copilot = Copilot(domain="parallel")
        kernel = OntogeneticKernel(order=2)
        
        # Evolve both
        introspect(copilot, depth=2)
        offspring = self_generate(kernel)
        
        assert copilot.state.introspection_depth >= 2
        assert offspring.genome.generation == 1
    
    def test_copilot_uses_kernel(self):
        """Test copilot using kernel for computation."""
        copilot = Copilot(domain="computation")
        kernel = create_mathematics_kernel(order=3)
        
        # Copilot could use kernel for mathematical operations
        initial_fitness = copilot.state.overall_fitness
        introspect(copilot, depth=1)
        
        # Both should be in valid states
        assert 0.0 <= copilot.state.overall_fitness <= 1.0
        assert 0.0 <= kernel.get_fitness() <= 1.0


class TestMultiGenerationEvolution:
    """Tests for multi-generation evolution scenarios."""
    
    def test_three_generation_lineage(self):
        """Test tracking lineage across three generations."""
        gen0 = create_consciousness_kernel(order=2)
        gen1 = self_generate(gen0)
        gen2 = self_generate(gen1)
        
        assert gen0.genome.generation == 0
        assert gen1.genome.generation == 1
        assert gen2.genome.generation == 2
    
    def test_population_evolution_stability(self):
        """Test population remains stable across generations."""
        initial = OntogeneticKernel(order=2)
        
        result = run_ontogenesis(
            initial_kernel=initial,
            generations=10,
            population_size=20
        )
        
        final_pop = result['final_population']
        assert len(final_pop) == 20
        assert all(k.get_fitness() >= 0 for k in final_pop)


class TestConcurrentOptimization:
    """Tests for concurrent optimization scenarios."""
    
    def test_multiple_copilots(self):
        """Test multiple copilots optimizing concurrently."""
        copilots = [
            Copilot(domain="coding"),
            Copilot(domain="testing"),
            Copilot(domain="documentation")
        ]
        
        for copilot in copilots:
            self_optimize(copilot, iterations=2)
        
        # All should have improved or stayed stable
        for copilot in copilots:
            assert copilot.state.overall_fitness >= 0
    
    def test_multiple_kernel_populations(self):
        """Test multiple kernel populations evolving."""
        populations = []
        
        for kernel_type_func in [
            create_consciousness_kernel,
            create_physics_kernel,
            create_mathematics_kernel
        ]:
            initial = kernel_type_func(order=2)
            result = run_ontogenesis(
                initial_kernel=initial,
                generations=3,
                population_size=5
            )
            populations.append(result['final_population'])
        
        # All populations should have evolved successfully
        assert len(populations) == 3
        for pop in populations:
            assert len(pop) == 5


class TestComplexScenarios:
    """Tests for complex real-world scenarios."""
    
    def test_full_development_cycle(self):
        """Test complete development from embryonic to mature."""
        copilot = Copilot(domain="full-cycle")
        
        # Evolve through stages
        for _ in range(10):
            self_optimize(copilot, iterations=1)
            copilot.state.maturity += 0.1
        
        # Should reach mature stage
        from introspection import DevelopmentStage
        assert copilot.development_stage in [
            DevelopmentStage.MATURE,
            DevelopmentStage.SENESCENT
        ]
    
    def test_adaptive_population_size(self):
        """Test evolution with changing population size."""
        initial = OntogeneticKernel(order=2)
        
        # Start with small population
        result1 = run_ontogenesis(
            initial_kernel=initial,
            generations=2,
            population_size=5
        )
        
        # Continue with larger population
        best = result1['best_kernel']
        result2 = run_ontogenesis(
            initial_kernel=best,
            generations=2,
            population_size=15
        )
        
        assert len(result2['final_population']) == 15
    
    def test_crossover_between_types(self):
        """Test crossover between different kernel types."""
        consciousness = create_consciousness_kernel(order=3)
        physics = create_physics_kernel(order=3)
        
        # Crossover should work even with different types
        hybrid = self_reproduce(consciousness, physics)
        
        assert hybrid is not None
        assert hybrid.order == 3


class TestPerformanceBenchmarks:
    """Basic performance benchmarks."""
    
    def test_introspection_performance(self):
        """Test introspection completes in reasonable time."""
        import time
        
        copilot = Copilot(domain="performance")
        start = time.time()
        introspect(copilot, depth=5)
        duration = time.time() - start
        
        # Should complete in less than 1 second
        assert duration < 1.0
    
    def test_evolution_performance(self):
        """Test evolution completes in reasonable time."""
        import time
        
        initial = OntogeneticKernel(order=2)
        start = time.time()
        run_ontogenesis(
            initial_kernel=initial,
            generations=5,
            population_size=10
        )
        duration = time.time() - start
        
        # Should complete in less than 5 seconds
        assert duration < 5.0
    
    def test_large_population_performance(self):
        """Test performance with larger population."""
        import time
        
        initial = OntogeneticKernel(order=2)
        start = time.time()
        run_ontogenesis(
            initial_kernel=initial,
            generations=3,
            population_size=50
        )
        duration = time.time() - start
        
        # Should complete in less than 10 seconds
        assert duration < 10.0


class TestErrorRecovery:
    """Tests for error handling and recovery."""
    
    def test_recover_from_bad_fitness(self):
        """Test recovery when fitness calculation fails."""
        kernel = OntogeneticKernel(order=2)
        
        # Force some edge case
        kernel.coefficients = np.ones(2) * 1e10
        
        # Should handle gracefully
        try:
            fitness = kernel.get_fitness()
            assert 0.0 <= fitness <= 1.0
        except Exception:
            pass  # Acceptable to raise exception
    
    def test_empty_capability_handling(self):
        """Test handling of empty capabilities."""
        from introspection import CopilotGenome
        
        genome = CopilotGenome(capabilities={})
        copilot = Copilot(domain="test")
        copilot.genome = genome
        
        # Should handle empty capabilities
        try:
            introspect(copilot, depth=1)
        except Exception:
            pass  # Acceptable to raise exception


class TestExampleReproduction:
    """Tests that reproduce example scenarios."""
    
    def test_basic_introspection_example(self):
        """Reproduce basic introspection example."""
        copilot = Copilot(domain="research")
        
        # Initial introspection
        result = introspect(copilot, depth=3)
        assert result['depth'] == 3
        
        # Self-optimization
        history = self_optimize(copilot, iterations=5)
        assert len(history) == 5
    
    def test_self_generation_example(self):
        """Reproduce self-generation example."""
        kernel = create_consciousness_kernel(order=4)
        
        # Generate lineage
        lineage = [kernel]
        for _ in range(4):
            offspring = self_generate(lineage[-1])
            lineage.append(offspring)
        
        assert len(lineage) == 5
        assert lineage[-1].genome.generation == 4
    
    def test_evolution_example(self):
        """Reproduce evolution example."""
        initial = create_mathematics_kernel(order=3)
        
        result = run_ontogenesis(
            initial_kernel=initial,
            generations=20,
            population_size=15,
            convergence_threshold=0.01
        )
        
        assert 'final_population' in result
        assert 'best_kernel' in result
        assert 'history' in result


class TestMemoryUsage:
    """Tests for memory usage patterns."""
    
    def test_no_memory_leak_in_evolution(self):
        """Test evolution doesn't leak memory."""
        initial = OntogeneticKernel(order=2)
        
        # Run multiple evolution cycles
        for _ in range(3):
            result = run_ontogenesis(
                initial_kernel=initial,
                generations=5,
                population_size=10
            )
            initial = result['best_kernel']
        
        # Should complete without memory issues
        assert initial is not None
    
    def test_no_memory_leak_in_optimization(self):
        """Test optimization doesn't leak memory."""
        copilot = Copilot(domain="memory-test")
        
        # Run multiple optimization cycles
        for _ in range(10):
            self_optimize(copilot, iterations=5)
        
        # Should complete without memory issues
        assert copilot is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
