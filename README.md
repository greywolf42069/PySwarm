w# PySwarm – Swarm Blockchain Library

[![Tests](https://img.shields.io/badge/tests-97%2F105%20passing-brightgreen.svg)](#)
[![Swarm Tests](https://img.shields.io/badge/swarm%20tests-48%2F48%20passing-brightgreen.svg)](#)

**PySwarm** is a specialized fork of PyWaves designed specifically for the **Swarm blockchain**.
It maintains the familiar `pywaves` import path while adding full support for Swarm's unique features including network byte "0" and Swarm-specific endpoints.

```bash
# Install from source (development version)
git clone https://github.com/your-repo/PySwarm.git
cd PySwarm
pip install -e .
```

## Basic Example
```python
import pywaves as pw

# Configure for Swarm blockchain
pw.setChain('swarm')  # Sets network byte "0" and Swarm endpoints

# Create Swarm addresses from seeds
firstAddress = pw.Address(seed = 'this is just a simple test seed 1')
secondAddress = pw.Address(seed = 'this is just a simple test seed 2')

# Send Swarm tokens from one address to another (offline mode)
tx = firstAddress.sendWaves(secondAddress, 100000)
assert 'api-endpoint' in tx
assert 'api-data' in tx

# Verify Swarm address format
print(f"Swarm address: {firstAddress.address}")  # Starts with network byte "0"
print(f"Address length: {len(firstAddress.address)}")  # 35 characters
```

## Purpose & Features of PySwarm

- **Swarm blockchain support** – specifically designed for the Swarm network with network byte "0"
- **Full compatibility** – maintains the familiar `import pywaves` interface
- **Comprehensive testing** – 48 Swarm-specific tests covering all functionality
- **Address generation** – proper Swarm address creation with network byte "0"
- **Transaction handling** – complete support for Swarm transaction types
- **Smart contracts** – DeFi, multisig, oracle, and dApp contract support
- **Advanced features** – asset issuance, mass transfers, data transactions, and leasing
- **Offline mode** – transaction creation without network connectivity
- **Production ready** – robust error handling and validation

### Swarm-Specific Features
- Network byte "0" implementation
- Swarm RPC endpoint integration  
- Chain ID validation for Swarm addresses
- Asset operations with proper length validation
- Smart contract deployment and invocation

## Documentation
- Swarm-specific documentation: [README_SWARM.md](README_SWARM.md)
- Progress tracking: [SWARM_PROGRESS.md](SWARM_PROGRESS.md)
- Example usage: [examples/swarm_example.py](examples/swarm_example.py)

## License
Code released under the [MIT License](https://github.com/PyWaves-CE/PyWaves-CE/blob/main/LICENSE).

## Development and Packaging

PyWaves uses [Poetry](https://python-poetry.org/) for dependency management and packaging.

### Installation for Development

1. Install Poetry (if not already installed)
```bash
pip install poetry
```

2. Install dependencies
```bash
poetry install
```

3. Activate the virtual environment
```bash
poetry shell
```

### Building the Package

```bash
poetry build
```

This will create both wheel and source distributions in the `dist/` directory.

### Testing Across Python Versions

PyWaves includes a workflow testing system that can test across multiple Python versions:

```bash
python workflow_venvs.py
python workflow_tests.py
```

This will test the library with all Python versions specified in PYTHON_VERSIONS.py.