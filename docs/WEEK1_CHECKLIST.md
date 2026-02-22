# Week 1 Action Checklist - Testing & CI/CD

## Overview
This checklist breaks down the first week's priorities into concrete, actionable tasks. Each task is designed to take 1-4 hours and can be completed independently.

---

## 🎯 Day 1-2: Unit Test Suite Foundation

### Task 1.1: Set Up Testing Infrastructure (1 hour)
- [ ] Create `tests/` directory structure
  ```bash
  mkdir -p opencog-org/tests
  cd opencog-org/tests
  ```
- [ ] Create `tests/__init__.py`
  ```python
  """
  Test suite for introspection and ontogenesis frameworks.
  """
  __version__ = "0.1.0"
  ```
- [ ] Create `tests/conftest.py` for pytest fixtures
  ```python
  """Shared pytest fixtures."""
  import pytest
  import numpy as np
  from introspection import Copilot, CopilotGenome
  from ontogenesis import OntogeneticKernel, KernelGenome
  
  @pytest.fixture
  def sample_copilot():
      """Create a sample copilot for testing."""
      return Copilot(domain="test", capabilities=np.random.rand(5))
  
  @pytest.fixture
  def sample_kernel():
      """Create a sample kernel for testing."""
      return OntogeneticKernel(order=3, kernel_type="consciousness")
  ```
- [ ] Create `requirements-dev.txt`
  ```
  pytest>=7.0.0
  pytest-cov>=4.0.0
  pytest-xdist>=3.0.0  # For parallel testing
  pytest-timeout>=2.1.0  # For timeout handling
  black>=22.0.0
  mypy>=0.990
  flake8>=5.0.0
  ```
- [ ] Install dev dependencies
  ```bash
  pip3 install -r requirements-dev.txt
  ```

**Expected Output**: Testing infrastructure ready to use

---

### Task 1.2: Introspection Unit Tests - Core (2 hours)

Create `tests/test_introspection.py`:

