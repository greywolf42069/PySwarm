#!/usr/bin/env python

import subprocess
import os
from PYTHON_VERSIONS import PYTHON_VERSIONS

def main():
    print("=== Creating Python virtual environments ===")
    
    for version in PYTHON_VERSIONS:
        print(f"\nProcessing Python {version}")
        subprocess.run(f"pyenv install -s {version}", shell=True)
        
        venv_dir = f"venv-py{version}"
        subprocess.run(f"pyenv shell {version} && pyenv exec python --version && pyenv exec python -m venv {venv_dir}", shell=True)
        print(f"Created {venv_dir}")
    
    print("\n=== All virtual environments created ===")

if __name__ == "__main__":
    main() 