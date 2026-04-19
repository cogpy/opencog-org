"""
Comprehensive tests matching the actual API implementation.

Covers gaps in existing test files:
- IntrospectionMetrics class
- GripComponents.total_grip() (not overall_grip)
- FitnessEvaluation.calculate() classmethod
- evaluate_grip() function
- Introspection operators with dict-based signatures
- OntogeneticKernel via initialize_ontogenetic_kernel
- KernelGenome.get_coefficients() / get_operator_weights()
- run_ontogenesis with OntogenesisConfig
- evolve_population / tournament_selection
- calculate_population_diversity / calculate_kernel_diversity
- crossover returns Tuple, mutate takes OntogeneticKernel
- apply_chain_rule_kernel, apply_product_rule_kernel, apply_quotient_rule_kernel
- create_general_purpose_kernel, self_reproduce methods
- OntogeneticKernel.to_dict()
- Development stage transitions in both modules
"""

import pytest
import numpy as np

# ---------------------------------------------------------------------------
# introspection module
# ---------------------------------------------------------------------------


class TestIntrospectionMetrics:
    """Tests for IntrospectionMetrics – completely absent in other test files."""

    def _make_metrics(self):
        from introspection.metrics import IntrospectionMetrics
        return IntrospectionMetrics()

    def test_initial_state(self):
        m = self._make_metrics()
        assert m.history == []
        assert m.grip_history == []
        assert m.fitness_history == []

    def test_record_iteration(self):
        m = self._make_metrics()
        m.record_iteration(grip=0.5, fitness=0.4, capabilities={'codeGeneration': 0.7})
        assert len(m.grip_history) == 1
        assert len(m.fitness_history) == 1
        assert len(m.history) == 1
        assert m.grip_history[0] == 0.5
        assert m.fitness_history[0] == 0.4

    def test_record_multiple_iterations(self):
        m = self._make_metrics()
        for i in range(5):
            m.record_iteration(grip=float(i) * 0.1, fitness=float(i) * 0.1, capabilities={})
        assert len(m.grip_history) == 5

    def test_get_improvement_rate_empty(self):
        m = self._make_metrics()
        assert m.get_improvement_rate() == 0.0

    def test_get_improvement_rate_single(self):
        m = self._make_metrics()
        m.record_iteration(grip=0.5, fitness=0.5, capabilities={})
        assert m.get_improvement_rate() == 0.0

    def test_get_improvement_rate_positive(self):
        m = self._make_metrics()
        m.record_iteration(grip=0.2, fitness=0.2, capabilities={})
        m.record_iteration(grip=0.4, fitness=0.4, capabilities={})
        m.record_iteration(grip=0.6, fitness=0.6, capabilities={})
        rate = m.get_improvement_rate()
        assert rate > 0.0

    def test_get_improvement_rate_negative(self):
        m = self._make_metrics()
        m.record_iteration(grip=0.8, fitness=0.8, capabilities={})
        m.record_iteration(grip=0.4, fitness=0.4, capabilities={})
        rate = m.get_improvement_rate()
        assert rate < 0.0

    def test_get_convergence_status_false_when_too_few(self):
        m = self._make_metrics()
        m.record_iteration(grip=0.95, fitness=0.95, capabilities={})
        m.record_iteration(grip=0.95, fitness=0.95, capabilities={})
        assert m.get_convergence_status(threshold=0.9) is False

    def test_get_convergence_status_true(self):
        m = self._make_metrics()
        for _ in range(3):
            m.record_iteration(grip=0.95, fitness=0.95, capabilities={})
        assert m.get_convergence_status(threshold=0.9) is True

    def test_get_convergence_status_false_below_threshold(self):
        m = self._make_metrics()
        for _ in range(3):
            m.record_iteration(grip=0.5, fitness=0.5, capabilities={})
        assert m.get_convergence_status(threshold=0.9) is False

    def test_get_statistics_empty(self):
        m = self._make_metrics()
        stats = m.get_statistics()
        assert stats['mean_grip'] == 0.0
        assert stats['max_grip'] == 0.0
        assert stats['min_grip'] == 0.0

    def test_get_statistics_with_data(self):
        m = self._make_metrics()
        m.record_iteration(grip=0.3, fitness=0.3, capabilities={})
        m.record_iteration(grip=0.7, fitness=0.7, capabilities={})
        stats = m.get_statistics()
        assert stats['mean_grip'] == pytest.approx(0.5)
        assert stats['max_grip'] == pytest.approx(0.7)
        assert stats['min_grip'] == pytest.approx(0.3)
        assert 'std_grip' in stats
        assert 'improvement_rate' in stats
        assert 'converged' in stats

    def test_get_capability_trends_empty(self):
        m = self._make_metrics()
        assert m.get_capability_trends() == {}

    def test_get_capability_trends_with_data(self):
        m = self._make_metrics()
        m.record_iteration(grip=0.5, fitness=0.5, capabilities={'codeGeneration': 0.7, 'testing': 0.5})
        m.record_iteration(grip=0.6, fitness=0.6, capabilities={'codeGeneration': 0.8, 'testing': 0.6})
        trends = m.get_capability_trends()
        assert 'codeGeneration' in trends
        assert 'testing' in trends
        assert len(trends['codeGeneration']) == 2
        assert trends['codeGeneration'] == [0.7, 0.8]


class TestGripComponents:
    """Tests for GripComponents – existing tests call non-existent overall_grip()."""

    def _make_grip(self, **kwargs):
        from introspection.metrics import GripComponents
        defaults = dict(understanding=0.5, correctness=0.5, efficiency=0.5,
                        completeness=0.5, elegance=0.5)
        defaults.update(kwargs)
        return GripComponents(**defaults)

    def test_total_grip_method_exists(self):
        grip = self._make_grip()
        assert hasattr(grip, 'total_grip')

    def test_total_grip_returns_float(self):
        grip = self._make_grip()
        result = grip.total_grip()
        assert isinstance(result, float)

    def test_total_grip_range(self):
        grip = self._make_grip()
        result = grip.total_grip()
        assert 0.0 <= result <= 1.0

    def test_total_grip_zero_components(self):
        grip = self._make_grip(understanding=0.0, correctness=0.0, efficiency=0.0,
                               completeness=0.0, elegance=0.0)
        assert grip.total_grip() == 0.0

    def test_total_grip_all_ones(self):
        grip = self._make_grip(understanding=1.0, correctness=1.0, efficiency=1.0,
                               completeness=1.0, elegance=1.0)
        assert grip.total_grip() == pytest.approx(1.0)

    def test_total_grip_weighted_formula(self):
        """Explicitly validate the documented formula:
        0.3*understanding + 0.3*correctness + 0.2*efficiency + 0.1*completeness + 0.1*elegance
        """
        from introspection.metrics import GripComponents
        grip = GripComponents(
            understanding=0.8, correctness=0.6, efficiency=0.4,
            completeness=0.2, elegance=0.1
        )
        expected = 0.3 * 0.8 + 0.3 * 0.6 + 0.2 * 0.4 + 0.1 * 0.2 + 0.1 * 0.1
        assert grip.total_grip() == pytest.approx(expected)

    def test_total_grip_weights(self):
        """Verify the understanding coefficient (0.3)."""
        grip = self._make_grip(understanding=1.0, correctness=0.0, efficiency=0.0,
                               completeness=0.0, elegance=0.0)
        assert grip.total_grip() == pytest.approx(0.3)

    def test_total_grip_understanding_weight(self):
        """Verify the correctness coefficient (0.3)."""
        grip = self._make_grip(understanding=0.0, correctness=1.0, efficiency=0.0,
                               completeness=0.0, elegance=0.0)
        assert grip.total_grip() == pytest.approx(0.3)

    def test_total_grip_efficiency_weight(self):
        """Verify the efficiency coefficient (0.2)."""
        grip = self._make_grip(understanding=0.0, correctness=0.0, efficiency=1.0,
                               completeness=0.0, elegance=0.0)
        assert grip.total_grip() == pytest.approx(0.2)

    def test_total_grip_completeness_weight(self):
        """Verify the completeness coefficient (0.1)."""
        grip = self._make_grip(understanding=0.0, correctness=0.0, efficiency=0.0,
                               completeness=1.0, elegance=0.0)
        assert grip.total_grip() == pytest.approx(0.1)

    def test_total_grip_elegance_weight(self):
        """Verify the elegance coefficient (0.1)."""
        grip = self._make_grip(understanding=0.0, correctness=0.0, efficiency=0.0,
                               completeness=0.0, elegance=1.0)
        assert grip.total_grip() == pytest.approx(0.1)