```python
"""Unit tests for introspection framework."""

import pytest
import numpy as np
from introspection import (
    Copilot, CopilotGenome, OntogeneticState,
    introspect, self_optimize, evaluate_fitness
)
from introspection.metrics import GripComponents


class TestCopilotGenome:
    """Tests for CopilotGenome class."""
    
    def test_genome_initialization(self):
        """Test genome creates with valid structure."""
        genome = CopilotGenome(
            capabilities=np.array([0.5, 0.6, 0.7]),
            domain="research"
        )
        assert genome.id is not None
        assert len(genome.capabilities) == 3
        assert genome.domain == "research"
        assert hasattr(genome, 'generation')
    
    def test_genome_mutation(self):
        """Test genome mutation produces valid offspring."""
        genome = CopilotGenome(capabilities=np.array([0.5, 0.5, 0.5]))
        mutated = genome.mutate(rate=0.1)
        
        assert len(mutated.capabilities) == len(genome.capabilities)
        assert not np.array_equal(mutated.capabilities, genome.capabilities)
        assert mutated.generation == genome.generation + 1
        assert mutated.parent_ids == [genome.id]
    
    def test_genome_crossover(self):
        """Test genome crossover combines parents."""
        genome1 = CopilotGenome(capabilities=np.array([1.0, 1.0, 1.0]))
        genome2 = CopilotGenome(capabilities=np.array([0.0, 0.0, 0.0]))
        
        offspring = genome1.crossover(genome2)
        
        assert len(offspring.capabilities) == len(genome1.capabilities)
        assert offspring.generation == max(genome1.generation, genome2.generation) + 1
        assert set(offspring.parent_ids) == {genome1.id, genome2.id}
        # Offspring should have mix of parent capabilities
        assert np.any(offspring.capabilities != genome1.capabilities)
        assert np.any(offspring.capabilities != genome2.capabilities)


class TestOntogeneticState:
    """Tests for OntogeneticState class."""
    
    def test_state_initialization(self):
        """Test state initializes to embryonic."""
        state = OntogeneticState()
        assert state.stage == "embryonic"
        assert state.maturity == 0.0
        assert state.age == 0
    
    def test_state_advancement(self):
        """Test state advances through stages."""
        state = OntogeneticState()
        
        state.advance(delta_maturity=0.3)
        assert state.stage == "juvenile"
        assert state.maturity == 0.3
        assert state.age == 1
        
        state.advance(delta_maturity=0.4)
        assert state.stage == "mature"
        assert state.maturity == 0.7
        
        state.advance(delta_maturity=0.3)
        assert state.stage == "senescent"
        assert state.maturity == 1.0  # Capped at 1.0


class TestCopilot:
    """Tests for Copilot class."""
    
    def test_copilot_initialization(self, sample_copilot):
        """Test copilot initializes correctly."""
        assert sample_copilot.genome is not None
        assert sample_copilot.state.stage == "embryonic"
        assert sample_copilot.domain == "test"
    
    def test_copilot_introspection_depth_1(self, sample_copilot):
        """Test single-level introspection."""
        result = introspect(sample_copilot, depth=1)
        
        assert 'depth' in result
        assert result['depth'] == 1
        assert 'metrics' in result
        assert 'grip' in result['metrics']
    
    def test_copilot_introspection_depth_3(self, sample_copilot):
        """Test recursive introspection."""
        result = introspect(sample_copilot, depth=3)
        
        assert result['depth'] == 3
        assert len(result['history']) == 3
        # Each level should have metrics
        for level in result['history']:
            assert 'grip' in level
            assert 'fitness' in level
    
    def test_copilot_self_optimization(self, sample_copilot):
        """Test self-optimization improves grip."""
        initial_fitness = evaluate_fitness(sample_copilot)
        
        self_optimize(sample_copilot, iterations=5, learning_rate=0.1)
        
        final_fitness = evaluate_fitness(sample_copilot)
        # Fitness should improve or stay same (won't decrease)
        assert final_fitness >= initial_fitness - 0.01  # Allow small numerical error
    
    def test_copilot_development_progression(self, sample_copilot):
        """Test copilot progresses through developmental stages."""
        assert sample_copilot.state.stage == "embryonic"
        
        # Optimize until maturity increases
        for _ in range(10):
            self_optimize(sample_copilot, iterations=5)
            if sample_copilot.state.maturity > 0.2:
                break
        
        assert sample_copilot.state.stage in ["juvenile", "mature"]


class TestGripCalculation:
    """Tests for grip calculation."""
    
    def test_grip_components_calculation(self, sample_copilot):
        """Test grip has all required components."""
        from introspection.operators import calculate_grip
        
        grip = calculate_grip(sample_copilot)
        
        assert isinstance(grip, GripComponents)
        assert 0.0 <= grip.understanding <= 1.0
        assert 0.0 <= grip.correctness <= 1.0
        assert 0.0 <= grip.efficiency <= 1.0
        assert 0.0 <= grip.adaptability <= 1.0
        assert 0.0 <= grip.creativity <= 1.0
    
    def test_grip_domain_specificity(self):
        """Test grip varies with domain."""
        copilot_research = Copilot(domain="research")
        copilot_coding = Copilot(domain="coding")
        
        from introspection.operators import calculate_grip
        grip_research = calculate_grip(copilot_research)
        grip_coding = calculate_grip(copilot_coding)
        
        # Grips should be different for different domains
        assert grip_research.understanding != grip_coding.understanding or \
               grip_research.correctness != grip_coding.correctness


class TestDifferentialOperators:
    """Tests for differential operators."""
    
    def test_chain_rule_application(self, sample_copilot):
        """Test chain rule operator."""
        from introspection.operators import apply_chain_rule
        
        result = apply_chain_rule(sample_copilot, sample_copilot)
        
        assert result is not None
        assert hasattr(result, 'genome')
        # Composed copilot should have evolved capabilities
        assert not np.array_equal(
            result.genome.capabilities,
            sample_copilot.genome.capabilities
        )
    
    def test_product_rule_application(self, sample_copilot):
        """Test product rule operator."""
        from introspection.operators import apply_product_rule
        
        copilot2 = Copilot(domain="test")
        result = apply_product_rule(sample_copilot, copilot2)
        
        assert result is not None
        # Product should combine capabilities
        assert len(result.genome.capabilities) == len(sample_copilot.genome.capabilities)
    
    def test_quotient_rule_application(self, sample_copilot):
        """Test quotient rule operator."""
        from introspection.operators import apply_quotient_rule
        
        copilot2 = Copilot(domain="test")
        result = apply_quotient_rule(sample_copilot, copilot2)
        
        assert result is not None


# Add more tests as needed...
# Target: 90% code coverage for introspection module
```

