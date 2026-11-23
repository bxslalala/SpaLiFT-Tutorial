# SpaLiFT

**Spatial Laplace-informed Framework for Generative Transport**

SpaLiFT integrates spatial RNA and ATAC gene scores to learn shared representations, predict molecular profiles, and explore correspondence across slices.

[Installation](installation.md) · [Run the notebook](tutorials/notebook.md) · {download}`Download .ipynb <../../notebooks/SpaLiFT_step_by_step.ipynb>`

```{figure} _static/spalift-framework.png
:alt: SpaLiFT framework showing spatial omics inputs, representation learning, transport bridges, cross-slice correspondence and multi-omics prediction.
:width: 100%
:target: _static/spalift-framework.png

SpaLiFT framework. Click the figure to view it at full resolution.
```

The CPU notebook walks through data preparation, training and result export. For your own datasets, see [data preparation](data.md) and the [method guide](method.md).

[Source code](https://github.com/bxslalala/SpaLiFT) · [Tutorial repository](https://github.com/bxslalala/SpaLiFT-Tutorial)

```{toctree}
:hidden:
:maxdepth: 2
:caption: Getting started

installation
tutorials/index
```

```{toctree}
:hidden:
:maxdepth: 1
:caption: User guide

data
method
clustering
api
troubleshooting
```
