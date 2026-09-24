# Human Activity Recognition from Wearable Inertial Sensors

IT8414 Deep Learning for Data Analytics, Assessment 2 (group project).

Six-class classification of human activity (walking, walking upstairs, walking
downstairs, sitting, standing, laying) from 2.56-second windows of raw
accelerometer and gyroscope signal recorded by a waist-worn smartphone
([UCI HAR dataset](DATA.md)). Two PyTorch models are compared: a 1-D CNN
baseline and a CNN-LSTM. Every data split is by **subject**, so all reported
results are on people the model never trained on.

**Deployed model: the baseline 1-D CNN** (44,422 parameters). On the nine
held-out test subjects it reaches 91.5% accuracy and 0.917 macro F1 (four-seed
mean 0.912 ± 0.005). Most remaining errors are sitting ↔ standing confusions,
concentrated in people whose two postures tilt the phone almost identically
(notebook §9.4).

| Member | Notebook sections |
|---|---|
| Ahmad Abbas | 1.0–4.0 (data, EDA, split, preprocessing) and Appendix A (live demonstration) |
| Khalifa Alhashel | 5.0–7.0 (baseline, CNN-LSTM, hyperparameter experiments) |
| Rashed Ramadham | 8.0–10.0 (test evaluation, interpretability, error analysis, conclusion) |

Every code cell names its author in its first line.

## Repository layout

| Path | Contents |
|---|---|
| `IT8414_HAR.ipynb` | The notebook: all code, executed, with outputs saved |
| `IT8414_HAR.html` | HTML export of the executed notebook |
| `figures/` | Figures 1–15, written by the notebook and reused in the report |
| `scripts/get_data.py` | Downloads the dataset, verifies its SHA-256, extracts it |
| `DATA.md` | Dataset source, licence, split rationale, known limitations |
| `requirements.txt` | Pinned library versions |
| `CLAUDE.md` | Working notes and conventions used while building the project |
| `data/` | The dataset (created by `get_data.py`; not in git) |
| `models/` | Trained weights (created by the notebook; not in git) |

## Environment

Python **3.12.10** on Windows 10. Library versions, pinned in
`requirements.txt`:

| Library | Version |
|---|---|
| torch | 2.14.0+cpu |
| numpy | 2.5.3 |
| pandas | 3.0.6 |
| scikit-learn | 1.9.1 |
| matplotlib | 3.11.2 |
| notebook | 7.6.3 |
| ipykernel | 7.3.0 |
| nbconvert | 7.17.1 |

PyTorch is the **CPU-only** build on purpose. The live demonstration runs on a
campus machine whose GPU cannot be relied on, and the models are small enough
that a GPU brings no benefit. The notebook still uses a GPU automatically if one
is available.

## Setup

From the repository root, in PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu
python scripts/get_data.py
jupyter notebook IT8414_HAR.ipynb
```

`get_data.py` needs internet access once. After that everything runs offline.
To prepare a machine without internet access, copy the whole `data/` folder
across instead.

## Reproducing the results

Open the notebook and use **Kernel → Restart Kernel and Run All Cells**. A full
run takes about **7 minutes** on a 6-core desktop CPU (i5-12400F). Most of that
time goes to the multi-run studies in §6.3, §7.0 and §8.3, which train 34 models
between them.

Every random source is seeded (seed 42, set in §1.0). On the same machine, two
runs give **bit-identical** results. On a machine with a different number of CPU
cores, results can differ in the last decimal places, because PyTorch adds up
floating-point numbers in a different order when it uses a different number of
threads. The conclusions do not depend on those digits.

To regenerate the HTML export after a run:

```powershell
jupyter nbconvert --to html IT8414_HAR.ipynb
```

## Live demonstration

The brief allots about five minutes to the demonstration and five to the live
modification. A full run is far too slow for that on an unknown machine, so the
procedure below prepares the notebook in under a minute and leaves the slow
studies alone. Their results are already saved in the notebook's outputs.

### Before the session

1. Install the environment on the demonstration machine and check that
   `data/UCI HAR Dataset/` exists. Environment failures on the day are not
   grounds for a re-sit.
2. Rehearse the warm-up below on that machine at least once.
3. Close heavy programs such as games. A game running during one of our runs
   doubled every training time.

### Warm-up: at the start of the session

1. Open `IT8414_HAR.ipynb`.
2. In §6.3, click the markdown cell headed **"Is the difference real, or seed
   luck?"**.
3. Choose **Run → Run All Above Selected Cell**.

This runs §1.0 to §6.2. It loads the data, rebuilds the subject-wise split,
trains both models and saves their weights to `models/`.

| Machine | Warm-up | One baseline retrain |
|---|---|---|
| i5-12400F, 6 threads | 26 s | 9 s |
| Same CPU limited to 2 threads | 38 s | 13 s |
| Same CPU limited to 1 thread | 58 s | 23 s |

**Do not use Run All** for the demonstration.

### Demonstration: Appendix A

Scroll to **Appendix A** at the end of the notebook and run its first code cell,
which loads the saved model. In the next cell, set `split` (`"train"`,
`"validation"` or `"test"`) and `index` to the window the tutor chooses, then
run it. It prints the true activity, the prediction with its probability, and
all six class probabilities, and plots the window. A commented line in the same
cell picks a window by subject and activity instead.

### Live modification: what to re-run

| Change | Edit | Then run |
|---|---|---|
| A `CONFIG` value (activation for all blocks, dropout, learning rate, batch size, optimiser, loss, epochs, patience) | The `CONFIG` cell in §1.0 | The `CONFIG` cell, then **"Training the baseline"** (§5.2), then the learning-curves cell (§5.3) |
| One specific layer, e.g. the activation of `block2` only | The `BaselineCNN` cell in §5.1 | That cell, then §5.2 training, then §5.3 curves |
| The improved model | The `CNNLSTM` cell in §6.1, or `CONFIG` | That cell, the §6.2 training cell, then the §6.3 curves cell |
| Anything in §8: per-class metrics, the confusion matrix on another split | The §8 cell concerned | First, once: §8's cell that loads the two models, then the cell defining `predict_proba` and `evaluate`. Then the edited cell |

**Retrain both models after any `CONFIG` change before running §8.** §8 rebuilds
both models from the current `CONFIG` and checks that the saved weights
reproduce the trained models. If only the baseline was retrained, the saved
CNN-LSTM no longer matches the new `CONFIG` and that check stops with an error.
Re-running the §6.2 training cell as well (about 10 s) avoids it.

Two §8 calls that are one argument away from what the notebook already does:

```python
evaluate(models["Baseline CNN"], X_test_std, y_test, average=None)["recall"]   # per-class recall
plot_confusions(X_val, y_val, "validation", 10, "confusion_validation")          # validation split
```

**Restoring the original results:** set `CONFIG` back and re-run the `CONFIG`
cell, §5.2 and §6.2. Training is deterministic, so this recreates the original
weights exactly on the same machine.

## Submission

The brief asks for a ZIP named `IT8414_Group[NN]_[ShortProjectTitle].zip` plus
the GitHub link. From this repository, include the notebook, its HTML export,
`figures/`, `scripts/`, `DATA.md`, `README.md` and `requirements.txt`. Leave out
`.venv/` and `data/` (`DATA.md` and `get_data.py` reproduce the dataset).
