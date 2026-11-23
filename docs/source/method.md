# Method and implementation scope

SpaLIFT learns molecular representations and conditional molecular outputs through a shared endpoint-generating pathway. Its implemented inputs are RNA expression and ATAC-derived gene scores on an aligned gene axis. A context identifies a tissue slice and modality.

## Representation and endpoint

The encoder receives a standardized profile, an explicit binary input mask and a learned modality embedding. The mask combines gene availability, any selected encoder features, and artificial masking. The encoder is a deterministic multilayer perceptron. The reference configuration uses hidden widths 512 and 256 and a 64-dimensional latent representation.

A shared target-modality-conditioned decoder maps the representation to a full-gene endpoint, `xT`. Its hidden widths reverse the encoder widths. Hidden layers use layer normalization and SiLU activations. A separate score network receives the perturbed molecular state, endpoint, time encoding, target-modality embedding and target-slice embedding.

The encoder and decoder do not consume slice embeddings or spatial coordinates. Coordinates support input identity checks and exported spatial visualization. This core implementation has no VAE posterior, KL objective, spatial graph convolution or peak-level likelihood.

## Laplace bridge

For observed target `x0`, decoded endpoint `xT`, time `t` and independent unit-scale Laplace noise `epsilon`, the training kernel is

```text
sigma(t) = 2 * beta * sqrt(t * (1 - t))
xt = (1 - t) * x0 + t * xT + sigma(t) * epsilon
score_target = -sign(epsilon) / sigma(t)
```

The reference scale is `beta = 0.5`, and times are sampled between 0.001 and 0.999. The network predicts the scaled score `u = sigma(t) * score`. Its denoising loss averages `(u + sign(epsilon))^2` over supervised, available target features. This is equivalent to weighting unscaled score error by `sigma(t)^2`.

The Gaussian control scales standard normal noise by `sqrt(2) * sigma(t)` to match the variance of the Laplace perturbations.

## Training tasks and correspondence

The trainer builds admissible ordered pairs only from observed contexts.

| Task family | Source and target |
| --- | --- |
| `reconstruction` | Same modality, slice and spot |
| `masked` | Same profile with artificially hidden input features |
| `cross_modal` | Paired spots in different modalities of one slice |
| `cross_slice` | Different slices, same modality |
| `multi_slice_multi_omics` | Different slices and modalities |

The first three families use paired targets. Masking occurs after normalization and standardization, and loss uses the artificially hidden available features. It is a model-space recovery task with a known training target.

For unpaired slices, query and key projections of source/target embeddings define four-head scaled dot-product attention. Softmax normalizes over target candidates, and the head-average matrix `P` weights every candidate source-target bridge loss. Gradients propagate through the correspondence weights and both embedding sets. Rows sum to one; column marginals are unconstrained. This is a directional soft correspondence, not a one-to-one registration or an optimal-transport coupling with prescribed marginals.

Training normalizes attention within the target minibatch. Full correspondence export normalizes over all target spots using a blockwise two-pass calculation.

## Conditional generation

Inference initializes the molecular state at the decoded endpoint at `t = 0.999` and integrates backwards to `t = 0.001` with Heun's predictor-corrector method:

```text
dx/dt = (xT - x) / (1 - t) - 4 * beta^2 * score_theta
```

The reference configuration uses 128 intervals with no terminal random perturbation. This implementation uses heuristic score-driven transport.

Generation is deterministic for fixed model, inputs and integration settings. It requires neither measured target profiles nor a correspondence calculation at inference. The target modality and slice identity must each have appeared among observed training contexts; their combination may have been unobserved. Outputs retain the source spot grid and are continuous inverse-standardized log-normalized values. See [data and output semantics](data.md).

## Optimization and variants

The reference epoch-based trainer uses AdamW, gradient-norm clipping at 5 and fixed sampled validation batches. The family-weighted validation objective selects `checkpoint.pt`; enabled auxiliary losses are included in that objective. Generation diagnostics do not select the checkpoint. There is no learning-rate schedule or early stopping.

With `full_pass: false`, an epoch is a fixed number of updates. With `full_pass: true`, every training source row of every observed context is visited once per epoch, with one eligible task assigned to each batch. It is not a full traversal of every source-target task for every row.

The [paired clustering extension](clustering.md) adds direct endpoint MSE, paired InfoNCE, a training-selected encoder-feature union and an optional local score branch. The paired clustering configurations disable both cross-slice task families.

The code also supports variance and covariance penalties, Gaussian noise and fixed-update training. Fixed-update training saves the final-update checkpoint.
