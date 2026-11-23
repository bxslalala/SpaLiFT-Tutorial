# Data preparation and output semantics

SpaLIFT consumes prepared AnnData H5AD files. This repository does not implement sequencing alignment, upstream quality control, peak calling or conversion of ATAC peaks to gene scores. Those steps must be documented with the source dataset.

## H5AD schema

| Field | Required content |
| --- | --- |
| `X` | Spot-by-gene linear-scale RNA measurements or ATAC-derived gene scores |
| `obs_names` | Unique spot identifiers |
| `var_names` | Unique gene identifiers |
| `obsm['spatial']` | Finite numeric array of shape `(n_spots, 2)` |
| `var['genescore_annotation_available']` | Boolean array on the gene axis, required for `modality: atac` |

`X` may be dense, CSR or CSC. Available entries must be finite and non-negative. Values at unavailable ATAC features are excluded before numerical validation and normalization. A measured zero at an available feature is a valid observation; it is different from an unavailable annotation.

All observed contexts must share exactly the same ordered gene axis. Gene-availability masks must agree across contexts of the same modality. RNA treats every gene as available. Paired modalities in one slice must have identical spot sets; row order may differ. After matching spot identifiers, paired coordinates must agree within absolute tolerance `1e-6`. Separate slices need not share spots or coordinates.

Training requires at least three spots per context and enough rows for the requested split fractions. Inference permits a single spot.

## Contexts and missing modalities

A configuration contains a list such as:

```yaml
contexts:
  - {slice: "a", modality: rna, path: ../data/demo/a_rna.h5ad}
  - {slice: "a", modality: atac, path: ../data/demo/a_atac.h5ad}
  - {slice: "b", modality: rna, path: ../data/demo/b_rna.h5ad}
  - {slice: "b", modality: atac, path: ../data/missing_b_atac.h5ad, observed: false}
output_dir: ../outputs/missing_modality_example
```

This fragment illustrates input declaration; choose the remaining training parameters for the experiment. YAML paths resolve relative to the YAML file. Slice identifiers must be strings, and the supported modality names are `rna` and `atac`.

An `observed: false` context is skipped before any file check or read, so its declared file need not exist. It contributes no preprocessing statistics or target values. Other observed contexts must expose the requested modality and slice identity before a missing combination can be generated. The model cannot generate for an entirely unseen slice embedding or an untrained modality.

The core loader reads observed `X`, identifiers, availability and spatial coordinates. It does not read paired layers or biological annotation columns. The separate clustering evaluator reads its reference label column explicitly.

## Normalization and partitions

The loader expects linear-scale measurements. Already log-transformed or standardized input would be transformed again and does not satisfy the documented input semantics. For each observed spot:

1. Sum available genes and scale their values to a total of 10,000 by default.
2. Apply the natural `log1p` transformation. Zero-library rows remain zero at this stage.
3. Standardize genes using modality-specific means and population standard deviations fitted on training spots pooled across observed slices.
4. Replace standard deviations below `1e-6` with 1 and set unavailable standardized dimensions to zero.

The saved preprocessor is reused for held-out spots and exports. Optional encoder feature selection ranks training log-normalized gene variances per modality and takes their union. It does not reduce the decoder's target gene axis.

Partitions use a stable SHA-256 ranking of split seed, slice identity and spot identifier. Paired modalities receive matching split membership. These are within-slice spot partitions; nearby spots may belong to different partitions. They are neither spatial-block nor independent-slice holdouts.

The loader reads observed matrices before splitting. Normalization and model fitting use training rows. Validation uses its assigned rows.

## Real-data configuration paths

`configs/bridge.yaml`, `configs/clustering_global.yaml` and `configs/clustering_local.yaml` expect six input files:

```text
data/11_S1_spatial_rna.h5ad
data/11_S1_genescore_spatial_rna.h5ad
data/13_S1_spatial_rna.h5ad
data/13_S1_genescore_spatial_rna.h5ad
data/18_S1_spatial_rna.h5ad
data/18_S1_genescore_spatial_rna.h5ad
```

Provide these H5AD files or update the `contexts` paths in your configuration. You can try the pipeline with [synthetic inputs](tutorials/quickstart.md).

## HDF5 exports

The export suffix `.h5` denotes standard HDF5, not an AnnData object. Read it with `h5py`:

```python
import h5py

with h5py.File("outputs/demo/a_to_b_atac.h5", "r") as result:
    assert result.attrs["status"] == "complete"
    values = result["log_normalized"][:]
    spots = result["source_spots"].asstr()[:]
    available = result["target_feature_available"][:]
```

All export types store `source_spots`, `genes`, `spatial`, the checkpoint SHA-256 and source information. A completed export has `status = complete`.

- **Embedding:** `z` contains the source latent representation.
- **Generation:** `standardized` retains raw generated model-space values. `log_normalized` applies the saved target-modality inverse standardization, without clipping or exponentiation. Unavailable dimensions are zeroed in `log_normalized` and separately identified by `target_feature_available`.
- **Correspondence:** `P` has shape `(n_source_spots, n_target_spots)` and `target_spots` records its column identities. Export computes full-target normalization rather than a minibatch approximation.

Available generated values can be negative in log-normalized space. They are continuous estimates, not integer counts, measured library sizes or peak accessibility calls. Unavailable genes are not recovered annotation-free measurements. Do not pass these exports back through the raw-input loader without an explicitly defined transformation.

Cross-slice generation keeps source spots and source coordinates. It changes the molecular target context; it does not interpolate onto the target tissue's physical grid. Full `P` export is blockwise on device but still occupies `n_source_spots * n_target_spots` entries on disk.