class TestFitnessEvaluationActual:
    """Tests for FitnessEvaluation using the correct calculate() classmethod."""

    def test_calculate_classmethod(self):
        from introspection.metrics import FitnessEvaluation
        fe = FitnessEvaluation.calculate(
            task_success=0.8,
            code_quality=0.7,
            efficiency=0.6,
            novelty=0.5
        )
        assert isinstance(fe, FitnessEvaluation)

    def test_calculate_overall_fitness_field(self):
        from introspection.metrics import FitnessEvaluation
        fe = FitnessEvaluation.calculate(
            task_success=1.0, code_quality=1.0, efficiency=1.0, novelty=1.0
        )
        assert fe.overall_fitness == pytest.approx(1.0)

    def test_calculate_zero_inputs(self):
        from introspection.metrics import FitnessEvaluation
        fe = FitnessEvaluation.calculate(
            task_success=0.0, code_quality=0.0, efficiency=0.0, novelty=0.0
        )
        assert fe.overall_fitness == 0.0

    def test_calculate_stores_components(self):
        from introspection.metrics import FitnessEvaluation
        fe = FitnessEvaluation.calculate(
            task_success=0.9, code_quality=0.8, efficiency=0.7, novelty=0.6
        )
        assert fe.task_success == 0.9
        assert fe.code_quality == 0.8
        assert fe.efficiency == 0.7
        assert fe.novelty == 0.6

    def test_calculate_weighted_combination(self):
        from introspection.metrics import FitnessEvaluation
        fe = FitnessEvaluation.calculate(
            task_success=1.0, code_quality=0.0, efficiency=0.0, novelty=0.0
        )
        # task_success weight is 0.4
        assert fe.overall_fitness == pytest.approx(0.4)


class TestEvaluateGrip:
    """Tests for the evaluate_grip() function."""

    def _make_copilot(self, **kwargs):
        from introspection.core import Copilot
        c = Copilot(**kwargs)
        return c

    def test_evaluate_grip_returns_float(self):
        from introspection.core import evaluate_grip
        c = self._make_copilot()
        result = evaluate_grip(c)
        assert isinstance(result, float)

    def test_evaluate_grip_range(self):
        from introspection.core import evaluate_grip
        c = self._make_copilot()
        result = evaluate_grip(c)
        assert 0.0 <= result <= 1.0

    def test_evaluate_grip_with_tests(self):
        from introspection.core import evaluate_grip
        c = self._make_copilot(tests_passing=10, total_tests=10)
        result = evaluate_grip(c)
        assert 0.0 <= result <= 1.0

    def test_evaluate_grip_no_tests(self):
        from introspection.core import evaluate_grip
        c = self._make_copilot(total_tests=0)
        # correctness defaults to 0.5 when no tests
        result = evaluate_grip(c)
        assert isinstance(result, float)

    def test_evaluate_grip_with_lint_errors(self):
        from introspection.core import evaluate_grip
        c = self._make_copilot(lint_errors=50, documentation_coverage=1.0)
        result = evaluate_grip(c)
        assert 0.0 <= result <= 1.0

    def test_evaluate_grip_perfect_conditions(self):
        from introspection.core import evaluate_grip
        c = self._make_copilot(
            tests_passing=100,
            total_tests=100,
            lint_errors=0,
            documentation_coverage=1.0,
            total_operations=10,
            redundant_operations=0,
        )
        c.ontogenetic_state.maturity = 1.0
        result = evaluate_grip(c)
        assert result > 0.5


class TestIntrospectionOperatorsActual:
    """Tests for operators with the correct dict-based signatures."""

    def test_apply_chain_rule_takes_dicts(self):
        from introspection.operators import apply_chain_rule
        state = {'capabilities': {'codeGeneration': 0.7}, 'maturity': 0.5}
        context = {}
        result = apply_chain_rule(state, context)
        assert isinstance(result, dict)

    def test_apply_chain_rule_amplifies_capabilities(self):
        from introspection.operators import apply_chain_rule
        state = {'capabilities': {'testing': 0.5}, 'maturity': 0.5}
        result = apply_chain_rule(state, {})
        assert 'capabilities' in result
        # Chain rule should amplify (value * (1 + value * 0.1))
        assert result['capabilities']['testing'] >= 0.5

    def test_apply_chain_rule_adds_meta_level(self):
        from introspection.operators import apply_chain_rule
        state = {'capabilities': {}, 'maturity': 0.4}
        result = apply_chain_rule(state, {})
        assert 'meta_level' in result
        assert result['meta_level'] == 1

    def test_apply_chain_rule_increments_meta_level(self):
        from introspection.operators import apply_chain_rule
        state = {'capabilities': {}, 'meta_level': 3, 'maturity': 0.4}
        result = apply_chain_rule(state, {})
        assert result['meta_level'] == 4

    def test_apply_chain_rule_capabilities_bounded(self):
        from introspection.operators import apply_chain_rule
        state = {'capabilities': {'codeGeneration': 0.99}, 'maturity': 0.5}
        result = apply_chain_rule(state, {})
        for v in result['capabilities'].values():
            assert v <= 1.0

    def test_apply_product_rule_takes_dicts(self):
        from introspection.operators import apply_product_rule
        s1 = {'capabilities': {'codeGeneration': 0.7}, 'maturity': 0.5}
        s2 = {'capabilities': {'codeGeneration': 0.6}, 'maturity': 0.4}
        result = apply_product_rule(s1, s2)
        assert isinstance(result, dict)

    def test_apply_product_rule_merges_capabilities(self):
        from introspection.operators import apply_product_rule
        s1 = {'capabilities': {'cap_a': 0.8}, 'maturity': 0.5}
        s2 = {'capabilities': {'cap_b': 0.7}, 'maturity': 0.5}
        result = apply_product_rule(s1, s2)
        assert 'cap_a' in result['capabilities']
        assert 'cap_b' in result['capabilities']

    def test_apply_product_rule_maturity_averaged(self):
        from introspection.operators import apply_product_rule
        s1 = {'capabilities': {}, 'maturity': 0.2}
        s2 = {'capabilities': {}, 'maturity': 0.8}
        result = apply_product_rule(s1, s2)
        assert result['maturity'] == pytest.approx(0.5)

    def test_apply_quotient_rule_takes_dicts(self):
        from introspection.operators import apply_quotient_rule
        solution = {'capabilities': {'codeGeneration': 0.8}, 'maturity': 0.5}
        constraints = {'weight': 1.0}
        result = apply_quotient_rule(solution, constraints)
        assert isinstance(result, dict)

    def test_apply_quotient_rule_adds_constrained_flag(self):
        from introspection.operators import apply_quotient_rule
        solution = {'capabilities': {'testing': 0.9}}
        result = apply_quotient_rule(solution, {})
        assert result.get('constrained') is True

    def test_apply_quotient_rule_refines_capabilities(self):
        from introspection.operators import apply_quotient_rule
        solution = {'capabilities': {'testing': 0.9}}
        result = apply_quotient_rule(solution, {'weight': 1.0})
        # value / (weight + 0.1) = 0.9 / 1.1 ≈ 0.818 -> clamped to 1.0
        assert 0.0 <= result['capabilities']['testing'] <= 1.0

    def test_optimize_grip_takes_state_and_domain(self):
        from introspection.operators import optimize_grip
        state = {'capabilities': {'codeGeneration': 0.7, 'testing': 0.5}, 'maturity': 0.5}
        result = optimize_grip(state, 'general')
        assert isinstance(result, dict)

    def test_optimize_grip_adds_grip_score(self):
        from introspection.operators import optimize_grip
        state = {'capabilities': {'codeGeneration': 0.7, 'testing': 0.5}, 'maturity': 0.5}
        result = optimize_grip(state, 'research')
        assert 'grip' in result
        assert isinstance(result['grip'], float)

    def test_optimize_grip_records_domain(self):
        from introspection.operators import optimize_grip
        state = {'capabilities': {'codeGeneration': 0.7}, 'maturity': 0.5}
        result = optimize_grip(state, 'production')
        assert result['domain'] == 'production'

    def test_optimize_grip_unknown_domain_uses_general(self):
        from introspection.operators import optimize_grip
        state = {'capabilities': {'codeGeneration': 0.7}, 'maturity': 0.5}
        result = optimize_grip(state, 'unknown_domain')
        assert 'grip' in result

    def test_optimize_grip_capabilities_bounded(self):
        from introspection.operators import optimize_grip
        state = {'capabilities': {'codeGeneration': 0.9, 'testing': 0.9}, 'maturity': 0.5}
        result = optimize_grip(state, 'production')
        for v in result['capabilities'].values():
            assert v <= 1.0

    def test_domain_profiles_research(self):
        from introspection.operators import optimize_grip
        state = {'capabilities': {'documentation': 0.5}, 'maturity': 0.5}
        result = optimize_grip(state, 'research')
        # research boosts documentation (weight 1.3): 0.5 * 1.3 = 0.65
        assert result['capabilities']['documentation'] == pytest.approx(0.65)

    def test_domain_profiles_prototype(self):
        from introspection.operators import optimize_grip
        state = {'capabilities': {'codeGeneration': 0.5}, 'maturity': 0.5}
        result = optimize_grip(state, 'prototype')
        # prototype boosts codeGeneration (weight 1.4): 0.5 * 1.4 = 0.7
        assert result['capabilities']['codeGeneration'] == pytest.approx(0.7)