**Checklist**:
- [ ] Write 15 tests for core introspection
- [ ] Achieve 70%+ coverage for introspection/core.py
- [ ] All tests pass
- [ ] Run: `pytest tests/test_introspection.py -v`

---

### Task 1.3: Ontogenesis Unit Tests - Core (2 hours)

Create `tests/test_ontogenesis.py`:

```python
"""Unit tests for ontogenesis framework."""

import pytest
import numpy as np
from ontogenesis import (
    OntogeneticKernel, KernelGenome,
    self_generate, self_optimize_kernel, self_reproduce
)
from ontogenesis.kernels import (
    create_consciousness_kernel,
    create_physics_kernel,
    create_mathematics_kernel
)


class TestKernelGenome:
    """Tests for KernelGenome class."""
    
    def test_genome_initialization(self):
        """Test kernel genome creates correctly."""
        genome = KernelGenome(
            coefficients=np.array([1.0, 0.5, 0.25]),
            kernel_type="consciousness",
            order=3
        )
        
        assert genome.id is not None
        assert len(genome.coefficients) == 3
        assert genome.kernel_type == "consciousness"
        assert genome.order == 3
    
    def test_genome_serialization(self):
        """Test genome can be serialized and deserialized."""
        genome = KernelGenome(
            coefficients=np.array([1.0, 0.5, 0.25]),
            kernel_type="physics",
            order=3
        )
        
        serialized = genome.to_dict()
        assert isinstance(serialized, dict)
        assert 'id' in serialized
        assert 'coefficients' in serialized
        assert 'kernel_type' in serialized


class TestOntogeneticKernel:
    """Tests for OntogeneticKernel class."""
    
    def test_kernel_initialization(self, sample_kernel):
        """Test kernel initializes correctly."""
        assert sample_kernel.genome is not None
        assert sample_kernel.fitness is not None
        assert sample_kernel.generation == 0
    
    def test_kernel_self_generation(self, sample_kernel):
        """Test kernel can self-generate offspring."""
        offspring = self_generate(sample_kernel)
        
        assert offspring is not None
        assert offspring.generation == sample_kernel.generation + 1
        assert offspring.genome.parent_ids == [sample_kernel.genome.id]
        # Offspring should have different coefficients
        assert not np.array_equal(
            offspring.genome.coefficients,
            sample_kernel.genome.coefficients
        )
    
    def test_kernel_self_optimization(self, sample_kernel):
        """Test kernel self-optimization."""
        initial_fitness = sample_kernel.fitness
        
        optimized = self_optimize_kernel(sample_kernel, iterations=5)
        
        # Fitness should improve or stay same
        assert optimized.fitness >= initial_fitness - 0.01
    
    def test_kernel_reproduction(self, sample_kernel):
        """Test sexual reproduction of kernels."""
        kernel2 = OntogeneticKernel(order=3, kernel_type="consciousness")
        
        offspring = self_reproduce(sample_kernel, kernel2)
        
        assert offspring is not None
        assert offspring.generation == max(sample_kernel.generation, kernel2.generation) + 1
        assert set(offspring.genome.parent_ids) == {sample_kernel.genome.id, kernel2.genome.id}


class TestKernelTypes:
    """Tests for different kernel types."""
    
    def test_consciousness_kernel_creation(self):
        """Test consciousness kernel has correct properties."""
        kernel = create_consciousness_kernel(order=4)
        
        assert kernel.genome.kernel_type == "consciousness"
        assert kernel.genome.order == 4
        assert len(kernel.genome.coefficients) == 4
    
    def test_physics_kernel_creation(self):
        """Test physics kernel has correct properties."""
        kernel = create_physics_kernel(order=4)
        
        assert kernel.genome.kernel_type == "physics"
        # Physics kernels should have energy conservation properties
        assert hasattr(kernel.genome, 'properties')
    
    def test_mathematics_kernel_creation(self):
        """Test mathematics kernel has correct properties."""
        kernel = create_mathematics_kernel(order=4)
        
        assert kernel.genome.kernel_type == "mathematics"
        # Math kernels should have high precision
        assert kernel.genome.properties.get('precision', 0) > 0.9


class TestGeneticOperators:
    """Tests for genetic operators."""
    
    def test_crossover_operation(self):
        """Test crossover produces valid offspring."""
        from ontogenesis.operators import crossover
        
        coeffs1 = np.array([1.0, 1.0, 1.0, 1.0])
        coeffs2 = np.array([0.0, 0.0, 0.0, 0.0])
        
        offspring = crossover(coeffs1, coeffs2, point=2)
        
        assert len(offspring) == 4
        # Should have parts from both parents
        assert np.any(offspring == 1.0)
        assert np.any(offspring == 0.0)
    
    def test_mutation_operation(self):
        """Test mutation produces variation."""
        from ontogenesis.operators import mutate
        
        coeffs = np.array([0.5, 0.5, 0.5, 0.5])
        mutated = mutate(coeffs, rate=0.1, strength=0.1)
        
        assert len(mutated) == len(coeffs)
        # Some values should have changed
        assert not np.array_equal(mutated, coeffs)


class TestEvolution:
    """Tests for evolution process."""
    
    def test_population_evolution(self):
        """Test population evolution runs successfully."""
        from ontogenesis.evolution import run_ontogenesis
        
        result = run_ontogenesis(
            population_size=10,
            generations=5,
            mutation_rate=0.1,
            crossover_rate=0.7,
            kernel_type="consciousness",
            order=3
        )
        
        assert 'best_kernel' in result
        assert 'history' in result
        assert len(result['history']) <= 5  # May converge early
        assert result['best_kernel'].fitness >= 0
    
    def test_tournament_selection(self):
        """Test tournament selection chooses fit individuals."""
        from ontogenesis.evolution import tournament_select
        
        population = [
            OntogeneticKernel(order=3, kernel_type="consciousness")
            for _ in range(10)
        ]
        
        # Manually set fitnesses for testing
        for i, kernel in enumerate(population):
            kernel.fitness = i / 10.0  # 0.0 to 0.9
        
        selected = tournament_select(population, k=3)
        
        # Selected should be relatively fit
        assert selected in population
        # Higher fitness individuals more likely to be selected


# Add more tests...
# Target: 90% code coverage for ontogenesis module
```

