"""
Core Gauge plugin functionality

This module provides the main classes for Gauge task execution,
configuration management, and plugin integration.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator


class GaugeConfig(BaseModel):
    """
    Configuration for Gauge execution tasks.

    Mirrors the configuration options available in the Gradle plugin:
    - specsDir: Gauge specs directory path
    - tags: Filter specs by specified tags expression
    - inParallel: Execute specs in parallel
    - nodes: Number of parallel execution streams
    - env: Gauge environment to run against
    - additionalFlags: Additional gauge flags for execution
    - dir: Path to gauge project directory
    - gaugeRoot: Path to gauge installation root
    - environmentVariables: Additional environment variables
    """

    specs_dir: Optional[str] = Field(default="specs", description="Gauge specs directory path")
    tags: Optional[str] = Field(default=None, description="Filter specs by tags expression")
    in_parallel: bool = Field(default=False, description="Execute specs in parallel")
    nodes: int = Field(default=1, description="Number of parallel execution streams")
    env: Optional[str] = Field(default=None, description="Gauge environment to run against")
    additional_flags: Optional[str] = Field(default=None, description="Additional gauge flags")
    project_dir: Optional[str] = Field(default=None, description="Path to gauge project directory")
    gauge_root: Optional[str] = Field(default=None, description="Path to gauge installation root")
    environment_variables: Dict[str, str] = Field(default_factory=dict, description="Additional environment variables")

    @validator('nodes')
    def validate_nodes(cls, v):
        if v < 1:
            raise ValueError('nodes must be at least 1')
        return v

    @validator('specs_dir')
    def validate_specs_dir(cls, v):
        if v and not Path(v).exists():
            print(f"Warning: specs directory '{v}' does not exist")
        return v

    def to_command_args(self) -> List[str]:
        """Convert configuration to gauge command arguments."""
        args = []

        if self.tags:
            args.extend(["--tags", self.tags])

        if self.in_parallel:
            args.append("--parallel")
            if self.nodes > 1:
                args.extend(["--n", str(self.nodes)])

        if self.env:
            args.extend(["--env", self.env])

        if self.additional_flags:
            # Split additional flags and add them
            args.extend(self.additional_flags.split())

        if self.specs_dir:
            args.append(self.specs_dir)

        return args

    def get_environment(self) -> Dict[str, str]:
        """Get environment variables for gauge execution."""
        env = os.environ.copy()

        if self.gauge_root:
            env["GAUGE_ROOT"] = self.gauge_root

        # Add custom environment variables
        env.update(self.environment_variables)

        return env


class GaugeTask:
    """
    Main task executor for Gauge operations.

    Provides methods for:
    - Running gauge specs
    - Validating gauge projects
    - Custom task execution
    """

    def __init__(self, config: Optional[GaugeConfig] = None):
        self.config = config or GaugeConfig()

    def _find_gauge_executable(self) -> str:
        """Find the gauge executable in the system."""
        if self.config.gauge_root:
            gauge_path = Path(self.config.gauge_root) / "bin" / "gauge"
            if gauge_path.exists():
                return str(gauge_path)

        # Check if gauge is in PATH
        import shutil
        gauge_exe = shutil.which("gauge")
        if gauge_exe:
            return gauge_exe

        raise RuntimeError("Gauge executable not found. Please install Gauge or set gauge_root in configuration.")

    def _run_command(self, command: List[str], cwd: Optional[str] = None) -> subprocess.CompletedProcess:
        """Run a command and return the result."""
        env = self.config.get_environment()
        working_dir = cwd or self.config.project_dir or os.getcwd()

        print(f"Running command: {' '.join(command)}")
        print(f"Working directory: {working_dir}")

        try:
            result = subprocess.run(
                command,
                cwd=working_dir,
                env=env,
                capture_output=True,
                text=True,
                check=False
            )

            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)

            return result
        except Exception as e:
            raise RuntimeError(f"Failed to execute command: {e}")

    def run(self, specs: Optional[List[str]] = None) -> bool:
        """
        Execute Gauge specs.

        Args:
            specs: Optional list of specific spec files to run

        Returns:
            True if execution was successful, False otherwise
        """
        gauge_exe = self._find_gauge_executable()
        command = [gauge_exe, "run"]

        # Add configuration arguments
        command.extend(self.config.to_command_args())

        # Add specific specs if provided
        if specs:
            # Remove the default specs_dir if specific specs are provided
            if self.config.specs_dir in command:
                command.remove(self.config.specs_dir)
            command.extend(specs)

        result = self._run_command(command)
        return result.returncode == 0

    def validate(self) -> bool:
        """
        Validate the Gauge project.

        Returns:
            True if validation was successful, False otherwise
        """
        gauge_exe = self._find_gauge_executable()
        command = [gauge_exe, "validate"]

        if self.config.specs_dir:
            command.append(self.config.specs_dir)

        result = self._run_command(command)
        return result.returncode == 0

    def install_plugin(self, plugin_name: str, version: Optional[str] = None) -> bool:
        """
        Install a Gauge plugin.

        Args:
            plugin_name: Name of the plugin to install
            version: Optional version of the plugin

        Returns:
            True if installation was successful, False otherwise
        """
        gauge_exe = self._find_gauge_executable()
        command = [gauge_exe, "install", plugin_name]

        if version:
            command.extend(["--version", version])

        result = self._run_command(command)
        return result.returncode == 0

    def format_specs(self) -> bool:
        """
        Format Gauge specification files.

        Returns:
            True if formatting was successful, False otherwise
        """
        gauge_exe = self._find_gauge_executable()
        command = [gauge_exe, "format"]

        if self.config.specs_dir:
            command.append(self.config.specs_dir)

        result = self._run_command(command)
        return result.returncode == 0


class GaugePlugin:
    """
    Main plugin class that orchestrates Gauge operations.

    This class provides the main interface for build tool integration
    and can be used by Poetry plugins, setuptools commands, or standalone CLI.
    """

    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self) -> GaugeConfig:
        """Load configuration from file or use defaults."""
        if self.config_file and Path(self.config_file).exists():
            # Load from TOML file
            import toml
            with open(self.config_file) as f:
                data = toml.load(f)

            # Extract gauge configuration
            gauge_config = data.get('tool', {}).get('gauge', {})
            return GaugeConfig(**gauge_config)

        return GaugeConfig()

    def create_task(self, config_override: Optional[Dict[str, Any]] = None) -> GaugeTask:
        """Create a new Gauge task with optional configuration override."""
        if config_override:
            # Merge configuration
            config_dict = self.config.dict()
            config_dict.update(config_override)
            config = GaugeConfig(**config_dict)
        else:
            config = self.config

        return GaugeTask(config)

    def run_specs(self, **kwargs) -> bool:
        """Run Gauge specs with optional configuration override."""
        task = self.create_task(kwargs)
        return task.run()

    def validate_project(self, **kwargs) -> bool:
        """Validate Gauge project with optional configuration override."""
        task = self.create_task(kwargs)
        return task.validate()

    def format_specs(self, **kwargs) -> bool:
        """Format Gauge specs with optional configuration override."""
        task = self.create_task(kwargs)
        return task.format_specs()