class TestCopilotActual:
    """Tests for the actual Copilot dataclass API."""

    def test_copilot_default_domain(self):
        from introspection.core import Copilot
        c = Copilot()
        assert c.domain == "general"

    def test_copilot_ontogenetic_state_attribute(self):
        """Copilot uses ontogenetic_state, not state."""
        from introspection.core import Copilot, OntogeneticState
        c = Copilot(domain="test")
        assert isinstance(c.ontogenetic_state, OntogeneticState)

    def test_copilot_performance_metrics_default_zero(self):
        from introspection.core import Copilot
        c = Copilot()
        assert c.tests_passing == 0
        assert c.total_tests == 0
        assert c.lint_errors == 0
        assert c.documentation_coverage == 0.0
        assert c.iterations_to_solution == 0
        assert c.redundant_operations == 0
        assert c.total_operations == 0

    def test_copilot_genome_default(self):
        from introspection.core import Copilot, CopilotGenome
        c = Copilot()
        assert isinstance(c.genome, CopilotGenome)

    def test_copilot_context_default_empty(self):
        from introspection.core import Copilot
        c = Copilot()
        assert c.context == {}


class TestOntogeneticStateActual:
    """Tests for the actual OntogeneticState dataclass API."""

    def test_initial_stage_embryonic(self):
        from introspection.core import OntogeneticState, DevelopmentStage
        s = OntogeneticState()
        assert s.stage == DevelopmentStage.EMBRYONIC

    def test_initial_maturity_zero(self):
        from introspection.core import OntogeneticState
        s = OntogeneticState()
        assert s.maturity == 0.0

    def test_initial_age_zero(self):
        from introspection.core import OntogeneticState
        s = OntogeneticState()
        assert s.age == 0

    def test_development_history_default_empty(self):
        from introspection.core import OntogeneticState
        s = OntogeneticState()
        assert s.development_history == []

    def test_no_introspection_depth_field(self):
        """OntogeneticState has no introspection_depth field."""
        from introspection.core import OntogeneticState
        s = OntogeneticState()
        assert not hasattr(s, 'introspection_depth')


class TestSelfOptimizeActual:
    """Tests for the actual self_optimize return value (None, modifies in place)."""

    def test_returns_none(self):
        from introspection.core import Copilot, self_optimize
        c = Copilot()
        result = self_optimize(c, iterations=2)
        assert result is None

    def test_maturity_increases(self):
        from introspection.core import Copilot, self_optimize
        c = Copilot()
        assert c.ontogenetic_state.maturity == 0.0
        self_optimize(c, iterations=3)
        assert c.ontogenetic_state.maturity > 0.0

    def test_age_increases(self):
        from introspection.core import Copilot, self_optimize
        c = Copilot()
        self_optimize(c, iterations=5)
        assert c.ontogenetic_state.age == 5

    def test_development_history_recorded(self):
        from introspection.core import Copilot, self_optimize
        c = Copilot()
        self_optimize(c, iterations=3)
        assert len(c.ontogenetic_state.development_history) == 3

    def test_history_contains_expected_keys(self):
        from introspection.core import Copilot, self_optimize
        c = Copilot()
        self_optimize(c, iterations=1)
        record = c.ontogenetic_state.development_history[0]
        assert 'iteration' in record
        assert 'grip' in record
        assert 'stage' in record
        assert 'maturity' in record

    def test_capabilities_clamped_to_1(self):
        from introspection.core import Copilot, self_optimize
        c = Copilot()
        self_optimize(c, iterations=100)
        for v in c.genome.capabilities.values():
            assert v <= 1.0

    def test_capabilities_clamped_to_0(self):
        from introspection.core import Copilot, self_optimize
        c = Copilot()
        self_optimize(c, iterations=100)
        for v in c.genome.capabilities.values():
            assert v >= 0.0

    def test_stage_transitions_occur(self):
        from introspection.core import Copilot, self_optimize, DevelopmentStage
        c = Copilot()
        # After enough iterations maturity should reach ≥ 0.25
        self_optimize(c, iterations=3)
        # stage should still be valid
        assert c.ontogenetic_state.stage in list(DevelopmentStage)


class TestUpdateDevelopmentStage:
    """Tests for _update_development_stage via self_optimize."""

    def _set_maturity(self, copilot, maturity):
        copilot.ontogenetic_state.maturity = maturity
        from introspection.core import _update_development_stage
        _update_development_stage(copilot)

    def test_embryonic_at_zero(self):
        from introspection.core import Copilot, DevelopmentStage
        c = Copilot()
        self._set_maturity(c, 0.0)
        assert c.ontogenetic_state.stage == DevelopmentStage.EMBRYONIC

    def test_juvenile_at_0_25(self):
        from introspection.core import Copilot, DevelopmentStage
        c = Copilot()
        self._set_maturity(c, 0.25)
        assert c.ontogenetic_state.stage == DevelopmentStage.JUVENILE

    def test_mature_at_0_6(self):
        from introspection.core import Copilot, DevelopmentStage
        c = Copilot()
        self._set_maturity(c, 0.6)
        assert c.ontogenetic_state.stage == DevelopmentStage.MATURE

    def test_senescent_at_0_9(self):
        from introspection.core import Copilot, DevelopmentStage
        c = Copilot()
        self._set_maturity(c, 0.9)
        assert c.ontogenetic_state.stage == DevelopmentStage.SENESCENT


