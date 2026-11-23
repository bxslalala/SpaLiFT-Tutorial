# SpaLiFT documentation and tutorials

The [SpaLiFT documentation](https://bxslalala.github.io/SpaLiFT-Tutorial/) includes installation, a CPU walkthrough, and guides to the model's three outputs. Start with the [runnable Jupyter notebook](notebooks/SpaLiFT_step_by_step.ipynb).

## Preview locally

Build the documentation using the instructions below, then serve `site/` locally.

```bash
python -m http.server 8765 --bind 127.0.0.1 --directory site
```

Open [the local documentation](http://127.0.0.1:8765/). Stop the server with Ctrl+C.

## Build the documentation

Use Python 3.11 in a dedicated environment. This installs documentation tools only; the website does not require PyTorch, biological data, or the model package.

```bash
python -m venv .venv-docs
```

Activate with `.venv-docs\Scripts\Activate.ps1` in PowerShell, or `source .venv-docs/bin/activate` on Linux/macOS. Then:

```bash
python -m pip install -r docs/requirements.txt
python -m sphinx -b html -W --keep-going docs/source site
```

Edit `docs/source/*.md` and rebuild. The generated `site/` and `.venv-docs/` directories are ignored by Git. They do not need to be committed: GitHub Actions builds the website from its Markdown sources.

## Quick start

Run the [Jupyter notebook](notebooks/SpaLiFT_step_by_step.ipynb) from the SpaLiFT source repository. For setup instructions, see [Run the notebook](docs/source/tutorials/notebook.md).

## Publish on GitHub Pages

The `Documentation` workflow checks pull requests and publishes successful `main` builds. See the [publishing guide](docs/PUBLISHING.md) for build and hosting settings.

## Repository layout

```text
docs/source/              Markdown content and Sphinx configuration
notebooks/                Runnable step-by-step Jupyter tutorial
docs/source/_static/      Theme overrides and local figures
docs/source/_downloads/   Bundled configuration and output inspector
docs/requirements.txt     Pinned documentation dependencies
docs/PUBLISHING.md        GitHub Pages and Read the Docs instructions
.github/workflows/docs.yml  Strict build and Pages deployment
.readthedocs.yaml          Optional Read the Docs build
site/                     Generated local HTML, ignored by Git
```

Keep bundled downloads synchronized when the model changes. The model code lives in the separate [SpaLiFT repository](https://github.com/bxslalala/SpaLiFT).
