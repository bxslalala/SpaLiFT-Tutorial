"""Read SpaLIFT HDF5 exports without loading a model or plotting anything.

From the SpaLiFT repository root, after running the three export commands:

    python ../SpaLiFT-Tutorial/examples/inspect_outputs.py outputs/demo

You can also pass one .h5 file. Install h5py if this script is used outside
the SpaLIFT environment: python -m pip install h5py

The artificial demo exercises the software interfaces; its values are not
evidence of biological prediction quality.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import h5py


def text(value: object) -> str:
    """HDF5 attributes may be returned as bytes or ordinary Python strings."""
    return value.decode("utf-8") if isinstance(value, bytes) else str(value)


def require_shape(result: h5py.File, name: str, expected: tuple) -> None:
    """Catch axis mismatches before using exported rows in another analysis."""
    actual = result[name].shape
    if actual != expected:
        raise ValueError(f"{name}: expected shape {expected}, found {actual}")


def inspect(path: Path, preview: int) -> None:
    # .h5 exports are standard HDF5 files, not AnnData .h5ad objects.
    # Opening read-only also guarantees that this script will not alter them.
    print(f"\nFILE: {path.resolve()}")
    with h5py.File(path, "r") as result:
        print("Metadata:")
        for name in sorted(result.attrs):
            print(f"  {name}: {text(result.attrs[name])}")

        if text(result.attrs.get("status", "")) != "complete":
            raise ValueError("Export is not marked complete; do not analyze partial output.")
        kind = text(result.attrs.get("kind", ""))
        required = {
            "encode": ("z",),
            "generate": ("standardized", "log_normalized", "target_feature_available"),
            "correspondence": ("P", "target_spots"),
        }
        if kind not in required:
            raise ValueError(f"Unsupported export kind: {kind!r}")
        names = ("source_spots", "genes", "spatial") + required[kind]
        for name in names:
            if name not in result or not isinstance(result[name], h5py.Dataset):
                raise ValueError(f"Required dataset is missing: {name}")

        print("Datasets (actual shapes and dtypes):")
        for name in sorted(result):
            dataset = result[name]
            if isinstance(dataset, h5py.Dataset):
                print(f"  {name}: shape={dataset.shape}, dtype={dataset.dtype}")

        if result["source_spots"].ndim != 1 or result["genes"].ndim != 1:
            raise ValueError("source_spots and genes must each have one dimension.")
        n_source = result["source_spots"].shape[0]
        n_genes = result["genes"].shape[0]
        require_shape(result, "spatial", (n_source, 2))
        rows = min(preview, n_source)
        source_ids = result["source_spots"].asstr()[:rows].tolist()
        gene_ids = result["genes"].asstr()[:min(preview, n_genes)].tolist()
        print(f"Source spot preview: {source_ids}")
        print(f"Gene preview: {gene_ids}")
        print(f"Source coordinate preview: {result['spatial'][:rows].tolist()}")

        if kind == "encode":
            if result["z"].ndim != 2 or result["z"].shape[0] != n_source:
                raise ValueError("z must have shape (n_source_spots, latent_dim).")
            print("Interpretation: z rows follow source_spots; columns are latent dimensions.")

        elif kind == "generate":
            require_shape(result, "standardized", (n_source, n_genes))
            require_shape(result, "log_normalized", (n_source, n_genes))
            require_shape(result, "target_feature_available", (n_genes,))
            available = result["target_feature_available"][:]
            print(f"Target genes with available annotations: {int(available.sum())}/{n_genes}")
            print(
                "Interpretation: generated rows follow source_spots and columns follow genes.\n"
                "  target_slice conditions the molecular prediction; spatial remains the\n"
                "  SOURCE coordinates. This is not a prediction on a target tissue grid.\n"
                "  log_normalized is inverse-standardized, unclipped continuous output.\n"
                "  Available values can be negative; these are not raw counts. Unavailable\n"
                "  genes are zeroed in log_normalized and marked by the availability mask."
            )

        else:
            if result["target_spots"].ndim != 1:
                raise ValueError("target_spots must have one dimension.")
            n_target = result["target_spots"].shape[0]
            require_shape(result, "P", (n_source, n_target))
            target_ids = result["target_spots"].asstr()[:min(preview, n_target)].tolist()
            print(f"Target spot preview: {target_ids}")

            # Read only a few rows, in column blocks. Even a large correspondence
            # export need not be loaded into RAM just to inspect row sums.
            row_sums = [0.0] * rows
            for start in range(0, n_target, 4096):
                partial = result["P"][:rows, start:start + 4096].sum(axis=1, dtype="float64")
                for row, value in enumerate(partial):
                    row_sums[row] += float(value)
            print("Sampled P row sums (normally near 1): " + ", ".join(f"{x:.8f}" for x in row_sums))
            print(
                "Interpretation: P[i, j] links source_spots[i] to target_spots[j].\n"
                "  Each attention head normalizes over the full target set, then heads\n"
                "  are averaged. These are soft learned weights, not verified matches\n"
                "  or a one-to-one mapping. The row-sum preview is not a quality metric."
            )
        print("Axis checks: passed.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "path", nargs="?", type=Path, default=Path("outputs/demo"),
        help="one HDF5 export, or a directory containing *.h5 exports (default: outputs/demo)",
    )
    parser.add_argument("--preview", type=int, default=3, help="number of identifier/coordinate rows to show (1-20)")
    args = parser.parse_args()
    if not 1 <= args.preview <= 20:
        parser.error("--preview must be between 1 and 20")
    if not args.path.exists():
        parser.error(f"path does not exist: {args.path}; run the SpaLIFT export commands first")
    paths = sorted(args.path.glob("*.h5")) if args.path.is_dir() else [args.path]
    if not paths:
        parser.error(f"no *.h5 exports found in {args.path}; run encode, generate and correspondence first")

    failures = 0
    for path in paths:
        try:
            inspect(path, args.preview)
        except (OSError, KeyError, ValueError, TypeError) as error:
            print(f"ERROR: {path}: {error}", file=sys.stderr)
            failures += 1
    print(f"\nInspected {len(paths)} export(s); {failures} failed inspection.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