**Checklist**:
- [ ] Write 15 tests for core ontogenesis
- [ ] Achieve 70%+ coverage for ontogenesis/core.py
- [ ] All tests pass
- [ ] Run: `pytest tests/test_ontogenesis.py -v`

---

## 🎯 Day 3: CI/CD Setup (3-4 hours)

### Task 3.1: GitHub Actions Workflow (2 hours)

Create `.github/workflows/test-introspection-ontogenesis.yml`:

```yaml
name: Introspection & Ontogenesis Tests

on:
  push:
    branches: [ main, develop ]
    paths:
      - 'introspection/**'
      - 'ontogenesis/**'
      - 'examples/**'
      - 'tests/**'
      - '.github/workflows/test-introspection-ontogenesis.yml'
  pull_request:
    branches: [ main, develop ]
    paths:
      - 'introspection/**'
      - 'ontogenesis/**'
      - 'examples/**'
      - 'tests/**'

jobs:
  test:
    name: Test Python ${{ matrix.python-version }}
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.8", "3.9", "3.10", "3.11"]
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt
          pip install numpy  # Core dependency
      
      - name: Lint with flake8
        run: |
          # Stop build if there are Python syntax errors or undefined names
          flake8 introspection ontogenesis --count --select=E9,F63,F7,F82 --show-source --statistics
          # Exit-zero treats all errors as warnings
          flake8 introspection ontogenesis --count --exit-zero --max-complexity=10 --max-line-length=100 --statistics
      
      - name: Type check with mypy
        run: |
          mypy introspection ontogenesis --ignore-missing-imports || true
      
      - name: Run unit tests
        run: |
          pytest tests/ -v --cov=introspection --cov=ontogenesis --cov-report=xml --cov-report=term
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          flags: unittests
          name: codecov-umbrella
          fail_ci_if_error: false
      
      - name: Test examples
        run: |
          python3 examples/introspection/basic_introspection.py
          python3 examples/ontogenesis/self_generation.py
          python3 examples/ontogenesis/evolution_example.py
      
      - name: Archive test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results-${{ matrix.python-version }}
          path: |
            coverage.xml
            .coverage

  test-summary:
    name: Test Summary
    needs: test
    runs-on: ubuntu-latest
    if: always()
    steps:
      - name: Check test results
        run: |
          if [ "${{ needs.test.result }}" = "success" ]; then
            echo "✅ All tests passed!"
          else
            echo "❌ Some tests failed"
            exit 1
          fi
```