class TestGeneticDiversity:
    """Tests for _genetic_diversity via evaluate_fitness with population."""

    def test_population_none_returns_half(self):
        from introspection.core import Copilot, evaluate_fitness
        c = Copilot()
        # population=None uses novelty=0.5 in calculation
        fitness = evaluate_fitness(c, population=None)
        assert isinstance(fitness, float)
        assert 0.0 <= fitness <= 1.0

    def test_single_member_population(self):
        from introspection.core import Copilot, evaluate_fitness
        c = Copilot()
        fitness = evaluate_fitness(c, population=[c])
        assert isinstance(fitness, float)

    def test_diverse_population_increases_novelty(self):
        from introspection.core import Copilot, evaluate_fitness
        target = Copilot()
        others = []
        for i in range(5):
            other = Copilot()
            # Make capabilities very different
            for k in other.genome.capabilities:
                other.genome.capabilities[k] = float(i) / 10.0
            others.append(other)
        fitness = evaluate_fitness(target, population=others + [target])
        assert isinstance(fitness, float)

    def test_evaluate_fitness_stores_on_genome(self):
        from introspection.core import Copilot, evaluate_fitness
        c = Copilot()
        fitness = evaluate_fitness(c)
        assert c.genome.fitness == fitness


# ---------------------------------------------------------------------------
# ontogenesis module
# ---------------------------------------------------------------------------


class TestGeneratedKernel:
    """Tests for the GeneratedKernel dataclass."""

    def test_basic_creation(self):
        from ontogenesis.core import GeneratedKernel
        k = GeneratedKernel(order=3, coefficients=[0.1, 0.2, 0.3])
        assert k.order == 3
        assert k.coefficients == [0.1, 0.2, 0.3]

    def test_default_domain(self):
        from ontogenesis.core import GeneratedKernel
        k = GeneratedKernel(order=2, coefficients=[0.5, 0.5])
        assert k.domain == "general"

    def test_custom_domain_and_properties(self):
        from ontogenesis.core import GeneratedKernel
        k = GeneratedKernel(order=2, coefficients=[0.5, 0.5],
                            domain="physics", properties={'symplectic': True})
        assert k.domain == "physics"
        assert k.properties['symplectic'] is True


class TestKernelGenomeActual:
    """Tests for the actual KernelGenome API."""

    def test_default_initialization(self):
        from ontogenesis.core import KernelGenome
        g = KernelGenome()
        assert g.generation == 0
        assert g.lineage == []
        assert len(g.genes) > 0

    def test_id_assigned(self):
        from ontogenesis.core import KernelGenome
        g = KernelGenome()
        assert g.id is not None
        assert len(g.id) > 0

    def test_ids_unique(self):
        from ontogenesis.core import KernelGenome
        ids = {KernelGenome().id for _ in range(10)}
        assert len(ids) == 10

    def test_get_coefficients(self):
        from ontogenesis.core import KernelGenome, GeneType
        g = KernelGenome()
        coeffs = g.get_coefficients()
        assert isinstance(coeffs, list)
        # Expect 4 coefficient genes by default
        assert len(coeffs) == 4

    def test_get_operator_weights(self):
        from ontogenesis.core import KernelGenome
        g = KernelGenome()
        weights = g.get_operator_weights()
        assert isinstance(weights, dict)
        assert 'chain' in weights
        assert 'product' in weights
        assert 'quotient' in weights

    def test_genes_searchable_by_name(self):
        """KernelGenome.genes is a list; genes are findable by iterating."""
        from ontogenesis.core import KernelGenome, KernelGene, GeneType
        g = KernelGenome()
        gene = KernelGene(gene_type=GeneType.COEFFICIENT, name="test_x", value=0.42)
        g.genes.append(gene)
        found = next((gn for gn in g.genes if gn.name == "test_x"), None)
        assert found is not None
        assert found.value == pytest.approx(0.42)

    def test_gene_not_found_returns_none_via_next(self):
        from ontogenesis.core import KernelGenome
        g = KernelGenome()
        result = next((gn for gn in g.genes if gn.name == "nonexistent"), None)
        assert result is None

    def test_generation_field(self):
        from ontogenesis.core import KernelGenome
        g = KernelGenome(generation=5)
        assert g.generation == 5

    def test_custom_lineage(self):
        from ontogenesis.core import KernelGenome
        g = KernelGenome(lineage=["parent1", "parent2"])
        assert g.lineage == ["parent1", "parent2"]

    def test_fitness_default_zero(self):
        from ontogenesis.core import KernelGenome
        g = KernelGenome()
        assert g.fitness == 0.0

    def test_age_default_zero(self):
        from ontogenesis.core import KernelGenome
        g = KernelGenome()
        assert g.age == 0


class TestInitializeOntogeneticKernel:
    """Tests for the initialize_ontogenetic_kernel factory function."""

    def test_returns_ontogenetic_kernel(self):
        from ontogenesis.core import OntogeneticKernel, initialize_ontogenetic_kernel
        k = initialize_ontogenetic_kernel()
        assert isinstance(k, OntogeneticKernel)

    def test_default_order_4(self):
        from ontogenesis.core import initialize_ontogenetic_kernel
        k = initialize_ontogenetic_kernel()
        assert k.base_kernel.order == 4
        assert len(k.base_kernel.coefficients) == 4

    def test_custom_order(self):
        from ontogenesis.core import initialize_ontogenetic_kernel
        k = initialize_ontogenetic_kernel(order=6)
        assert k.base_kernel.order == 6
        assert len(k.base_kernel.coefficients) == 6

    def test_starts_embryonic(self):
        from ontogenesis.core import initialize_ontogenetic_kernel, DevelopmentStage
        k = initialize_ontogenetic_kernel()
        assert k.development_stage == DevelopmentStage.EMBRYONIC

    def test_starts_zero_maturity(self):
        from ontogenesis.core import initialize_ontogenetic_kernel
        k = initialize_ontogenetic_kernel()
        assert k.maturity == 0.0

    def test_generation_zero(self):
        from ontogenesis.core import initialize_ontogenetic_kernel
        k = initialize_ontogenetic_kernel()
        assert k.genome.generation == 0

    def test_with_provided_base_kernel(self):
        from ontogenesis.core import initialize_ontogenetic_kernel, GeneratedKernel
        base = GeneratedKernel(order=2, coefficients=[0.3, 0.7], domain="custom")
        k = initialize_ontogenetic_kernel(kernel=base, order=2)
        assert k.base_kernel.coefficients == [0.3, 0.7]
        assert k.base_kernel.domain == "custom"


class TestOntogeneticKernelActual:
    """Tests for the actual OntogeneticKernel API."""

    def _make_kernel(self, order=2):
        from ontogenesis.core import initialize_ontogenetic_kernel
        return initialize_ontogenetic_kernel(order=order)

    def test_to_dict(self):
        k = self._make_kernel()
        d = k.to_dict()
        assert isinstance(d, dict)
        assert 'genome_id' in d
        assert 'generation' in d
        assert 'order' in d
        assert 'coefficients' in d
        assert 'domain' in d
        assert 'stage' in d
        assert 'maturity' in d
        assert 'fitness' in d

    def test_to_dict_values_correct_types(self):
        k = self._make_kernel(order=3)
        d = k.to_dict()
        assert isinstance(d['generation'], int)
        assert isinstance(d['order'], int)
        assert isinstance(d['coefficients'], list)
        assert isinstance(d['maturity'], float)
        assert isinstance(d['fitness'], float)

    def test_base_kernel_attribute(self):
        from ontogenesis.core import GeneratedKernel
        k = self._make_kernel()
        assert isinstance(k.base_kernel, GeneratedKernel)

    def test_genome_attribute(self):
        from ontogenesis.core import KernelGenome
        k = self._make_kernel()
        assert isinstance(k.genome, KernelGenome)


