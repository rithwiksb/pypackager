# pypackager

Unified build pipeline to produce multiple distribution formats (wheels, Docker images, standalone binaries) from a Python project using a single command.

## Features (MVP)
- Wheel builder (pure-Python preferred; ABI wheels allowed)
- Docker builder (multi-stage with `python:<version>-slim` runtime)
- Binary builder (PyInstaller backend)
- Plugin system via entry points (`pypackager.builders`)
- Isolated ephemeral virtualenvs per build target

Planned Phase 2: Linux `.deb` (via fpm), Homebrew formula, Windows installer (MSI/Inno Setup).

## Supported Platforms
- Linux: Ubuntu 22.04+ (`amd64`, `arm64`) — glibc only
- macOS: 13+ (`x86_64`, `arm64`)
- Windows: 10+ (`x64`)
- Python: 3.9 – 3.13

## Installation (from source)
```bash
git clone https://github.com/rithwiksb/pypackager
cd pypackager
python -m pip install -e .
```

## Quick Start
Run the CLI against a Python project (defaults to current directory):
```bash
# Show version
pypackager --version

# Build all default targets (wheel, docker, binary)
pypackager build

# Build only wheels
pypackager build --only wheel

# Use alias
pypack build --only docker --output dist
```

Outputs are written under `dist/<target>/`.

## Configuration
`pypackager.toml` in the project root is optional. Minimal example:
```toml
[pypackager]
targets = ["wheel", "docker", "binary"]
```

## Architecture Overview
- Scanner: parses PEP 621 `pyproject.toml` to obtain name, version, Python requirement, dependencies.
- Resolver: writes `pypackager.lock` TOML with declared dependencies (MVP); later resolves exact versions via pip.
- Environment: builds in per-target ephemeral `venv` environments.
- Pipeline: orchestrates scan → lock → env → builder discovery → build.
- Builders: isolated modules implementing `configure(project_info)` and `build(output_directory)`.
- Plugins: discovered via `importlib.metadata.entry_points` group `pypackager.builders`.

## Contributing
Issues and pull requests are welcome: https://github.com/rithwiksb/pypackager

## License
MIT License. See `LICENSE`.
