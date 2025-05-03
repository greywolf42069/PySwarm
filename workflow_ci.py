#!/usr/bin/env python

import sys
import subprocess
from PYTHON_TESTS import PYTHON_TESTS

def main():
    result = subprocess.run([sys.executable, '-m', 'pytest'] + PYTHON_TESTS + ['-v'])
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
