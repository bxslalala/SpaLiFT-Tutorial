# Run the notebook

{download}`Download SpaLiFT_step_by_step.ipynb <../../../notebooks/SpaLiFT_step_by_step.ipynb>`

## 1. Set up

Follow [Installation](../installation.md) using Python 3.10–3.12. Save the notebook inside the **SpaLiFT source repository**, then run these commands there in your activated environment:

```bash
python -m pip install -e .
python -m pip install jupyterlab ipykernel
python -m ipykernel install --user --name spalift --display-name "Python (SpaLiFT)"
python -m jupyterlab
```

## 2. Run the cells

Open the notebook, select **Python (SpaLiFT)**, and press **Shift+Enter** to run each cell in order. The workflow is:

**Prepare data → Train → Encode → Predict → Inspect correspondence**

The small synthetic example runs on CPU. Each complete run creates a new directory and keeps earlier results intact.

## 3. Check the results

You will obtain an embedding `(24, 8)`, molecular predictions `(24, 32)`, and correspondence weights `(24, 24)`. The notebook includes checks and example outputs.

If the source folder is not found, set `SOURCE_REPO` in the notebook. If you keep the notebook in the sibling tutorial repository, launch Jupyter from their common parent so both folders are visible. For a fresh run, use **Restart Kernel and Run All**.
