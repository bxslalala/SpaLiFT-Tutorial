# Tutorials

Start with the **[Jupyter notebook](notebook.md)**. Run its cells in order to prepare a small dataset, train on CPU and inspect the results.

{download}`Download SpaLiFT_step_by_step.ipynb <../../../notebooks/SpaLiFT_step_by_step.ipynb>`

```{figure} ../_static/spalift-framework.png
:alt: SpaLiFT framework overview, including representation learning, cross-slice correspondence and molecular prediction.
:width: 100%
:target: ../_static/spalift-framework.png

SpaLiFT framework. Click to view the full-size figure.
```

## Command-line guides

Prefer the terminal? Follow these short guides from the **SpaLiFT source repository root**:

- [CPU quick start](quickstart.md): create data, train and export an embedding.
- [Molecular prediction](prediction.md): generate a target-modality profile.
- [Soft correspondence](correspondence.md): inspect source-to-target weights.

The examples use synthetic data to demonstrate the software. See [data preparation](../data.md) for real inputs.

```{toctree}
:hidden:
:maxdepth: 1

notebook
quickstart
prediction
correspondence
```
