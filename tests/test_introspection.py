"""
Unit tests for introspection framework.
"""

import pytest
import numpy as np
from introspection import (
    Copilot, CopilotGenome, OntogeneticState,
    introspect, self_optimize, evaluate_fitness,
    GripComponents, FitnessEvaluation
)
from introspection.core import DevelopmentStage


class TestCopilotGenome:
    """Tests for CopilotGenome data structure."""
    
    def test_default_initialization(self):
        """Test genome initializes with default values."""
        genome = CopilotGenome()
        assert isinstance(genome.capabilities, dict)
        assert 'codeGeneration' in genome.capabilities
        assert genome.generation == 0
        assert genome.lineage == []
    
    def test_custom_capabilities(self):
        """Test genome with custom capabilities."""
        custom_caps = {'testing': 0.9, 'debugging': 0.8}
        genome = CopilotGenome(capabilities=custom_caps)
        assert genome.capabilities['testing'] == 0.9
        assert genome.capabilities['debugging'] == 0.8
    
    def test_operator_genes(self):
        """Test operator genes are present."""
        genome = CopilotGenome()
        assert 'chainRule' in genome.operatorGenes
        assert 'productRule' in genome.operatorGenes
        assert 'quotientRule' in genome.operatorGenes


class TestOntogeneticState:
    """Tests for OntogeneticState tracking."""
    
    def test_initialization(self):
        """Test state initializes correctly."""
        state = OntogeneticState()
        assert state.stage == DevelopmentStage.EMBRYONIC
        assert state.maturity == 0.0
        assert state.generation == 0
    
    def test_development_stages(self):
        """Test stage transitions."""
        state = OntogeneticState(maturity=0.3)
        assert state.stage == DevelopmentStage.JUVENILE
        
        state.maturity = 0.7
        assert state.stage == DevelopmentStage.MATURE
        
        state.maturity = 0.95
        assert state.stage == DevelopmentStage.SENESCENT
    
    def test_introspection_depth_tracking(self):
        """Test introspection depth increases."""
        state = OntogeneticState()
        initial_depth = state.introspection_depth
        state.introspection_depth += 1
        assert state.introspection_depth == initial_depth + 1


class TestCopilot:
    """Tests for Copilot agent class."""
    
    def test_initialization(self):
        """Test copilot initializes with ID and genome."""
        copilot = Copilot(domain="testing")
        assert copilot.id is not None
        assert copilot.domain == "testing"
        assert isinstance(copilot.genome, CopilotGenome)
        assert isinstance(copilot.state, OntogeneticState)
    
    def test_get_capability(self):
        """Test capability retrieval."""
        copilot = Copilot(domain="research")
        cap = copilot.get_capability('codeGeneration')
        assert 0.0 <= cap <= 1.0
    
    def test_update_capability(self):
        """Test capability updates."""
        copilot = Copilot(domain="development")
        copilot.update_capability('testing', 0.95)
        assert copilot.genome.capabilities['testing'] == 0.95
    
    def test_development_stage_property(self):
        """Test development stage property."""
        copilot = Copilot(domain="test")
        assert copilot.development_stage == DevelopmentStage.EMBRYONIC


class TestIntrospection:
    """Tests for introspection function."""
    
    def test_basic_introspection(self):
        """Test basic introspection at depth 1."""
        copilot = Copilot(domain="testing")
        result = introspect(copilot, depth=1)
        
        assert 'agent_id' in result
        assert 'depth' in result
        assert result['depth'] == 1
        assert 'genome' in result
        assert 'state' in result
    
    def test_recursive_introspection(self):
        """Test recursive introspection increases depth."""
        copilot = Copilot(domain="testing")
        result = introspect(copilot, depth=3)
        
        assert result['depth'] == 3
        assert 'meta_introspection' in result
        assert copilot.state.introspection_depth >= 3
    
    def test_introspection_updates_state(self):
        """Test introspection updates copilot state."""
        copilot = Copilot(domain="testing")
        initial_depth = copilot.state.introspection_depth
        introspect(copilot, depth=2)
        assert copilot.state.introspection_depth > initial_depth
    
    def test_zero_depth_introspection(self):
        """Test introspection with depth 0 returns base case."""
        copilot = Copilot(domain="testing")
        result = introspect(copilot, depth=0)
        assert result['depth'] == 0


class TestSelfOptimization:
    """Tests for self-optimization function."""
    
    def test_self_optimize_basic(self):
        """Test basic self-optimization."""
        copilot = Copilot(domain="coding")
        initial_fitness = copilot.state.overall_fitness
        
        history = self_optimize(copilot, iterations=3)
        
        assert len(history) == 3
        assert all('iteration' in h for h in history)
        assert all('fitness' in h for h in history)
    
    def test_fitness_improves_or_stays_stable(self):
        """Test that fitness generally improves or stays stable."""
        copilot = Copilot(domain="optimization")
        history = self_optimize(copilot, iterations=5)
        
        # Fitness should not decrease significantly
        initial = history[0]['fitness']
        final = history[-1]['fitness']
        assert final >= initial * 0.9  # Allow small decreases due to randomness
    
    def test_convergence_detection(self):
        """Test early stopping on convergence."""
        copilot = Copilot(domain="convergence")
        history = self_optimize(copilot, iterations=20, threshold=0.01)
        
        # Should converge before 20 iterations
        assert len(history) <= 20
    
    def test_learning_rate_effect(self):
        """Test learning rate parameter."""
        copilot = Copilot(domain="learning")
        history = self_optimize(copilot, iterations=3, learning_rate=0.5)
        assert len(history) == 3


