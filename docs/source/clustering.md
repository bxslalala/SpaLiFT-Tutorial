# Paired latent fusion and clustering

SpaLiFT clusters fused RNA and ATAC embeddings within each slice.

## Training configurations

```bash
spalift train --config configs/clustering_global.yaml
spalift train --config configs/clustering_local.yaml
```

Both configurations use the inputs listed in [data preparation](data.md) and write to `outputs/clustering_global` or `outputs/clustering_local`. Use a new output directory for each run. The local profile adds a learned displacement branch to the scaled score. Both profiles train paired tasks within slices.

## Python workflow

Install the `clustering` extra. There is no separate clustering CLI command. The following example evaluates one trained configuration and freezes its validation-selected fusion profiles before test scoring:

```python
import json
from pathlib import Path

from spalift.clustering import extract_latents, search_fusion, final_clusters

run_dir = Path("outputs/clustering_global")
latent_dir = run_dir / "latents"

extract_latents(
    checkpoint=run_dir / "checkpoint.pt",
    output_dir=latent_dir,
    device="cpu",  # Use "cuda" if available.
)

selection = search_fusion(
    latent_dir,
    target_counts={"11": 8, "13": 12, "18": 14},
)
frozen_path = run_dir / "selection_frozen.json"
with frozen_path.open("x", encoding="utf-8") as handle:
    json.dump(selection, handle, indent=2)

with frozen_path.open(encoding="utf-8") as handle:
    frozen_selection = json.load(handle)
results = final_clusters(
    latent_dir,
    frozen_selection,
    run_dir / "clusters",
    seeds=(42, 0, 1),
)
```

Keep the input files at the paths saved in the checkpoint. Latent extraction checks gene and spot identities and restores the saved splits. Use full data without `max_rows` or `max_features`.

Provide `obs['Combined_Clusters_annotation']` for each RNA spot and set `target_counts` to the class count for each slice.

To compare the two profiles, run validation search for both and freeze the model and fusion settings before calling `final_clusters`.
