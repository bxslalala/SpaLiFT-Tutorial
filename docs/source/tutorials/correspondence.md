# Soft correspondence

First complete the [CPU quick start](quickstart.md). Run this example from the **SpaLiFT source repository root**.

## 1. Export source-to-target weights

Provide both source and target data:

```bash
python -m spalift correspondence --checkpoint outputs/demo/checkpoint.pt --source data/demo/a_rna.h5ad --source-modality rna --target data/demo/b_atac.h5ad --target-modality atac --target-slice b --output outputs/demo/a_to_b_correspondence.h5 --device cpu
```

## 2. Inspect the matrix

```python
import h5py
import numpy as np

with h5py.File("outputs/demo/a_to_b_correspondence.h5", "r") as f:
    print(f["P"].shape)  # (24, 24): source spots × target spots
    rows = f["P"][:3, :]
    np.testing.assert_allclose(rows.sum(axis=1), 1.0, atol=1e-5)
    print(f["source_spots"].asstr()[:3])
    print(f["target_spots"].asstr()[:3])
```

Each row sums approximately to one. The values are directional soft weights, not validated spot matches or a one-to-one spatial registration. Columns are not constrained to sum to one.

The file stores the full source-by-target matrix, so storage grows with both spot counts. Inspect large exports in blocks and choose a new filename when rerunning. See the [method guide](../method.md) for details, or use the [notebook](notebook.md).
