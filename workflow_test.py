#!/usr/bin/env python

import os
import sys
import subprocess

def main():
    if len(sys.argv) < 2:
        print("Usage: python workflow_test.py PATH_TO_TEST_FILE")
        sys.exit(1)
    
    test_path = sys.argv[1]
    if not os.path.exists(test_path):
        print(f"Error: Test file '{test_path}' does not exist")
        sys.exit(1)
    
    sys.path.insert(0, os.path.abspath('.'))
    subprocess.run([sys.executable, '-m', 'pytest', test_path, '-v'])

if __name__ == "__main__":
    main() 