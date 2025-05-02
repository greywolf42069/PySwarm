#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This setup.py is for backward compatibility with pip install.
# For package development, use Poetry.

import setuptools

if __name__ == "__main__":
    setuptools.setup(
        name="pywaves",
        version="2.0.0",
        description="Python library for interacting with the Waves blockchain",
        packages=setuptools.find_packages(),
        install_requires=[
            "requests",
            "python-axolotl-curve25519",
            "base58==0.2.5",
            "protobuf==3.19.6",
        ],
        python_requires=">=3.6",
    ) 