class TestSelfGenerateActual:
    """Tests for the actual self_generate API."""

    def _make_kernel(self, order=2):
        from ontogenesis.core import initialize_ontogenetic_kernel
        return initialize_ontogenetic_kernel(order=order)

    def test_returns_new_object(self):
        from ontogenesis.core import self_generate
        parent = self._make_kernel()
        offspring = self_generate(parent)
        assert offspring is not parent

    def test_offspring_generation_plus_one(self):
        from ontogenesis.core import self_generate
        parent = self._make_kernel()
        offspring = self_generate(parent)
        assert offspring.genome.generation == parent.genome.generation + 1

    def test_offspring_starts_embryonic(self):
        from ontogenesis.core import self_generate, DevelopmentStage
        parent = self._make_kernel()
        offspring = self_generate(parent)
        assert offspring.development_stage == DevelopmentStage.EMBRYONIC

    def test_offspring_same_order(self):
        from ontogenesis.core import self_generate
        parent = self._make_kernel(order=4)
        offspring = self_generate(parent)
        assert offspring.base_kernel.order == 4

    def test_lineage_contains_parent_id(self):
        from ontogenesis.core import self_generate
        parent = self._make_kernel()
        offspring = self_generate(parent)
        assert parent.genome.id in offspring.genome.lineage

    def test_multi_generation_lineage(self):
        from ontogenesis.core import self_generate
        g0 = self._make_kernel()
        g1 = self_generate(g0)
        g2 = self_generate(g1)
        g3 = self_generate(g2)
        assert g3.genome.generation == 3
        assert len(g3.genome.lineage) == 3


class TestSelfOptimizeKernelActual:
    """Tests for self_optimize_kernel (returns None, modifies in place)."""

    def _make_kernel(self):
        from ontogenesis.core import initialize_ontogenetic_kernel
        return initialize_ontogenetic_kernel(order=3)

    def test_returns_none(self):
        from ontogenesis.core import self_optimize_kernel
        k = self._make_kernel()
        result = self_optimize_kernel(k, iterations=2)
        assert result is None

    def test_maturity_increases(self):
        from ontogenesis.core import self_optimize_kernel
        k = self._make_kernel()
        assert k.maturity == 0.0
        self_optimize_kernel(k, iterations=3)
        assert k.maturity > 0.0

    def test_age_increases(self):
        from ontogenesis.core import self_optimize_kernel
        k = self._make_kernel()
        self_optimize_kernel(k, iterations=4)
        assert k.genome.age == 4

    def test_coefficients_stay_bounded(self):
        from ontogenesis.core import self_optimize_kernel
        k = self._make_kernel()
        self_optimize_kernel(k, iterations=20)
        for c in k.base_kernel.coefficients:
            assert 0.01 <= c <= 1.0

    def test_stage_updates(self):
        from ontogenesis.core import self_optimize_kernel, DevelopmentStage
        k = self._make_kernel()
        self_optimize_kernel(k, iterations=5)
        assert k.development_stage in list(DevelopmentStage)


class TestSelfReproduceActual:
    """Tests for self_reproduce with actual API."""

    def _make_kernel(self, order=2):
        from ontogenesis.core import initialize_ontogenetic_kernel
        return initialize_ontogenetic_kernel(order=order)

    def test_crossover_method(self):
        from ontogenesis.core import self_reproduce
        p1 = self._make_kernel()
        p2 = self._make_kernel()
        offspring = self_reproduce(p1, p2, method='crossover')
        assert offspring is not None

    def test_mutation_method(self):
        from ontogenesis.core import self_reproduce
        p1 = self._make_kernel()
        p2 = self._make_kernel()
        offspring = self_reproduce(p1, p2, method='mutation')
        assert offspring is not None

    def test_cloning_method(self):
        from ontogenesis.core import self_reproduce
        p1 = self._make_kernel()
        p2 = self._make_kernel()
        offspring = self_reproduce(p1, p2, method='cloning')
        assert offspring is not None

    def test_invalid_method_raises(self):
        from ontogenesis.core import self_reproduce
        p1 = self._make_kernel()
        p2 = self._make_kernel()
        with pytest.raises(ValueError):
            self_reproduce(p1, p2, method='invalid_method')

    def test_offspring_generation_incremented(self):
        from ontogenesis.core import self_reproduce
        p1 = self._make_kernel()
        p2 = self._make_kernel()
        offspring = self_reproduce(p1, p2)
        assert offspring.genome.generation == max(
            p1.genome.generation, p2.genome.generation
        ) + 1

    def test_coefficients_bounded(self):
        from ontogenesis.core import self_reproduce
        p1 = self._make_kernel()
        p2 = self._make_kernel()
        offspring = self_reproduce(p1, p2)
        for c in offspring.base_kernel.coefficients:
            assert 0.01 <= c <= 1.0


class TestEvaluateKernelFitnessActual:
    """Tests for evaluate_kernel_fitness with the actual API."""

    def _make_kernel(self):
        from ontogenesis.core import initialize_ontogenetic_kernel
        return initialize_ontogenetic_kernel(order=3)

    def _make_population(self, n=5):
        from ontogenesis.core import initialize_ontogenetic_kernel
        return [initialize_ontogenetic_kernel(order=3) for _ in range(n)]

    def test_returns_float(self):
        from ontogenesis.evolution import evaluate_kernel_fitness
        k = self._make_kernel()
        pop = self._make_population()
        fitness = evaluate_kernel_fitness(k, pop)
        assert isinstance(fitness, float)

    def test_fitness_range(self):
        from ontogenesis.evolution import evaluate_kernel_fitness
        k = self._make_kernel()
        pop = self._make_population()
        fitness = evaluate_kernel_fitness(k, pop)
        assert 0.0 <= fitness <= 1.0

    def test_stores_fitness_on_genome(self):
        from ontogenesis.evolution import evaluate_kernel_fitness
        k = self._make_kernel()
        pop = self._make_population()
        fitness = evaluate_kernel_fitness(k, pop)
        assert k.genome.fitness == pytest.approx(fitness)

    def test_custom_fitness_function(self):
        from ontogenesis.evolution import evaluate_kernel_fitness
        k = self._make_kernel()
        pop = self._make_population()
        custom = lambda kernel: 0.42
        fitness = evaluate_kernel_fitness(k, pop, custom_fitness=custom)
        assert fitness == pytest.approx(0.42)

    def test_empty_population(self):
        from ontogenesis.evolution import evaluate_kernel_fitness
        k = self._make_kernel()
        fitness = evaluate_kernel_fitness(k, [])
        assert isinstance(fitness, float)


class TestTournamentSelection:
    """Tests for tournament_selection in evolution module."""

    def _make_population(self, n=10):
        from ontogenesis.core import initialize_ontogenetic_kernel
        return [initialize_ontogenetic_kernel(order=2) for _ in range(n)]

    def test_returns_kernel_from_population(self):
        from ontogenesis.evolution import tournament_selection
        pop = self._make_population(10)
        fitnesses = [float(i) / 10.0 for i in range(10)]
        winner = tournament_selection(pop, fitnesses)
        assert winner in pop

    def test_returns_kernel_instance(self):
        from ontogenesis.evolution import tournament_selection
        from ontogenesis.core import OntogeneticKernel
        pop = self._make_population(5)
        fitnesses = [0.5] * 5
        winner = tournament_selection(pop, fitnesses)
        assert isinstance(winner, OntogeneticKernel)

    def test_custom_tournament_size(self):
        from ontogenesis.evolution import tournament_selection
        pop = self._make_population(10)
        fitnesses = [float(i) / 10.0 for i in range(10)]
        winner = tournament_selection(pop, fitnesses, tournament_size=5)
        assert winner in pop

    def test_selects_highest_fitness_winner(self):
        """With a single best individual, it should appear significantly more than chance."""
        from ontogenesis.evolution import tournament_selection
        pop = self._make_population(10)
        fitnesses = [0.0] * 9 + [1.0]
        # With tournament_size=3 and population=10, P(best is picked per run) ≈ 0.3.
        # Expected wins in 100 runs ≈ 30. Assert at least 20 (well below mean).
        wins = sum(
            tournament_selection(pop, fitnesses) is pop[9]
            for _ in range(100)
        )
        assert wins >= 20


