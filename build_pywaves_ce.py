#!/usr/bin/env python3
"""
build_pywaves_ce.py

A script to build a pywaves-ce distribution in a temporary directory,
preserving the original PyWaves package structure and metadata.
"""
import os
import sys
import shutil
import tempfile
import subprocess


def main():
    repo_root = os.path.abspath(os.path.dirname(__file__))
    build_root = os.path.join(repo_root, 'temp')
    if os.path.exists(build_root):
        shutil.rmtree(build_root)
    os.makedirs(build_root)
    tmpdir = build_root
    print(f"Building pywaves-ce package in {tmpdir}")

    print("Checking for setuptools and wheel...")
    try:
        import setuptools, wheel
        print("setuptools and wheel already available")
    except ImportError:
        print("Bootstrapping pip, setuptools, and wheel...")
        try:
            import ensurepip
            ensurepip.bootstrap(upgrade=True)
        except Exception:
            print("ensurepip not available; downloading get-pip.py")
            import urllib.request
            get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
            with urllib.request.urlopen(get_pip_url) as resp:
                script = resp.read()
            exec(script, {'__name__': '__main__'})
        print("Installing setuptools and wheel via pip")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "setuptools", "wheel"])

    pkg_dst = os.path.join(tmpdir, "pywaves")
    os.makedirs(pkg_dst)

    modules = [
        "__init__.py",
        "address.py",
        "asset.py",
        "contract.py",
        "crypto.py",
        "ParallelPyWaves.py",
        "WXFeeCalculator.py",
        "txGenerator.py",
        "txSigner.py",
        "oracle.py",
        "order.py",
    ]

    for fname in modules:
        src = os.path.join(repo_root, fname)
        dst = os.path.join(pkg_dst, fname)
        if os.path.exists(src):
            shutil.copy2(src, dst)
        else:
            print(f"Warning: {fname} not found in repo root.")

    src_waves = os.path.join(repo_root, "protobuf", "waves")
    dst_proto = os.path.join(pkg_dst, "protobuf")
    dst_waves = os.path.join(dst_proto, "waves")
    if os.path.exists(src_waves):
        os.makedirs(dst_waves, exist_ok=True)
        open(os.path.join(dst_proto, "__init__.py"), "w").close()
        open(os.path.join(dst_waves, "__init__.py"), "w").close()
        waves_files = [
            "amount_pb2.py",
            "block_pb2.py",
            "invoke_script_result_pb2.py",
            "order_pb2.py",
            "recipient_pb2.py",
            "transaction_pb2.py",
        ]
        for fname in waves_files:
            src = os.path.join(src_waves, fname)
            dst = os.path.join(dst_waves, fname)
            if os.path.exists(src):
                shutil.copy2(src, dst)
            else:
                print(f"Warning: protobuf/waves/{fname} not found in repo root.")
    else:
        print("Warning: protobuf/waves directory not found in repo root.")

    for fname in ("README.md",):
        src = os.path.join(repo_root, fname)
        if os.path.exists(src):
            shutil.copy2(src, tmpdir)
        else:
            print(f"Warning: {fname} not found in repo root.")

    setup_py = os.path.join(tmpdir, "setup.py")
    with open(setup_py, "w", encoding="utf-8") as f:
        f.write("""from setuptools import setup, find_packages

setup(
    name="PyWaves-CE",
    version="1.0.5",
    description="Object-oriented library for the Waves blockchain platform",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="PyWaves Developers",
    author_email="dev@pywaves.org",
    url="https://github.com/PyWaves-CE/PyWaves-CE",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "base58==0.2.5",
        "python-axolotl-curve25519",
        "requests",
        "google-api-python-client",
        "protobuf==3.19.6"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="waves blockchain analytics",
    python_requires=">=3.6",
)
""")

    manifest = os.path.join(tmpdir, "MANIFEST.in")
    with open(manifest, "w", encoding="utf-8") as f:
        f.write("""include README.md
""")

    print("Running build...")
    subprocess.check_call([sys.executable, "setup.py", "sdist", "bdist_wheel", "--universal"], cwd=tmpdir)

    dist_dir = os.path.join(tmpdir, "dist")
    print(f"Build complete. Distributions are located in: {dist_dir}")

    print("Checking for twine...")
    try:
        import twine
        print("twine already installed")
    except ImportError:
        print("Installing twine...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "twine"])

    import glob
    dist_files = glob.glob(os.path.join(dist_dir, "*"))
    print("Distributions to process:", dist_files)
    print("Running twine check...")
    subprocess.check_call([sys.executable, "-m", "twine", "check"] + dist_files)
    print("Uploading with twine...")
    subprocess.check_call([sys.executable, "-m", "twine", "upload"] + dist_files)
    print("Upload complete!")


if __name__ == "__main__":
    main() 