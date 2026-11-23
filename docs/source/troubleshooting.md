# Troubleshooting

## The output directory already exists

Training and exports intentionally reject existing destinations. Choose a new directory:

```bash
python -m spalift train --config configs/demo.yaml --output-dir outputs/demo_repeat
```

Use the new checkpoint path and new export filenames in subsequent commands.

## Gene or spot identities do not match

All observed contexts need the same unique, ordered `var_names`. Within each slice, paired files must contain the same spot set and matching coordinates after reordering by spot identity. Do not relabel independent spots to force pairing. ATAC availability masks must agree across contexts of the same modality. See [data preparation](data.md).

## Can I generate for an unseen slice?

The target modality and target slice must each appear in observed training contexts. An unobserved combination of known identities is supported; an entirely unseen slice embedding is not.

## Why does anndata.read_h5ad reject an export?

Exports are standard HDF5 files. Use `h5py.File`, or {download}`the output inspector <_downloads/inspect_outputs.py>`. Preserve source identifiers, gene order, feature availability and output scale when converting for downstream tools.

## PowerShell blocks environment activation

Call the environment interpreter directly without changing execution policy:

```powershell
.venv\Scripts\python.exe -m pip install -e .
.venv\Scripts\python.exe examples/make_demo_data.py
.venv\Scripts\python.exe -m spalift train --config configs/demo.yaml
```

## Windows reports a c10.dll initialization error

If Windows reports this error after loading another numerical library, place `import torch` before NumPy, AnnData or clustering imports in your script. The CLI already imports PyTorch first.

## Are generated values counts?

No. `log_normalized` stores inverse-standardized continuous predictions and can be negative. Rows remain indexed by source spots even when the requested target slice differs. See [prediction semantics](tutorials/prediction.md).