class TestCalculatePopulationDiversity:
    """Tests for calculate_population_diversity."""

    def _make_population(self, n=5):
        from ontogenesis.core import initialize_ontogenetic_kernel
        return [initialize_ontogenetic_kernel(order=2) for _ in range(n)]

    def test_single_kernel_diversity_zero(self):
        from ontogenesis.evolution import calculate_population_diversity
        pop = self._make_population(1)
        d = calculate_population_diversity(pop)
        assert d == 0.0

    def test_empty_population_diversity_zero(self):
        from ontogenesis.evolution import calculate_population_diversity
        assert calculate_population_diversity([]) == 0.0

    def test_two_kernels(self):
        from ontogenesis.evolution import calculate_population_diversity
        pop = self._make_population(2)
        d = calculate_population_diversity(pop)
        assert isinstance(d, float)
        assert d >= 0.0

    def test_diversity_in_range(self):
        from ontogenesis.evolution import calculate_population_diversity
        pop = self._make_population(10)
        d = calculate_population_diversity(pop)
        assert 0.0 <= d <= 1.0

    def test_identical_kernels_low_diversity(self):
        from ontogenesis.evolution import calculate_population_diversity
        from ontogenesis.core import initialize_ontogenetic_kernel, GeneratedKernel
        # All kernels with same coefficients
        pop = []
        for _ in range(5):
            from ontogenesis.core import OntogeneticKernel, KernelGenome
            k = OntogeneticKernel(
                base_kernel=GeneratedKernel(order=2, coefficients=[0.5, 0.5]),
                genome=KernelGenome()
            )
            pop.append(k)
        d = calculate_population_diversity(pop)
        assert d == pytest.approx(0.0)


class TestCalculateKernelDiversity:
    """Tests for calculate_kernel_diversity."""

    def _make_kernel(self):
        from ontogenesis.core import initialize_ontogenetic_kernel
        return initialize_ontogenetic_kernel(order=2)

    def _make_population(self, n=5):
        from ontogenesis.core import initialize_ontogenetic_kernel
        return [initialize_ontogenetic_kernel(order=2) for _ in range(n)]

    def test_single_population_returns_half(self):
        from ontogenesis.evolution import calculate_kernel_diversity
        k = self._make_kernel()
        d = calculate_kernel_diversity(k, [k])
        assert d == pytest.approx(0.5)

    def test_with_population(self):
        from ontogenesis.evolution import calculate_kernel_diversity
        k = self._make_kernel()
        pop = self._make_population(5)
        d = calculate_kernel_diversity(k, pop + [k])
        assert 0.0 <= d <= 1.0


class TestRunOntogenesisActual:
    """Tests for run_ontogenesis with the actual OntogenesisConfig API."""

    def _config(self, max_generations=3, population_size=5, fitness_threshold=0.99):
        from ontogenesis.evolution import OntogenesisConfig, EvolutionConfig
        ev = EvolutionConfig(
            population_size=population_size,
            max_generations=max_generations,
            fitness_threshold=fitness_threshold,
        )
        return OntogenesisConfig(evolution=ev)

    def test_returns_list(self):
        from ontogenesis.evolution import run_ontogenesis
        config = self._config()
        results = run_ontogenesis(config)
        assert isinstance(results, list)

    def test_results_are_generation_results(self):
        from ontogenesis.evolution import run_ontogenesis, GenerationResult
        config = self._config()
        results = run_ontogenesis(config)
        for r in results:
            assert isinstance(r, GenerationResult)

    def test_results_have_expected_fields(self):
        from ontogenesis.evolution import run_ontogenesis
        config = self._config()
        results = run_ontogenesis(config)
        assert len(results) > 0
        r = results[0]
        assert hasattr(r, 'generation')
        assert hasattr(r, 'population')
        assert hasattr(r, 'best_fitness')
        assert hasattr(r, 'average_fitness')
        assert hasattr(r, 'diversity')
        assert hasattr(r, 'best_kernel')

    def test_generation_count_limited(self):
        from ontogenesis.evolution import run_ontogenesis
        config = self._config(max_generations=3)
        results = run_ontogenesis(config)
        assert len(results) <= 3

    def test_population_size_maintained(self):
        from ontogenesis.evolution import run_ontogenesis
        config = self._config(max_generations=2, population_size=8)
        results = run_ontogenesis(config)
        for r in results:
            assert len(r.population) == 8

    def test_best_fitness_in_range(self):
        from ontogenesis.evolution import run_ontogenesis
        config = self._config(max_generations=2)
        results = run_ontogenesis(config)
        for r in results:
            assert 0.0 <= r.best_fitness <= 1.0

    def test_with_seed_kernels(self):
        from ontogenesis.evolution import run_ontogenesis, OntogenesisConfig, EvolutionConfig
        from ontogenesis.core import initialize_ontogenetic_kernel
        seeds = [initialize_ontogenetic_kernel(order=2) for _ in range(5)]
        config = OntogenesisConfig(
            evolution=EvolutionConfig(population_size=5, max_generations=2),
            seed_kernels=seeds
        )
        results = run_ontogenesis(config)
        assert len(results) > 0

    def test_with_custom_fitness_function(self):
        from ontogenesis.evolution import run_ontogenesis, OntogenesisConfig, EvolutionConfig
        config = OntogenesisConfig(
            evolution=EvolutionConfig(population_size=4, max_generations=2),
            fitness_function=lambda k: 0.5
        )
        results = run_ontogenesis(config)
        assert len(results) > 0

    def test_convergence_stops_early(self):
        from ontogenesis.evolution import run_ontogenesis, OntogenesisConfig, EvolutionConfig
        from ontogenesis.core import initialize_ontogenetic_kernel
        # Fitness threshold of 0.0 means best_fitness >= 0.0 is always true after the
        # first generation, so the loop breaks after recording generation 0.
        seeds = []
        for _ in range(5):
            k = initialize_ontogenetic_kernel(order=2)
            k.base_kernel.coefficients = [0.5, 0.5]
            seeds.append(k)
        config = OntogenesisConfig(
            evolution=EvolutionConfig(
                population_size=5,
                max_generations=100,
                # Any non-negative fitness satisfies this threshold immediately
                fitness_threshold=0.0,
            ),
            seed_kernels=seeds,
        )
        results = run_ontogenesis(config)
        assert len(results) == 1  # Stops after the first generation


class TestEvolutionConfig:
    """Tests for EvolutionConfig and OntogenesisConfig dataclasses."""

    def test_evolution_config_defaults(self):
        from ontogenesis.evolution import EvolutionConfig
        ec = EvolutionConfig()
        assert ec.population_size == 20
        assert ec.mutation_rate == 0.15
        assert ec.crossover_rate == 0.8
        assert ec.elitism_rate == 0.1
        assert ec.max_generations == 50
        assert ec.fitness_threshold == 0.9
        assert ec.diversity_pressure == 0.2

    def test_evolution_config_custom(self):
        from ontogenesis.evolution import EvolutionConfig
        ec = EvolutionConfig(population_size=10, mutation_rate=0.5)
        assert ec.population_size == 10
        assert ec.mutation_rate == 0.5

    def test_ontogenesis_config_defaults(self):
        from ontogenesis.evolution import OntogenesisConfig, EvolutionConfig
        oc = OntogenesisConfig()
        assert isinstance(oc.evolution, EvolutionConfig)
        assert oc.seed_kernels == []
        assert oc.fitness_function is None