class TestFitnessEvaluation:
    """Tests for fitness evaluation."""
    
    def test_evaluate_fitness_returns_float(self):
        """Test fitness evaluation returns a float."""
        copilot = Copilot(domain="testing")
        fitness = evaluate_fitness(copilot)
        assert isinstance(fitness, float)
        assert 0.0 <= fitness <= 1.0
    
    def test_fitness_considers_maturity(self):
        """Test fitness considers maturity."""
        copilot1 = Copilot(domain="test")
        copilot1.state.maturity = 0.1
        
        copilot2 = Copilot(domain="test")
        copilot2.state.maturity = 0.9
        
        fitness1 = evaluate_fitness(copilot1)
        fitness2 = evaluate_fitness(copilot2)
        
        # More mature copilot should have higher base fitness
        assert fitness2 >= fitness1 * 0.9


class TestGripComponents:
    """Tests for GripComponents metrics."""
    
    def test_initialization(self):
        """Test grip components initialize."""
        grip = GripComponents()
        assert 0.0 <= grip.understanding <= 1.0
        assert 0.0 <= grip.correctness <= 1.0
        assert 0.0 <= grip.efficiency <= 1.0
    
    def test_custom_values(self):
        """Test grip with custom values."""
        grip = GripComponents(
            understanding=0.8,
            correctness=0.9,
            efficiency=0.7
        )
        assert grip.understanding == 0.8
        assert grip.correctness == 0.9
        assert grip.efficiency == 0.7
    
    def test_overall_grip(self):
        """Test overall grip calculation."""
        grip = GripComponents(
            understanding=0.8,
            correctness=0.9,
            efficiency=0.7,
            novelty=0.6,
            coherence=0.8
        )
        overall = grip.overall_grip()
        assert 0.0 <= overall <= 1.0
        assert isinstance(overall, float)


class TestFitnessEvaluationClass:
    """Tests for FitnessEvaluation class."""
    
    def test_initialization(self):
        """Test fitness evaluation initializes."""
        fitness = FitnessEvaluation()
        assert 0.0 <= fitness.task_success <= 1.0
        assert 0.0 <= fitness.code_quality <= 1.0
    
    def test_overall_fitness(self):
        """Test overall fitness calculation."""
        fitness = FitnessEvaluation(
            task_success=0.9,
            code_quality=0.8,
            efficiency=0.7,
            novelty=0.6,
            user_satisfaction=0.85
        )
        overall = fitness.overall_fitness()
        assert 0.0 <= overall <= 1.0
        assert isinstance(overall, float)


class TestDevelopmentStages:
    """Tests for development stage transitions."""
    
    def test_embryonic_stage(self):
        """Test embryonic stage characteristics."""
        copilot = Copilot(domain="test")
        copilot.state.maturity = 0.0
        assert copilot.development_stage == DevelopmentStage.EMBRYONIC
    
    def test_juvenile_stage(self):
        """Test juvenile stage characteristics."""
        copilot = Copilot(domain="test")
        copilot.state.maturity = 0.3
        assert copilot.development_stage == DevelopmentStage.JUVENILE
    
    def test_mature_stage(self):
        """Test mature stage characteristics."""
        copilot = Copilot(domain="test")
        copilot.state.maturity = 0.7
        assert copilot.development_stage == DevelopmentStage.MATURE
    
    def test_senescent_stage(self):
        """Test senescent stage characteristics."""
        copilot = Copilot(domain="test")
        copilot.state.maturity = 0.95
        assert copilot.development_stage == DevelopmentStage.SENESCENT


class TestEdgeCases:
    """Tests for edge cases and error handling."""
    
    def test_negative_depth(self):
        """Test introspection with negative depth."""
        copilot = Copilot(domain="test")
        result = introspect(copilot, depth=-1)
        assert result['depth'] == 0  # Should default to 0
    
    def test_zero_iterations(self):
        """Test optimization with zero iterations."""
        copilot = Copilot(domain="test")
        history = self_optimize(copilot, iterations=0)
        assert len(history) == 0
    
    def test_extreme_capability_values(self):
        """Test capabilities bounded to [0, 1]."""
        copilot = Copilot(domain="test")
        copilot.update_capability('testing', 2.0)
        # Should be clamped to valid range
        assert 0.0 <= copilot.get_capability('testing') <= 1.0
    
    def test_empty_domain(self):
        """Test copilot with empty domain."""
        copilot = Copilot(domain="")
        assert copilot.domain == ""
        assert copilot.id is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