**Checklist**:
- [ ] Create workflow file
- [ ] Test workflow locally with act (optional)
- [ ] Push and verify workflow runs
- [ ] Check all Python versions pass

---

### Task 3.2: Add Badges and Status (1 hour)

Update main `README.md` to add status badges:

```markdown
## 🧬 Introspection & Ontogenesis Frameworks

![Tests](https://github.com/opencog/opencog-org/workflows/Introspection%20%26%20Ontogenesis%20Tests/badge.svg)
![Coverage](https://codecov.io/gh/opencog/opencog-org/branch/main/graph/badge.svg?flag=introspection-ontogenesis)
![Python](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)
![License](https://img.shields.io/badge/license-AGPL--3.0-green)

**NEW**: Self-aware, self-evolving systems based on recursive introspection and genetic kernels.
```

Create `tests/README.md`:

```markdown
# Testing Guide

## Running Tests

### All Tests
```bash
pytest tests/ -v
```

### With Coverage
```bash
pytest tests/ --cov=introspection --cov=ontogenesis --cov-report=html
```

### Specific Module
```bash
pytest tests/test_introspection.py -v
pytest tests/test_ontogenesis.py -v
```

### Parallel Execution
```bash
pytest tests/ -n auto
```

## Test Structure

- `test_introspection.py` - Introspection framework tests
- `test_ontogenesis.py` - Ontogenesis framework tests
- `test_integration.py` - Integration tests
- `test_operators.py` - Operator tests
- `conftest.py` - Shared fixtures

## Coverage Goals

- Target: 85%+ overall coverage
- Critical paths: 95%+ coverage
- New code: Must include tests

## Writing Tests

Follow pytest conventions:
- Test files: `test_*.py`
- Test functions: `test_*()`
- Test classes: `Test*`

Use fixtures from `conftest.py` for common setup.
```

**Checklist**:
- [ ] Add badges to README
- [ ] Create tests/README.md
- [ ] Verify badges work after CI runs
- [ ] Update main docs with testing info

---

## 🎯 Day 4: Integration Tests (3-4 hours)

### Task 4.1: Create Integration Test Suite (3 hours)

Create `tests/test_integration.py`:

```python
"""Integration tests for introspection + ontogenesis."""

import pytest
import numpy as np
from introspection import Copilot, introspect, self_optimize
from ontogenesis import run_ontogenesis, OntogeneticKernel


class TestIntrospectionOntogenesisIntegration:
    """Test integration between frameworks."""
    
    def test_copilot_evolves_with_ontogenesis(self):
        """Test copilot uses ontogenesis for evolution."""
        # Create copilot
        copilot = Copilot(domain="evolution")
        
        # Initial fitness
        initial_fitness = copilot.fitness
        
        # Use ontogenesis to evolve copilot's kernel
        result = run_ontogenesis(
            population_size=5,
            generations=3,
            kernel_type="consciousness",
            order=3
        )
        
        # Apply best kernel to copilot
        best_kernel = result['best_kernel']
        copilot.apply_kernel(best_kernel)
        
        # Fitness should improve
        assert copilot.fitness >= initial_fitness
    
    def test_multi_generation_lineage(self):
        """Test tracking lineage across multiple generations."""
        # Create initial population
        population = [
            OntogeneticKernel(order=3, kernel_type="consciousness")
            for _ in range(5)
        ]
        
        # Evolve for multiple generations
        history = []
        for gen in range(5):
            # ... evolution logic ...
            history.append(population.copy())
        
        # Verify lineage tracking
        assert len(history) == 5
        # Check parent-child relationships
        # ... verification logic ...


# More integration tests...
```

