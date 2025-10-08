# Gauge Python Build Plugin

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://img.shields.io/pypi/v/gauge-pybuild-plugin.svg)](https://pypi.org/project/gauge-pybuild-plugin/)
[![Downloads](https://img.shields.io/pypi/dm/gauge-pybuild-plugin.svg)](https://pypi.org/project/gauge-pybuild-plugin/)

A comprehensive Python build plugin for [Gauge](https://gauge.org/) testing framework, inspired by the [Gauge Gradle Plugin](https://github.com/getgauge/gauge-gradle-plugin). This plugin provides seamless integration with UV, Poetry, setuptools, and standalone CLI functionality for running Gauge specifications in Python projects.

## Quick Start

```bash
# Install from PyPI
pip install gauge-pybuild-plugin

# Run your Gauge specs
gauge-py run

# Or use with UV for faster performance
uv pip install gauge-pybuild-plugin
uv run gauge-py run --parallel --nodes=4
```

## Features

- 🚀 **Multiple Integration Options**: UV, Poetry plugin, setuptools commands, and standalone CLI
- ⚡ **Parallel Execution**: Run specs in parallel with configurable worker nodes
- 🏷️ **Tag-based Filtering**: Execute specific specs using tag expressions
- 🌍 **Environment Support**: Run against different environments (dev, test, prod, etc.)
- ⚙️ **Flexible Configuration**: TOML-based configuration with sensible defaults
- 🔧 **Validation & Formatting**: Built-in project validation and spec formatting
- 📦 **Plugin Management**: Install and manage Gauge plugins
- 🎯 **Gradle-like Experience**: Similar API and workflow as the Gradle plugin
- 🦀 **Modern Tools**: Support for UV (Rust-based, 10-100x faster than pip)

## Prerequisites

Before using this plugin, you need:

1. **Gauge Framework** installed on your system:
   ```bash
   # macOS
   brew install gauge
   
   # Windows (using Chocolatey)
   choco install gauge
   
   # Linux
   curl -SsL https://downloads.gauge.org/stable | sh
   ```
   Verify installation: `gauge version`

2. **Gauge Python Plugin** installed:
   ```bash
   gauge install python
   ```

3. **An existing Gauge project** or create a new one:
   ```bash
   # Create new Gauge project
   gauge init python
   
   # This creates:
   # - manifest.json (Gauge project metadata)
   # - specs/ (test specifications directory)
   # - step_impl/ (step implementations)
   ```

> ⚠️ **Important**: This plugin must be run from within a Gauge project directory (one containing `manifest.json` and `specs/`). It enhances existing Gauge projects with build tool integration.

## Installation

### Quick Install from PyPI 📦

```bash
# Using pip (works everywhere)
pip install gauge-pybuild-plugin

# Using UV (recommended - 10-100x faster!)
uv pip install gauge-pybuild-plugin

# Using Poetry
poetry add gauge-pybuild-plugin
```

### Using UV (Recommended - Fast!) ⚡

UV is a modern, Rust-based Python package manager that's 10-100x faster than pip.

```bash
# Install UV first (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install the plugin from PyPI
uv pip install gauge-pybuild-plugin

# Or add to your project
uv add gauge-pybuild-plugin
```

### Using Poetry

```bash
poetry add gauge-pybuild-plugin
```

### Using pip

```bash
pip install gauge-pybuild-plugin
```

### Development Installation

```bash
# Clone the repository
git clone https://github.com/lirany1/gauge-pybuild-plugin.git
cd gauge-pybuild-plugin

# Option 1: Using UV (recommended - faster)
uv pip install -e ".[dev]"

# Option 2: Using Poetry
poetry install
```

### Verify Installation

After installation, verify the plugin is working:

```bash
# Check if CLI is available
gauge-py --help

# In a Gauge project directory, try:
gauge-py validate
```

## Quick Start

### 1. UV Integration (Modern & Fast) ⚡

UV automatically manages virtual environments and dependencies:

```bash
# Run Gauge specs
uv run gauge-py run

# Run with options
uv run gauge-py run --parallel --nodes=4 --env=dev --tags="smoke"

# Validate and format
uv run gauge-py validate
uv run gauge-py format

# Install Gauge plugins
uv run gauge-py install python
```

### 2. Poetry Integration

Add the plugin to your `pyproject.toml`:

```toml
[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
name = "my-gauge-project"
version = "0.1.0"
description = "My Gauge project"

[tool.poetry.dependencies]
python = "^3.8"
getgauge = "^0.3.7"
gauge-pybuild-plugin = "^0.1.0"

# Gauge configuration
[tool.gauge]
specs_dir = "specs"
in_parallel = false
nodes = 1
env = "default"
additional_flags = "--verbose"

[tool.gauge.environment_variables]
gauge_reports_dir = "reports"
logs_directory = "logs"
```

Run Gauge through Poetry:

```bash
# Run all specs
poetry gauge run

# Run specific specs
poetry gauge run spec1.spec spec2.spec

# Run with options
poetry gauge run --parallel --nodes=4 --env=dev --tags="smoke"

# Validate project
poetry gauge validate

# Format specs
poetry gauge format

# Install plugins
poetry gauge install python
```

### 3. Setuptools Integration

Add to your `setup.py`:

```python
from setuptools import setup

setup(
    name="my-gauge-project",
    version="0.1.0",
    install_requires=[
        "getgauge>=0.3.7",
        "gauge-pybuild-plugin>=0.1.0",
    ],
    entry_points={
        "distutils.commands": [
            "gauge = gauge_pybuild_plugin.setuptools_command:GaugeCommand",
            "gauge_validate = gauge_pybuild_plugin.setuptools_command:GaugeValidateCommand",
            "gauge_format = gauge_pybuild_plugin.setuptools_command:GaugeFormatCommand",
        ]
    }
)
```

Run through setuptools:

```bash
# Run specs
python setup.py gauge

# Run with options
python setup.py gauge --parallel --nodes=4 --env=dev

# Validate and format
python setup.py gauge_validate
python setup.py gauge_format
```

### 4. Standalone CLI

Install the plugin and use the CLI directly:

```bash
# Run specs
gauge-py run

# Run with configuration
gauge-py run --specs-dir=specs --parallel --nodes=4 --env=dev

# Other commands
gauge-py validate
gauge-py format
gauge-py install python
gauge-py config --init
```

## Configuration Options

The plugin supports all the configuration options from the Gradle plugin, with Python-friendly naming:

| Option | CLI Flag | Description | Default |
|--------|----------|-------------|---------|
| `specs_dir` | `--specs-dir` | Gauge specs directory path | `"specs"` |
| `tags` | `--tags` | Filter specs by tags expression | `None` |
| `in_parallel` | `--parallel` | Execute specs in parallel | `false` |
| `nodes` | `--nodes` | Number of parallel execution streams | `1` |
| `env` | `--env` | Gauge environment to run against | `None` |
| `additional_flags` | `--additional-flags` | Additional gauge flags | `None` |
| `project_dir` | `--project-dir` | Path to gauge project directory | Current directory |
| `gauge_root` | `--gauge-root` | Path to gauge installation root | Auto-detected |
| `environment_variables` | N/A | Additional environment variables | `{}` |

### Configuration File Examples

#### Basic Configuration

```toml
[tool.gauge]
specs_dir = "specs"
in_parallel = false
nodes = 1
env = "default"
```

#### Advanced Configuration

```toml
[tool.gauge]
specs_dir = "specifications"
in_parallel = true
nodes = 4
env = "ci"
additional_flags = "--simple-console --verbose"
gauge_root = "/opt/gauge"

[tool.gauge.environment_variables]
gauge_reports_dir = "custom/reports"
logs_directory = "custom/logs"
screenshot_on_failure = "true"
```

#### Multiple Environment Configurations

```toml
# Default configuration
[tool.gauge]
specs_dir = "specs"
in_parallel = false
nodes = 1

# Development environment
[tool.gauge.environments.dev]
env = "dev"
additional_flags = "--verbose"

# CI environment  
[tool.gauge.environments.ci]
env = "ci"
in_parallel = true
nodes = 4
additional_flags = "--simple-console"
```

## Usage Examples

### UV Examples (Fast & Modern) ⚡

```bash
# Basic execution
uv run gauge-py run

# Parallel execution
uv run gauge-py run --parallel --nodes=4

# Tag-based execution
uv run gauge-py run --tags="smoke & !slow"

# Environment-specific execution
uv run gauge-py run --env=dev

# Specific specs
uv run gauge-py run specs/login.spec specs/checkout.spec

# Combined options
uv run gauge-py run --parallel --nodes=8 --env=ci --tags="regression"
```

### Poetry Examples

```bash
# Basic execution
poetry gauge run

# Parallel execution
poetry gauge run --parallel --nodes=4

# Tag-based execution
poetry gauge run --tags="smoke & !slow"

# Environment-specific execution
poetry gauge run --env=dev

# Specific specs
poetry gauge run specs/login.spec specs/checkout.spec

# Combined options
poetry gauge run --parallel --nodes=8 --env=ci --tags="regression" --additional-flags="--simple-console"
```

### CLI Examples

```bash
# Initialize configuration
gauge-py config --init

# Show current configuration
gauge-py config --show

# Run with verbose output
gauge-py --verbose run --parallel --nodes=4

# Run specific specs
gauge-py run specs/api/*.spec

# Install and manage plugins
gauge-py install python --version=0.3.7
gauge-py install html-report
```

### Setuptools Examples

```bash
# Basic execution
python setup.py gauge

# With options
python setup.py gauge --parallel --nodes=4 --env=test

# Validation and formatting
python setup.py gauge_validate
python setup.py gauge_format
```

## Comparison with Gradle Plugin

| Feature | Gradle Plugin | Python Plugin |
|---------|---------------|---------------|
| Build Tool Integration | ✅ Gradle | ✅ Poetry, setuptools |
| Parallel Execution | ✅ | ✅ |
| Tag Filtering | ✅ | ✅ |
| Environment Support | ✅ | ✅ |
| Custom Tasks | ✅ | ✅ (via CLI/API) |
| Configuration | `build.gradle` | `pyproject.toml` |
| CLI Interface | `gradle gauge` | `gauge-py run` |

### Gradle vs Python Syntax

**Gradle Plugin:**
```groovy
// build.gradle
gauge {
    specsDir = 'specs'
    inParallel = true
    nodes = 2
    env = 'dev'
    tags = 'tag1'
    additionalFlags = '--verbose'
}

// Command line
gradle gauge -PspecsDir="specs" -PinParallel=true -Pnodes=4
```

**Python Plugin:**
```toml
# pyproject.toml
[tool.gauge]
specs_dir = "specs"
in_parallel = true
nodes = 2
env = "dev"
tags = "tag1"
additional_flags = "--verbose"
```

```bash
# Command line
poetry gauge run --specs-dir=specs --parallel --nodes=4
gauge-py run --specs-dir=specs --parallel --nodes=4
```

## API Reference

### Core Classes

#### `GaugeConfig`

Configuration management class with validation and command generation.

```python
from gauge_pybuild_plugin import GaugeConfig

config = GaugeConfig(
    specs_dir="specs",
    in_parallel=True,
    nodes=4,
    env="dev"
)

# Generate command arguments
args = config.to_command_args()
# ['--parallel', '--n', '4', '--env', 'dev', 'specs']

# Get environment variables
env = config.get_environment()
```

#### `GaugeTask`

Task execution wrapper for running Gauge commands.

```python
from gauge_pybuild_plugin import GaugeTask, GaugeConfig

config = GaugeConfig(in_parallel=True, nodes=4)
task = GaugeTask(config)

# Run specs
success = task.run()
success = task.run(["spec1.spec", "spec2.spec"])

# Validate project
success = task.validate()

# Format specs
success = task.format_specs()

# Install plugin
success = task.install_plugin("python", "0.3.7")
```

#### `GaugePlugin`

Main plugin orchestrator with configuration loading.

```python
from gauge_pybuild_plugin import GaugePlugin

# Load from config file
plugin = GaugePlugin("pyproject.toml")

# Create tasks
task = plugin.create_task()
task = plugin.create_task({"in_parallel": True})

# High-level operations
plugin.run_specs(in_parallel=True, nodes=4)
plugin.validate_project()
plugin.format_specs()
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests: `pytest tests/`
5. Run linting: `ruff check . && ruff format .`
6. Submit a pull request

### Development Setup

**Using UV (Recommended - 10-100x faster):**

```bash
git clone https://github.com/lirany1/gauge-pybuild-plugin.git
cd gauge-pybuild-plugin

# Install UV first
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies with dev extras
uv pip install -e ".[dev]"

# Run tests
uv run pytest

# Run linting (using Ruff - modern & fast)
uv run ruff check .
uv run ruff format .
uv run mypy src/

# Install pre-commit hooks
uv run pre-commit install
```

**Using Poetry:**

```bash
git clone https://github.com/lirany1/gauge-pybuild-plugin.git
cd gauge-pybuild-plugin

# Install dependencies
poetry install

# Run tests
poetry run pytest

# Run linting
poetry run ruff check .
poetry run ruff format .
poetry run mypy src/

# Install pre-commit hooks
poetry run pre-commit install
```

## Troubleshooting

### Common Issues

#### "Failed to find Gauge project directory. Missing manifest.json file"
**Cause**: You're not in a Gauge project directory.

**Solution**: 
- Navigate to a directory containing a Gauge project (with `manifest.json`)
- Or create a new Gauge project: `gauge init python`

#### "specs directory 'specs' does not exist"
**Cause**: The Gauge project doesn't have a specs directory.

**Solution**:
- Create the specs directory: `mkdir specs`
- Or initialize a Gauge project properly: `gauge init python`

#### "poetry: command not found"
**Cause**: Poetry is not installed.

**Solution**:
- **Recommended**: Use UV instead: `uv run gauge-py run`
- Or install Poetry: `curl -sSL https://install.python-poetry.org | python3 -`
- Or use the standalone CLI: `gauge-py run`

#### "Slow dependency installation"
**Cause**: Using pip or Poetry for package installation.

**Solution**:
- Switch to UV for 10-100x faster installs:
  ```bash
  # Install UV
  curl -LsSf https://astral.sh/uv/install.sh | sh
  
  # Use UV instead
  uv pip install gauge-pybuild-plugin
  ```

#### "python: command not found" (when running Gauge)
**Cause**: Gauge expects `python` but your system has `python3`.

**Solution**:
```bash
# Create a symlink
sudo ln -s $(which python3) /usr/local/bin/python

# Or modify env/default/python.properties in your Gauge project
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the [Gauge Gradle Plugin](https://github.com/getgauge/gauge-gradle-plugin)
- Built for the [Gauge](https://gauge.org/) testing framework
- Thanks to the Gauge community for their awesome work

## Support

- � [PyPI Package](https://pypi.org/project/gauge-pybuild-plugin/)
- �📖 [Gauge Documentation](https://docs.gauge.org/)
- 🐛 [Report Issues](https://github.com/lirany1/gauge-pybuild-plugin/issues)
- 💬 [Gauge Community](https://github.com/getgauge/gauge/discussions)
- 🌟 [GitHub Repository](https://github.com/lirany1/gauge-pybuild-plugin)