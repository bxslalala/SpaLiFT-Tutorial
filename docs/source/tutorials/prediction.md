# Molecular prediction

First complete the [CPU quick start](quickstart.md). Run this example from the **SpaLiFT source repository root**.

## 1. Generate a target profile

Use slice `a` RNA to predict ATAC gene scores conditioned on slice `b`:

```bash
python -m spalift generate --checkpoint outputs/demo/checkpoint.pt --source data/demo/a_rna.h5ad --source-modality rna --target-modality atac --target-slice b --output outputs/demo/a_to_b_atac.h5 --device cpu
```

The target modality and slice must each have appeared during training. No measured target profile is required at inference.

## 2. Read the result

```python
import h5py

with h5py.File("outputs/demo/a_to_b_atac.h5", "r") as f:
    profiles = f["log_normalized"][:]
    spots = f["source_spots"].asstr()[:]
    available = f["target_feature_available"][:]
    print(profiles.shape)  # (24, 32)
    print(spots[:3])      # Source spot identities
```

Rows remain on the **source spot grid**. Values are continuous log-normalized predictions, can be negative, and are not raw counts. Use the availability mask to exclude unavailable target genes.

Exports are HDF5 files; open them with `h5py`. Choose a new filename when rerunning. For more detail, see [output semantics](../data.md) or run the [notebook](notebook.md).
