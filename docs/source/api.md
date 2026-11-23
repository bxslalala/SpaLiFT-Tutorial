# Python API and command-line interfaces

The examples assume the working directory is the SpaLiFT source repository root, the package is installed, and the [demo inputs](tutorials/quickstart.md) exist.

## Train from Python

```python
from spalift.config import RunConfig
from spalift.trainer import train

config = RunConfig.load("configs/demo.yaml")
config.output_dir = "outputs/demo_api"
summary = train(config)
print(summary)
```

`RunConfig.load` resolves YAML paths relative to that YAML file. Paths assigned directly in Python resolve relative to the working directory. Choose a new output directory for each run.

## Export an embedding

```python
from spalift.exports import export

export(
    "outputs/demo_api/checkpoint.pt",
    source_path="data/demo/a_rna.h5ad",
    source_modality="rna",
    output_path="outputs/demo_api/embedding.h5",
    kind="encode",
    device="cpu",
)
```

The HDF5 file contains `z`, source spot identifiers, the gene axis, source coordinates and checkpoint provenance. It is not an AnnData H5AD file.

## Command-line interfaces

| Command | Purpose | Walkthrough |
| --- | --- | --- |
| `train` | Train from a YAML configuration | [CPU workflow](tutorials/quickstart.md) |
| `encode` | Export molecular latent representations | [CPU workflow](tutorials/quickstart.md) |
| `generate` | Export conditional molecular predictions | [Prediction](tutorials/prediction.md) |
| `correspondence` | Export full directional soft correspondence | [Correspondence](tutorials/correspondence.md) |

Inspect options for the installed version:

```bash
python -m spalift train --help
python -m spalift encode --help
python -m spalift generate --help
python -m spalift correspondence --help
```

Exports default to CPU; use `--device cuda` with a compatible GPU installation. Training and exports reject existing destinations.

## Paired clustering functions

`spalift.clustering` provides `extract_latents`, `search_fusion` and `final_clusters`. There is no clustering CLI subcommand. The [clustering guide](clustering.md) documents reference labels, prescribed class counts and validation selection.

## Checkpoints

Checkpoints contain model parameters, preprocessing, feature/context identities and split membership. They are inference/evaluation artifacts, without the optimizer and complete random-state cursor needed to resume interrupted training.
