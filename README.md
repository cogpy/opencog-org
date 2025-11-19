# OpenCog Organization Repository

This repository contains the OpenCog ecosystem components, comprehensive build automation, and advanced introspection & ontogenesis frameworks.

## 🚀 One-Click Gitpod Deployment

Launch a complete OpenCog development environment in your browser with zero configuration:

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/OpenCoq/opencog-org)

### ✨ What You Get Instantly

- **🧠 Complete OpenCog Ecosystem** - AtomSpace, CogServer, and all core components
- **🐍 Python 3.10 Environment** - Pre-configured with scientific computing libraries
- **📦 Guix Package Manager** - Reproducible builds with automatic fallback
- **🔧 Automated Build System** - One-command build of entire ecosystem
- **🌐 Port Forwarding** - Direct browser access to OpenCog services
- **📚 Comprehensive Documentation** - Guides, troubleshooting, and examples
- **🛠️ VS Code Integration** - Full IDE with C++, Python, and Guile support

### 🎯 Two-Minute Quick Start

1. **Click the Gitpod button above** ⬆️
2. **Wait 2-3 minutes** for automatic environment setup
3. **Run `opencog_status`** to verify installation
4. **Run `build-opencog`** to build all components
5. **Run `demos`** to see available examples

### 🌐 Service Access

Once deployed, access OpenCog services via Gitpod's port forwarding:

| Service | Port | Access |
|---------|------|--------|
| **CogServer Telnet** | 17001 | `start-cogserver` |
| **CogServer Web UI** | 18001 | Browser preview |
| **REST API** | 5000 | Browser preview |
| **Web Demos** | 8080 | Browser preview |

### 📖 Documentation

- **[Complete Gitpod Guide](.gitpod/README.md)** - Comprehensive deployment documentation
- **[Troubleshooting Guide](.gitpod/TROUBLESHOOTING.md)** - Solutions to common issues
- **[OpenCog Wiki](https://wiki.opencog.org/)** - Official OpenCog documentation

## 🏗️ OpenCog Dependency Build Matrix

We've implemented a comprehensive GitHub Actions workflow that builds and installs all OpenCog components according to dependency diagrams with matrix discovery of hidden dependencies.

### Key Features:
- **40+ Component Coverage**: Builds the entire OpenCog ecosystem
- **9 Dependency Layers**: Foundation → Core → Logic → Cognitive → Advanced → Learning → Language → Robotics → Integration  
- **Fail-Never Approach**: Discovers all possible build issues without stopping
- **Matrix Build Strategy**: Parallel builds within dependency categories
- **Hidden Dependency Discovery**: Systematic identification of undocumented dependencies
- **Comprehensive Reporting**: Automated issue creation and detailed build summaries

### Quick Start:
1. Go to [Actions tab](../../actions)
2. Select "OpenCog Dependency Build Matrix"
3. Click "Run workflow"
4. Choose build category (or "all" for complete build)

### Documentation:
- [Complete Documentation](docs/OPENCOG_DEPENDENCY_BUILD.md)
- [Quick Start Guide](docs/QUICK_START_GUIDE.md)
- [Dependency Diagrams](MERMAID_DIAGRAMS.md)

## 🧬 Introspection & Ontogenesis Frameworks

**NEW**: Self-aware, self-evolving systems based on recursive introspection and genetic kernels.

### Features:
- **Introspection Framework**: Recursive self-awareness for copilot agents
  - Meta-cognitive introspection: `self.copilot(n) = introspection.self.copilot(n-1)`
  - Self-optimization through grip maximization
  - Differential operators (chain, product, quotient rules)
  - Ontogenetic development stages
  
- **Ontogenesis Framework**: Self-generating mathematical kernels
  - Self-generation via chain rule composition
  - Genetic operators (crossover, mutation)
  - Population evolution with fitness evaluation
  - Domain-specific kernels (consciousness, physics, mathematics)

### Quick Start:
```bash
# Install dependencies
pip3 install numpy

# Run introspection example
python3 examples/introspection/basic_introspection.py

# Run ontogenesis example
python3 examples/ontogenesis/self_generation.py

# Run evolution example
python3 examples/ontogenesis/evolution_example.py
```

### Documentation:
- [Introspection Agent Specification](.github/agents/introspection.md)
- [Ontogenesis Agent Specification](.github/agents/ONTOGENESIS.md)
- [Examples and Usage](examples/README.md)
- [Introspection Analysis](INTROSPECTION_REPORT.md)

## Repository Structure

This repository contains OpenCog components organized by functional categories as defined in the dependency diagrams.