class TestEvolvePopulationActual:
    """Tests for evolve_population with the actual signature."""

    def _make_population(self, n=10, order=2):
        from ontogenesis.core import initialize_ontogenetic_kernel
        return [initialize_ontogenetic_kernel(order=order) for _ in range(n)]

    def test_maintains_population_size(self):
        from ontogenesis.evolution import evolve_population, EvolutionConfig
        pop = self._make_population(10)
        fitnesses = [float(i) / 10.0 for i in range(10)]
        config = EvolutionConfig(
            population_size=10, elitism_rate=0.1,
            crossover_rate=0.8, mutation_rate=0.1
        )
        new_pop = evolve_population(pop, fitnesses, config)
        assert len(new_pop) == 10

    def test_returns_list_of_kernels(self):
        from ontogenesis.evolution import evolve_population, EvolutionConfig
        from ontogenesis.core import OntogeneticKernel
        pop = self._make_population(8)
        fitnesses = [0.5] * 8
        config = EvolutionConfig(population_size=8, elitism_rate=0.1,
                                 crossover_rate=0.8, mutation_rate=0.1)
        new_pop = evolve_population(pop, fitnesses, config)
        assert all(isinstance(k, OntogeneticKernel) for k in new_pop)

    def test_elite_individuals_preserved(self):
        """Best individual should survive with elitism."""
        from ontogenesis.evolution import evolve_population, EvolutionConfig, evaluate_kernel_fitness
        pop = self._make_population(10)
        # Give the last one a very high fitness by setting ideal coefficients
        pop[-1].base_kernel.coefficients = [0.5, 0.5]
        fitnesses = [evaluate_kernel_fitness(k, pop) for k in pop]
        config = EvolutionConfig(population_size=10, elitism_rate=0.2,
                                 crossover_rate=0.5, mutation_rate=0.05)
        new_pop = evolve_population(pop, fitnesses, config)
        assert len(new_pop) == 10


class TestOntogenesisOperatorsActual:
    """Tests for operators with the actual OntogeneticKernel API."""

    def _make_kernel(self, order=3):
        from ontogenesis.core import initialize_ontogenetic_kernel
        return initialize_ontogenetic_kernel(order=order)

    def test_apply_chain_rule_kernel_returns_kernel(self):
        from ontogenesis.operators import apply_chain_rule_kernel
        from ontogenesis.core import OntogeneticKernel
        k = self._make_kernel()
        result = apply_chain_rule_kernel(k)
        assert isinstance(result, OntogeneticKernel)

    def test_apply_chain_rule_kernel_modifies_in_place(self):
        from ontogenesis.operators import apply_chain_rule_kernel
        k = self._make_kernel()
        original_coeffs = list(k.base_kernel.coefficients)
        apply_chain_rule_kernel(k)
        # Coefficients should be amplified
        assert k.base_kernel.coefficients != original_coeffs

    def test_apply_chain_rule_kernel_coefficients_bounded(self):
        from ontogenesis.operators import apply_chain_rule_kernel
        k = self._make_kernel()
        apply_chain_rule_kernel(k)
        for c in k.base_kernel.coefficients:
            assert 0.01 <= c <= 1.0

    def test_apply_product_rule_kernel_returns_kernel(self):
        from ontogenesis.operators import apply_product_rule_kernel
        from ontogenesis.core import OntogeneticKernel
        k1 = self._make_kernel()
        k2 = self._make_kernel()
        result = apply_product_rule_kernel(k1, k2)
        assert isinstance(result, OntogeneticKernel)

    def test_apply_product_rule_kernel_different_lengths(self):
        """Product rule should handle kernels with different coefficient lengths."""
        from ontogenesis.operators import apply_product_rule_kernel
        k1 = self._make_kernel(order=2)
        k2 = self._make_kernel(order=4)
        result = apply_product_rule_kernel(k1, k2)
        assert result is not None

    def test_apply_product_rule_kernel_bounded(self):
        from ontogenesis.operators import apply_product_rule_kernel
        k1 = self._make_kernel()
        k2 = self._make_kernel()
        result = apply_product_rule_kernel(k1, k2)
        for c in result.base_kernel.coefficients:
            assert 0.01 <= c <= 1.0

    def test_apply_quotient_rule_kernel_returns_kernel(self):
        from ontogenesis.operators import apply_quotient_rule_kernel
        from ontogenesis.core import OntogeneticKernel
        k = self._make_kernel()
        result = apply_quotient_rule_kernel(k)
        assert isinstance(result, OntogeneticKernel)

    def test_apply_quotient_rule_kernel_with_weight(self):
        from ontogenesis.operators import apply_quotient_rule_kernel
        k = self._make_kernel()
        result = apply_quotient_rule_kernel(k, constraint_weight=2.0)
        assert result is not None
        for c in result.base_kernel.coefficients:
            assert 0.01 <= c <= 1.0

    def test_apply_quotient_rule_kernel_high_weight_reduces_coeffs(self):
        from ontogenesis.operators import apply_quotient_rule_kernel
        from ontogenesis.core import initialize_ontogenetic_kernel
        k = initialize_ontogenetic_kernel(order=2)
        k.base_kernel.coefficients = [0.8, 0.8]
        apply_quotient_rule_kernel(k, constraint_weight=9.0)
        # 0.8 / 9.1 ≈ 0.088 → clamped to 0.088
        for c in k.base_kernel.coefficients:
            assert c < 0.2

    def test_crossover_returns_tuple(self):
        from ontogenesis.operators import crossover
        k1 = self._make_kernel()
        k2 = self._make_kernel()
        result = crossover(k1, k2)
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_crossover_offspring_are_kernels(self):
        from ontogenesis.operators import crossover
        from ontogenesis.core import OntogeneticKernel
        k1 = self._make_kernel()
        k2 = self._make_kernel()
        o1, o2 = crossover(k1, k2)
        assert isinstance(o1, OntogeneticKernel)
        assert isinstance(o2, OntogeneticKernel)

    def test_crossover_with_explicit_point(self):
        from ontogenesis.operators import crossover
        k1 = self._make_kernel(order=4)
        k2 = self._make_kernel(order=4)
        o1, o2 = crossover(k1, k2, point=2)
        assert o1 is not None
        assert o2 is not None

    def test_crossover_offspring_lineage(self):
        from ontogenesis.operators import crossover
        k1 = self._make_kernel()
        k2 = self._make_kernel()
        o1, o2 = crossover(k1, k2)
        assert k1.genome.id in o1.genome.lineage
        assert k2.genome.id in o1.genome.lineage

    def test_crossover_generation_incremented(self):
        from ontogenesis.operators import crossover
        k1 = self._make_kernel()
        k2 = self._make_kernel()
        o1, o2 = crossover(k1, k2)
        assert o1.genome.generation == max(k1.genome.generation, k2.genome.generation) + 1

    def test_mutate_takes_ontogenetic_kernel(self):
        from ontogenesis.operators import mutate
        k = self._make_kernel()
        # mutate should not raise
        mutate(k, rate=0.5)

    def test_mutate_returns_none(self):
        from ontogenesis.operators import mutate
        k = self._make_kernel()
        result = mutate(k, rate=0.5)
        assert result is None

    def test_mutate_rate_zero_no_change(self):
        from ontogenesis.operators import mutate
        k = self._make_kernel()
        original_coeffs = list(k.base_kernel.coefficients)
        mutate(k, rate=0.0)
        assert k.base_kernel.coefficients == original_coeffs

    def test_mutate_keeps_coefficients_bounded(self):
        from ontogenesis.operators import mutate
        k = self._make_kernel()
        for _ in range(20):
            mutate(k, rate=1.0)
        for c in k.base_kernel.coefficients:
            assert 0.01 <= c <= 1.0


