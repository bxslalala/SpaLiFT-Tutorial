# Publishing the SpaLiFT documentation

The `Documentation` workflow builds and deploys the [SpaLiFT tutorial](https://bxslalala.github.io/SpaLiFT-Tutorial/) to GitHub Pages.

## Build and preview locally

Run these commands from the `SpaLiFT-Tutorial` repository with Python 3.11 in an activated virtual environment:

```bash
python -m pip install -r docs/requirements.txt
python -m sphinx -b html -W --keep-going docs/source site
python -m http.server 8765 --bind 127.0.0.1 --directory site
```

Open [the local preview](http://127.0.0.1:8765/). Stop the server with `Ctrl+C`.

The documentation build installs only `docs/requirements.txt`. It does not check out the sibling SpaLiFT repository, install model dependencies, run training, or need a GPU. Documentation sources and bundled downloads must therefore stay self-contained in this repository. Keep generated `site/` output out of Git; the workflow builds it for publication.

## Publish to GitHub Pages

1. In **Settings > Pages**, choose **GitHub Actions** as the publishing source.
2. Merge the documentation changes into `main`, or run **Actions > Documentation > Run workflow** on `main`.
3. Check that the build and deployment succeed, then open the URL in the `github-pages` deployment summary.

Publish any model changes required by the examples in the [SpaLiFT source repository](https://github.com/bxslalala/SpaLiFT) before publishing the corresponding tutorial update.

The workflow follows GitHub's [custom Pages workflow](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) model:

| Trigger | Behavior |
| --- | --- |
| Pull request targeting `main` | Build HTML with warnings treated as errors; no Pages configuration, artifact upload, or deployment. |
| Push to `main` | Build HTML, upload `site/`, then deploy to the `github-pages` environment. |
| Manual run on `main` | Build and deploy the selected `main` revision. |
| Manual run on another branch | Build only. |

The build has read-only repository permissions. Only the deployment job has `pages: write` and `id-token: write`; it waits for the build to succeed. Existing `github-pages` environment protection rules still apply. No deployment secret or separate `gh-pages` branch is needed for this workflow.

## Optional Read the Docs hosting

The familiar Read the Docs appearance comes from the Sphinx theme and works on GitHub Pages. Hosting on Read the Docs is optional and separate from enabling GitHub Pages.

To use Read the Docs, import this repository and choose the default branch. The root `.readthedocs.yaml` uses Ubuntu 24.04, Python 3.11, `docs/requirements.txt`, and `docs/source/conf.py`, with Sphinx warnings treated as failures. See the [Read the Docs configuration reference](https://docs.readthedocs.com/platform/stable/config-file/v2.html).

## Updating the documentation

Edit the files under `docs/source/`, synchronize bundled examples when the core package changes, and run the strict local build before publication. Pull requests provide a build check. Once the changes reach `main`, the configured Pages workflow rebuilds and replaces the published documentation.

If the build fails, resolve the reported Sphinx warning or error before retrying. If deployment fails while the build succeeds, check the repository's Pages source setting, workflow permissions, and `github-pages` environment rules in GitHub.
