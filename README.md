# PyWaves – Community Edition

[![PyPI version](https://img.shields.io/pypi/v/pywaves-ce.svg)](https://pypi.org/project/pywaves-ce/)

**[PyWaves-CE](https://pypi.org/project/pywaves-ce/)** is a community-maintained fork of the original **[PyWaves](https://pypi.org/project/pywaves/)** library for the Waves blockchain.
It is a *drop-in replacement* that keeps the import path `pywaves` intact, so existing code keeps working without edits.

```bash
pip install pywaves-ce
```

```python
import pywaves as pw           # import path unchanged
print(pw.__version__)          # "2.0.x"
```

> **Notice:**
> `pip install pywaves` (without `-ce`) still installs the unmaintained upstream package.
> Use **pywaves-ce** to get the actively maintained version.

## Purpose & Rationale

- **Unmaintained upstream** – the original [PyWaves](https://pypi.org/project/pywaves/) no longer receives updates.
- **Drop-in replacement** – legacy code keeps using `import pywaves as pw` unchanged.
- **Active maintenance** – security fixes and new Waves features are delivered regularly.
- **Repository layout** – **[PyWaves-CE](https://pypi.org/project/pywaves-ce/)** hosts the pristine [1.0.5 upstream snapshot](https://github.com/PyWaves-CE/PyWaves-CE/tree/PyWaves-1.0.5).
- **PyPI distribution** – published as **pywaves-ce** while the internal package name remains `pywaves`.
- **Versioning roadmap**
  - **1.x** – strict legacy API compatibility with upstream 1.0.5.
  - **2.x** – modernization and intentional breaking changes.

[Documentation](https://github.com/PyWaves-CE/PyWaves-CE/wiki)