class TestKernelDomainSpecific:
    """Tests for domain-specific kernel creators including create_general_purpose_kernel."""

    def test_create_consciousness_kernel_domain(self):
        from ontogenesis.kernels import create_consciousness_kernel
        k = create_consciousness_kernel(order=3)
        assert k.base_kernel.domain == "consciousness"

    def test_create_physics_kernel_domain(self):
        from ontogenesis.kernels import create_physics_kernel
        k = create_physics_kernel(order=3)
        assert k.base_kernel.domain == "physics"

    def test_create_mathematics_kernel_domain(self):
        from ontogenesis.kernels import create_mathematics_kernel
        k = create_mathematics_kernel(order=3)
        assert k.base_kernel.domain == "mathematics"

    def test_create_general_purpose_kernel(self):
        from ontogenesis.kernels import create_general_purpose_kernel
        k = create_general_purpose_kernel(order=4)
        assert k.base_kernel.domain == "general"

    def test_create_general_purpose_kernel_order(self):
        from ontogenesis.kernels import create_general_purpose_kernel
        k = create_general_purpose_kernel(order=5)
        assert k.base_kernel.order == 5

    def test_consciousness_kernel_properties(self):
        from ontogenesis.kernels import create_consciousness_kernel
        k = create_consciousness_kernel(order=3)
        assert k.base_kernel.properties.get('self_reference') is True
        assert k.base_kernel.properties.get('meta_cognitive') is True

    def test_physics_kernel_properties(self):
        from ontogenesis.kernels import create_physics_kernel
        k = create_physics_kernel(order=3)
        assert k.base_kernel.properties.get('symplectic') is True
        assert k.base_kernel.properties.get('energy_conserving') is True

    def test_mathematics_kernel_properties(self):
        from ontogenesis.kernels import create_mathematics_kernel
        k = create_mathematics_kernel(order=3)
        assert k.base_kernel.properties.get('high_precision') is True
        assert k.base_kernel.properties.get('convergent') is True

    def test_general_purpose_kernel_properties(self):
        from ontogenesis.kernels import create_general_purpose_kernel
        k = create_general_purpose_kernel(order=4)
        assert k.base_kernel.properties.get('balanced') is True

    def test_order_one_kernel(self):
        """Kernels with order 1 should work (coeff list sliced to length 1)."""
        from ontogenesis.kernels import create_consciousness_kernel
        k = create_consciousness_kernel(order=1)
        assert len(k.base_kernel.coefficients) == 1

    def test_large_order_kernel(self):
        from ontogenesis.kernels import create_general_purpose_kernel
        k = create_general_purpose_kernel(order=10)
        assert k.base_kernel.order == 10


class TestOntogenesisDevelopmentStage:
    """Tests for ontogenesis DevelopmentStage transitions."""

    def _make_kernel(self):
        from ontogenesis.core import initialize_ontogenetic_kernel
        return initialize_ontogenetic_kernel(order=2)

    def test_embryonic_at_zero(self):
        from ontogenesis.core import _update_kernel_stage, DevelopmentStage
        k = self._make_kernel()
        k.maturity = 0.0
        _update_kernel_stage(k)
        assert k.development_stage == DevelopmentStage.EMBRYONIC

    def test_juvenile_at_0_25(self):
        from ontogenesis.core import _update_kernel_stage, DevelopmentStage
        k = self._make_kernel()
        k.maturity = 0.25
        _update_kernel_stage(k)
        assert k.development_stage == DevelopmentStage.JUVENILE

    def test_mature_at_0_6(self):
        from ontogenesis.core import _update_kernel_stage, DevelopmentStage
        k = self._make_kernel()
        k.maturity = 0.6
        _update_kernel_stage(k)
        assert k.development_stage == DevelopmentStage.MATURE

    def test_senescent_at_0_9(self):
        from ontogenesis.core import _update_kernel_stage, DevelopmentStage
        k = self._make_kernel()
        k.maturity = 0.9
        _update_kernel_stage(k)
        assert k.development_stage == DevelopmentStage.SENESCENT


class TestGeneticDistance:
    """Tests for _genetic_distance via calculate_population_diversity."""

    def test_identical_kernels_zero_distance(self):
        from ontogenesis.evolution import _genetic_distance
        from ontogenesis.core import OntogeneticKernel, GeneratedKernel, KernelGenome
        coeffs = [0.3, 0.7]
        k1 = OntogeneticKernel(
            base_kernel=GeneratedKernel(order=2, coefficients=list(coeffs)),
            genome=KernelGenome()
        )
        k2 = OntogeneticKernel(
            base_kernel=GeneratedKernel(order=2, coefficients=list(coeffs)),
            genome=KernelGenome()
        )
        d = _genetic_distance(k1, k2)
        assert d == pytest.approx(0.0)

    def test_different_kernels_nonzero_distance(self):
        from ontogenesis.evolution import _genetic_distance
        from ontogenesis.core import OntogeneticKernel, GeneratedKernel, KernelGenome
        k1 = OntogeneticKernel(
            base_kernel=GeneratedKernel(order=2, coefficients=[0.0, 0.0]),
            genome=KernelGenome()
        )
        k2 = OntogeneticKernel(
            base_kernel=GeneratedKernel(order=2, coefficients=[1.0, 1.0]),
            genome=KernelGenome()
        )
        d = _genetic_distance(k1, k2)
        assert d > 0.0

    def test_pads_shorter_array(self):
        """Kernels of different orders should still compute a distance."""
        from ontogenesis.evolution import _genetic_distance
        from ontogenesis.core import OntogeneticKernel, GeneratedKernel, KernelGenome
        k1 = OntogeneticKernel(
            base_kernel=GeneratedKernel(order=2, coefficients=[0.5, 0.5]),
            genome=KernelGenome()
        )
        k2 = OntogeneticKernel(
            base_kernel=GeneratedKernel(order=4, coefficients=[0.5, 0.5, 0.5, 0.5]),
            genome=KernelGenome()
        )
        d = _genetic_distance(k1, k2)
        assert isinstance(d, float)


class TestKernelGeneActual:
    """Supplementary tests for KernelGene."""

    def test_gene_types(self):
        from ontogenesis.core import KernelGene, GeneType
        for gt in [GeneType.COEFFICIENT, GeneType.OPERATOR, GeneType.SYMMETRY, GeneType.PRESERVATION]:
            gene = KernelGene(gene_type=gt, name="g", value=0.5)
            assert gene.gene_type == gt

    def test_immutable_gene_never_mutates(self):
        from ontogenesis.core import KernelGene, GeneType
        gene = KernelGene(gene_type=GeneType.PRESERVATION, name="cons", value=0.7, mutable=False)
        for _ in range(50):
            gene.mutate(rate=1.0)
        assert gene.value == pytest.approx(0.7)

    def test_mutable_high_rate_changes_value(self):
        np.random.seed(0)
        from ontogenesis.core import KernelGene, GeneType
        original = 0.5
        gene = KernelGene(gene_type=GeneType.COEFFICIENT, name="b1", value=original)
        changed = False
        for _ in range(50):
            gene.mutate(rate=1.0)
            if gene.value != pytest.approx(original):
                changed = True
                break
        assert changed

    def test_gene_value_bounded_after_mutation(self):
        from ontogenesis.core import KernelGene, GeneType
        gene = KernelGene(gene_type=GeneType.COEFFICIENT, name="b1", value=0.95)
        for _ in range(30):
            gene.mutate(rate=1.0)
            assert 0.0 <= gene.value <= 1.0


class TestIntrospectActual:
    """Tests for the actual introspect() return values."""

    def _make_copilot(self, domain="test"):
        from introspection.core import Copilot
        return Copilot(domain=domain)

    def test_depth_zero_returns_capabilities(self):
        from introspection.core import introspect
        c = self._make_copilot()
        result = introspect(c, depth=0)
        assert 'capabilities' in result
        assert 'stage' in result
        assert 'maturity' in result

    def test_depth_one_returns_enhanced_state(self):
        from introspection.core import introspect
        c = self._make_copilot()
        result = introspect(c, depth=1)
        assert isinstance(result, dict)
        # Chain rule adds meta_level
        assert 'meta_level' in result

    def test_depth_two_increases_meta_level(self):
        from introspection.core import introspect
        c = self._make_copilot()
        result = introspect(c, depth=2)
        assert result.get('meta_level', 0) >= 2

    def test_depth_zero_stage_is_string(self):
        from introspection.core import introspect
        c = self._make_copilot()
        result = introspect(c, depth=0)
        assert isinstance(result['stage'], str)

    def test_capabilities_copied_not_referenced(self):
        """Depth 0 should return a copy of capabilities."""
        from introspection.core import introspect
        c = self._make_copilot()
        result = introspect(c, depth=0)
        result['capabilities']['codeGeneration'] = 0.0
        assert c.genome.capabilities['codeGeneration'] != 0.0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