**Checklist**:
- [ ] Write 10 integration tests
- [ ] Test cross-module interactions
- [ ] Verify data flow between modules
- [ ] All tests pass

---

## 🎯 Day 5: Documentation & Final Verification (2-3 hours)

### Task 5.1: Update Documentation (1 hour)

Update `IMPLEMENTATION_SUMMARY.md` with testing info:

```markdown
## Phase 3: Testing & Quality Assurance ✅

### Unit Test Suite
- **Coverage**: 85%+ across both frameworks
- **Python Versions**: 3.8, 3.9, 3.10, 3.11
- **Test Count**: 40+ unit tests, 10+ integration tests

### CI/CD Pipeline
- **GitHub Actions**: Automated testing on every push/PR
- **Test Matrix**: Multi-version Python testing
- **Coverage Reporting**: Codecov integration
- **Quality Gates**: Linting, type checking, coverage thresholds
```

**Checklist**:
- [ ] Update IMPLEMENTATION_SUMMARY.md
- [ ] Update NEXT_STEPS.md progress
- [ ] Update README with testing section
- [ ] Create TESTING.md guide

---

### Task 5.2: Final Verification (1 hour)

Run complete test suite and verify everything works:

```bash
# 1. Run all tests
pytest tests/ -v --cov=introspection --cov=ontogenesis

# 2. Check coverage
pytest tests/ --cov=introspection --cov=ontogenesis --cov-report=html
open htmlcov/index.html  # View coverage report

# 3. Run examples
python3 examples/introspection/basic_introspection.py
python3 examples/ontogenesis/self_generation.py
python3 examples/ontogenesis/evolution_example.py

# 4. Verify CI passes
git push origin main
# Check GitHub Actions

# 5. Run linting
flake8 introspection ontogenesis
black --check introspection ontogenesis
mypy introspection ontogenesis
```

**Checklist**:
- [ ] All tests pass locally
- [ ] Coverage ≥ 70%
- [ ] Examples run without errors
- [ ] CI passes on GitHub
- [ ] No linting errors
- [ ] Documentation updated

---

## 📊 Success Criteria

By end of Week 1, you should have:

✅ **Testing**
- [ ] 40+ unit tests written
- [ ] 10+ integration tests written
- [ ] 70%+ code coverage
- [ ] All tests passing

✅ **CI/CD**
- [ ] GitHub Actions workflow active
- [ ] Multi-version Python testing
- [ ] Automated coverage reporting
- [ ] Status badges in README

✅ **Quality**
- [ ] No linting errors
- [ ] Type hints added
- [ ] Documentation updated
- [ ] Examples verified working

✅ **Infrastructure**
- [ ] `tests/` directory structure
- [ ] `requirements-dev.txt` file
- [ ] `conftest.py` fixtures
- [ ] `.github/workflows/` CI config

---

## 🚨 Troubleshooting

### Tests Fail
- Check Python version compatibility
- Verify all dependencies installed
- Look at pytest output for specific errors
- Run individual tests to isolate issues

### CI Fails
- Check workflow syntax with act
- Verify paths in workflow file
- Check if secrets are needed
- Review CI logs on GitHub

### Coverage Too Low
- Identify uncovered lines with HTML report
- Add tests for edge cases
- Test error handling paths
- Add parametrized tests

---

## 📝 Daily Commit Messages

Use clear, descriptive commit messages:

```bash
git commit -m "Add unit test suite for introspection framework"
git commit -m "Create GitHub Actions workflow for testing"
git commit -m "Achieve 70% test coverage for ontogenesis"
git commit -m "Add integration tests for cross-module functionality"
git commit -m "Update documentation with testing guidelines"
```

---

## 🎉 Week 1 Complete!

Once all checkboxes are ticked, you're ready to move to Week 2: AtomSpace Integration!

**Next**: See [NEXT_STEPS.md](../NEXT_STEPS.md) Priority 2 for AtomSpace bridge implementation.
