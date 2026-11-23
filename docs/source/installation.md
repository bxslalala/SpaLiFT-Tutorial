# Installation

SpaLiFT requires **Python 3.10–3.12**. The synthetic tutorial runs on CPU. Real-data configurations request CUDA and need a compatible PyTorch installation.

## Obtain the source

Clone the [SpaLiFT source repository](https://github.com/bxslalala/SpaLiFT).

```bash
git clone https://github.com/bxslalala/SpaLiFT.git
cd SpaLiFT
```

Run the installation and tutorial commands from the folder containing `pyproject.toml`, `src/`, `configs/` and `examples/`.

## Create a dedicated environment

With Conda:

```bash
conda create -n spalift python=3.10
conda activate spalift
```

Alternatively, use Python's built-in virtual environments.

### Windows / PowerShell

```powershell
python --version
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
```

## Install SpaLiFT

Install the core package from the source repository root:

```bash
python -m pip install -e .
```

For [downstream clustering](clustering.md), install the optional dependencies with `python -m pip install -e ".[clustering]"`.

For a GPU workflow, install the desired compatible PyTorch build before installing the package. Consult [PyTorch's installation instructions](https://pytorch.org/get-started/locally/).

```{important}
The Python API and CLI use the same code. `python -m spalift` is an alias for `spalift` and makes the selected Python environment explicit.
```

## Check the installation

```bash
python -m spalift --help
```

Continue to the [CPU quick start](tutorials/quickstart.md) for a synthetic end-to-end run.
