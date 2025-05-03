#!/usr/bin/env python

import subprocess
import os
import platform
from PYTHON_VERSIONS import PYTHON_VERSIONS
from PYTHON_TESTS import PYTHON_TESTS

def main():
    print("=== Running tests in all Python environments ===")

    for version in PYTHON_VERSIONS:
        print(f"\nRunning tests with Python {version}")
        venv_dir = f"venv-py{version}"
        env = os.environ.copy()
        env["VIRTUAL_ENV"] = os.path.abspath(venv_dir)

        is_windows = platform.system() == "Windows"
        python_path = f"{venv_dir}\\Scripts\\python" if is_windows else f"{venv_dir}/bin/python"

        subprocess.run(f"{python_path} -m pip install poetry", shell=True)
        subprocess.run(f"{python_path} -m poetry lock", shell=True, env=env)
        subprocess.run(f"{python_path} -m poetry install --no-root --with dev", shell=True, env=env)

        for test_path in PYTHON_TESTS:
            print(f"  Running test: {test_path}")
            subprocess.run(f"{python_path} workflow_test.py {test_path}", shell=True)

    print("\n=== All tests completed ===")

if __name__ == "__main__":
    main()
