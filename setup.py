from setuptools import setup, find_packages

setup(
    name="pywaves",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-axolotl-curve25519",
        "base58==0.2.5",
        "protobuf==3.19.6",
        "google-api-python-client",
        "pytest",
        "pytest-cov"
    ],
) 