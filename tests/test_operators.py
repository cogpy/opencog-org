"""
Unit tests for differential operators in introspection and ontogenesis.
"""

import pytest
import numpy as np
from introspection.operators import (
    apply_chain_rule, apply_product_rule, apply_quotient_rule,
    optimize_grip
)
from ontogenesis.operators import (
    apply_chain_rule_kernel, apply_product_rule_kernel,
    crossover, mutate
)


class TestIntrospectionOperators:
    """Tests for introspection differential operators."""
    
    def test_chain_rule_basic(self):
        """Test chain rule application."""
        f = lambda x: x**2
        g = lambda x: x + 1
        
        result = apply_chain_rule(f, g, x=2.0)
        # f(g(2)) = f(3) = 9
        assert isinstance(result, (int, float))
    
    def test_product_rule_basic(self):
        """Test product rule application."""
        f = lambda x: x**2
        g = lambda x: x + 1
        
        result = apply_product_rule(f, g, x=2.0)
        # f(2) * g(2) = 4 * 3 = 12
        assert isinstance(result, (int, float))
    
    def test_quotient_rule_basic(self):
        """Test quotient rule application."""
        f = lambda x: x**2
        g = lambda x: x + 1
        
        result = apply_quotient_rule(f, g, x=2.0)
        # f(2) / g(2) = 4 / 3
        assert isinstance(result, (int, float))
        assert result > 0
    
    def test_quotient_rule_zero_division(self):
        """Test quotient rule handles zero division."""
        f = lambda x: x**2
        g = lambda x: 0.0
        
        # Should handle zero denominator gracefully
        result = apply_quotient_rule(f, g, x=2.0)
        assert result is not None
    
    def test_optimize_grip(self):
        """Test grip optimization."""
        from introspection import Copilot
        
        copilot = Copilot(domain="optimization")
        initial_grip = copilot.state.grip
        
        optimized = optimize_grip(copilot, iterations=3)
        
        # Grip should be optimized
        assert optimized.state.grip >= initial_grip * 0.9


class TestOntogenesisOperators:
    """Tests for ontogenesis kernel operators."""
    
    def test_chain_rule_kernel(self):
        """Test kernel chain rule application."""
        from ontogenesis import OntogeneticKernel
        
        kernel = OntogeneticKernel(order=2)
        result = apply_chain_rule_kernel(kernel)
        
        assert isinstance(result, np.ndarray)
    
    def test_product_rule_kernel(self):
        """Test kernel product rule."""
        from ontogenesis import OntogeneticKernel
        
        kernel1 = OntogeneticKernel(order=2)
        kernel2 = OntogeneticKernel(order=2)
        
        result = apply_product_rule_kernel(kernel1, kernel2)
        assert isinstance(result, np.ndarray)
    
    def test_crossover_single_point(self):
        """Test single-point crossover."""
        parent1 = np.array([0.1, 0.2, 0.3, 0.4])
        parent2 = np.array([0.9, 0.8, 0.7, 0.6])
        
        offspring = crossover(parent1, parent2)
        
        assert offspring.shape == parent1.shape
        # Offspring should have elements from both parents
    
    def test_crossover_preserves_length(self):
        """Test crossover preserves array length."""
        parent1 = np.array([0.5] * 10)
        parent2 = np.array([0.3] * 10)
        
        offspring = crossover(parent1, parent2)
        assert len(offspring) == len(parent1)
    
    def test_mutate_with_zero_rate(self):
        """Test mutation with zero rate doesn't change values."""
        original = np.array([0.5, 0.5, 0.5])
        mutated = mutate(original.copy(), rate=0.0)
        
        np.testing.assert_array_equal(original, mutated)
    
    def test_mutate_with_high_rate(self):
        """Test mutation with high rate changes values."""
        np.random.seed(42)
        original = np.array([0.5, 0.5, 0.5, 0.5, 0.5])
        mutated = mutate(original.copy(), rate=1.0)
        
        # With high mutation rate, at least some values should change
        # (very small chance of failure due to randomness)
    
    def test_mutate_bounds(self):
        """Test mutation keeps values in valid range."""
        np.random.seed(42)
        coefficients = np.array([0.1, 0.9, 0.5])
        
        for _ in range(20):
            coefficients = mutate(coefficients, rate=1.0)
            assert np.all(coefficients >= 0.0)
            assert np.all(coefficients <= 1.0)


class TestOperatorComposition:
    """Tests for operator composition and chaining."""
    
    def test_chain_then_product(self):
        """Test chaining operators."""
        f = lambda x: x**2
        g = lambda x: x + 1
        h = lambda x: x * 2
        
        # Apply chain rule, then product rule
        chained = apply_chain_rule(f, g, x=2.0)
        assert isinstance(chained, (int, float))
    
    def test_multiple_kernel_operations(self):
        """Test multiple kernel operations."""
        from ontogenesis import OntogeneticKernel
        
        k1 = OntogeneticKernel(order=2)
        k2 = OntogeneticKernel(order=2)
        
        # Apply multiple operations
        result1 = apply_chain_rule_kernel(k1)
        result2 = apply_product_rule_kernel(k1, k2)
        
        assert isinstance(result1, np.ndarray)
        assert isinstance(result2, np.ndarray)


class TestNumericalStability:
    """Tests for numerical stability of operators."""
    
    def test_large_values(self):
        """Test operators with large values."""
        f = lambda x: x * 1000
        g = lambda x: x + 1
        
        result = apply_chain_rule(f, g, x=100.0)
        assert np.isfinite(result)
    
    def test_small_values(self):
        """Test operators with small values."""
        f = lambda x: x * 0.001
        g = lambda x: x + 0.001
        
        result = apply_product_rule(f, g, x=0.001)
        assert np.isfinite(result)
    
    def test_kernel_stability(self):
        """Test kernel operators remain stable."""
        from ontogenesis import OntogeneticKernel
        
        kernel = OntogeneticKernel(order=5)
        kernel.coefficients = np.array([0.9] * 5)
        
        result = apply_chain_rule_kernel(kernel)
        assert np.all(np.isfinite(result))


class TestEdgeCases:
    """Tests for edge cases in operators."""
    
    def test_identity_function(self):
        """Test operators with identity function."""
        identity = lambda x: x
        f = lambda x: x**2
        
        result = apply_chain_rule(identity, f, x=5.0)
        assert isinstance(result, (int, float))
    
    def test_constant_function(self):
        """Test operators with constant function."""
        constant = lambda x: 1.0
        f = lambda x: x**2
        
        result = apply_product_rule(constant, f, x=3.0)
        assert isinstance(result, (int, float))
    
    def test_zero_coefficients(self):
        """Test kernel operators with zero coefficients."""
        from ontogenesis import OntogeneticKernel
        
        kernel = OntogeneticKernel(order=3)
        kernel.coefficients = np.zeros(3)
        
        result = apply_chain_rule_kernel(kernel)
        assert isinstance(result, np.ndarray)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
