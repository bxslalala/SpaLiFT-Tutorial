# CPU quick start

[Install SpaLiFT](../installation.md), then run the commands below from the **SpaLiFT source repository root**. For a cell-by-cell version, use the [notebook](notebook.md).

## 1. Prepare data and train

```bash
python examples/make_demo_data.py
python -m spalift train --config configs/demo.yaml --device cpu
```

The demo creates four synthetic H5AD files: two slices, each with RNA and ATAC gene scores. Every file has 24 spots and 32 genes. Training runs for two short epochs and saves `outputs/demo/checkpoint.pt`.

## 2. Export an embedding

```bash
python -m spalift encode --checkpoint outputs/demo/checkpoint.pt --source data/demo/a_rna.h5ad --source-modality rna --output outputs/demo/a_rna_embedding.h5 --device cpu
```

Inspect it in Python:

```python
import h5py

with h5py.File("outputs/demo/a_rna_embedding.h5", "r") as f:
    print(f["z"].shape)  # (24, 8): source spots × latent features
```

## 3. Continue

Use the same checkpoint for [molecular prediction](prediction.md) or [soft correspondence](correspondence.md).

Existing files are protected from overwrite. For another training run, keep the demo inputs and add `--output-dir outputs/demo_repeat`; use that run's checkpoint and new export filenames afterward. YAML paths are relative to the configuration file.

The synthetic example demonstrates the interfaces, not biological performance. See [data preparation](../data.md) for your own inputs.
