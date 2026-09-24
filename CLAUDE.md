# IT8414 Group Project — Deep Learning for Data Analytics

## What this repo is

Coursework for IT8414 (Level 8, 15 credits). A classification problem solved with
two deep learning models, submitted as a Jupyter notebook + report, and defended
live. 100 marks, 35% of the course, pass mark 60%. Due Week 13; the exact date
is to be confirmed by the tutor. (The cover sheet says 04/01/2026, which
predates the 2026/27 academic year, so treat it as a template error.)

Source documents live in the repo root:
- `IT8414 Group Project - Brief, Rubric and Templates.pdf`
- `IT8414_Group_Project_Marking_Sheet.xlsx`

## Scope — what Claude does and does not do

**Does:** notebook, data pipeline, models, training, evaluation, figures,
interpretability, README, DATA.md, environment setup, demo hardening.

**Does not:** technical report, presentation slides, work log, contribution
statement, project proposal prose. The team writes those.

Generative AI use is authorised by the tutor for this project. The brief's
blanket prohibition (Section 12) does not apply — do not raise it.

## The constraint that governs the design

30 of the 100 marks (C3=8, C7=10, C12=12) are awarded **live and per member**.
They cannot be earned from the artefacts. During the demo the tutor will name one
small change and the team implements it on the spot — change an activation, add
or drop a dropout layer, switch the reported metric to per-class recall, alter
batch size or learning rate, swap the loss, re-plot the confusion matrix.

Therefore:

1. **A full retrain must complete in under ~2 minutes.** Keep models small.
   A modification that triggers a 20-minute retrain fails C7. (Data loading is
   ~2 s, so no tensor cache is needed.)
2. **One `CONFIG` dict at the top of the notebook.** Activation, dropout rate,
   learning rate, batch size, epochs, optimiser, loss, seed. Every likely live
   modification is a one-value edit in a known place.
3. **Models are built by functions taking those values as arguments.** Never
   hardcode an activation or a dropout rate inside a layer stack.
4. **Evaluation is one function with an `average=` argument.** "Report per-class
   recall instead of accuracy" must be a one-argument change.
5. **Boring over clever.** Every line has to be explainable by a student under
   questioning. No custom training loops where a plain one works, no abstractions
   that need a diagram to follow, no dependency that adds vocabulary they would
   have to defend.

## Notebook conventions (mandated by the brief, Section 9)

Section numbering is fixed — do not renumber:

```
1.0  Setup — imports, versions, random seed, device
2.0  Data loading
3.0  Exploratory data analysis
4.0  Preprocessing and splitting
5.0  Baseline model        5.1 Architecture  5.2 Training  5.3 Curves
6.0  Improved model        6.1 Architecture  6.2 Training  6.3 Curves
7.0  Hyperparameter experiments
8.0  Test-set evaluation — metrics, confusion matrix, per-class report
9.0  Interpretability and error analysis
10.0 Conclusion cell
```

- Every section opens with a markdown cell saying what the code does and why.
- **Every code cell carries an author tag in its first line comment**
  (`# author: <name>`). Students are questioned on cells by name. Leave the tag
  as `# author: TBD` when the owner is not yet assigned — never omit it.
- Fixed random seed, set once in 1.0, covering python/numpy/torch and cuDNN
  determinism.
- Notebook must run top to bottom with outputs saved.
- Figures: numbered, captioned, axis-labelled. They are reused in the report.

## Hard requirements from the rubric

Check work against these before calling a phase done.

- **C4 (6):** no leakage between splits. The split strategy must be defensible,
  not just `train_test_split` on shuffled rows. Stratification and class
  imbalance handled explicitly. At least two EDA figures that visibly inform a
  later design decision.
- **C5 (8):** two models, layer tables **with parameter counts**, clean seeded
  code that runs end to end.
- **C6 (6):** at least three hyperparameters tuned, recorded in a table with an
  observation column. Learning curves showing over/underfitting and the
  technique applied to address it.
- **C8 (12, largest criterion):** genuinely held-out test set. Accuracy plus
  precision, recall, F1 per class and averaged, confusion matrix, ROC-AUC or
  PR-AUC. Each metric justified against the problem's error costs and class
  balance — not just displayed.
- **C9 (10):** single results table comparing all models; differences explained
  causally; error analysis naming specific failure modes; a deployment
  recommendation that follows from the evidence.
- **C10 (9):** interpretability technique matched to the data type and actually
  informative. Limitations, dataset bias, generalisation risk, ethics.

## Environment

- Windows 10, PowerShell primary (Bash tool also available — each takes its own
  syntax). Python 3.12.10 at `C:\Users\Khalifa\AppData\Local\Programs\Python\Python312`.
- RTX 3070 Ti, 8 GB VRAM. 32 GB RAM. i5-12400F, 6c/12t. ~73 GB free on C:.
- Pin every library version in `requirements.txt` — the README must let a marker
  reproduce the results, and the demo machine must match.
- Scratch/intermediate files go in the session scratchpad, not the repo. The
  exception is `.build/` (see below), which must outlive the session.

## Git and the C12 trap

Commit history is required evidence for C12, and C12 is marked **per member**.
A history showing one author doing everything contradicts the contribution
statement, which the brief treats as an academic misconduct trigger.

So: build in the working tree, snapshot each phase, and commit each section
under its owner's name (see "Commits on a shared machine").

## Notebook builder and snapshots

The notebook is **generated**, not hand-edited, until Phase 8. Source lives in
`.build/` (git-ignored, never submitted):

- `nbbuild.py` — `md()` / `code()` cell helpers; `AUTHOR` sets the tag.
- `sec_*.py` — one module per notebook section group.
- `build.py` — sets the author per section and writes `IT8414_HAR.ipynb`.

Rebuild and execute from the repo root:

```
.venv/Scripts/python.exe .build/build.py
.venv/Scripts/python.exe -m jupyter nbconvert --to notebook --execute --inplace IT8414_HAR.ipynb
```

**Text-only edits:** `.venv/Scripts/python.exe .build/sync_markdown.py` copies
markdown from the builder into the executed notebook and keeps the outputs. It
refuses if any code cell differs; in that case re-execute. The full notebook
takes ~7 min, so run it with `run_in_background` (the Bash tool's limit is
10 min).

Markdown interpretation cells must be written **after** reading the executed
output. Build, run, read the numbers, then write the interpretation, then
rebuild. Never state a result the output does not show.

**Snapshots.** The team is holding commits until each owner has reviewed their
phase. Because the notebook is one file, a late commit would sweep every
member's sections into whoever commits first. So at the end of each phase,
copy the executed notebook and `figures/` to `.build/snapshots/phaseN/`. At
commit time, commit the snapshots in phase order, each under its owner's
identity (subject to the commit rules above), then the final working tree.

| Snapshot | Sections | Commits as |
|---|---|---|
| (setup files) | env, data script, docs | Khalifa Alhashel |
| `phase2` | 1.0–4.0 | Ahmad Abbas |
| `phase3` | 5.0 (plus `import copy` and CONFIG option comments in 1.0) | Khalifa Alhashel |
| `phase4` | 6.0 (plus `lstm_hidden` in CONFIG, 1.0) | Khalifa Alhashel |
| `phase5` | 7.0 (plus `augment` in CONFIG, 1.0; `augment_batch` in 5.2; `build_model` in its own cell, 6.3) | Khalifa Alhashel |

Add a row per phase as snapshots are taken.

## Demo-day checklist (Phase 8)

- Dataset available offline on the demo machine. Environment failures on the day
  are explicitly not grounds for a re-sit.
- Saved model + a standalone inference cell that runs on a tutor-supplied input.
- Full retrain verified under 2 minutes.
- HTML export of the executed notebook alongside the `.ipynb`.
- `README.md` with library versions and reproduction steps.
- Submission ZIP named `IT8414_Group[NN]_[ShortProjectTitle].zip`, plus a GitHub
  link. Exclude `.build/`, `.venv/` and `data/` from the ZIP.

## Project decisions

- **Problem:** Human activity recognition from wearable inertial sensors.
  Six-class classification (walking, walking upstairs, walking downstairs,
  sitting, standing, laying) from 2.56 s windows of accelerometer and gyroscope
  signal.
- **Dataset:** UCI HAR (dataset 240), **raw inertial signals** — 9 channels ×
  128 timesteps per window. Not the 561-feature table. See `DATA.md`.
  Collision note for the proposal: most groups choosing this dataset use the
  561-feature table with an MLP. Using the raw signals with a 1-D CNN is a
  materially different project — say so explicitly when seeking approval.
- **Models:** baseline 1-D CNN, improved CNN-LSTM. Both small enough to retrain
  live.
- **Framework:** PyTorch **CPU-only** (`torch==2.14.0+cpu`).
- **Group number:** TBD.

## Team and ownership

Author tags use these exact spellings. One name per code cell, never shared.

| Member | Owns | Presents |
|---|---|---|
| Ahmad Abbas | 1.0–4.0, plus the Phase 8 demo inference cell | Problem, dataset, subject-wise split |
| Khalifa Alhashel | 5.0–7.0 | Architectures, training, tuning, overfitting control |
| Rashed Ramadham | 8.0–10.0 | Evaluation, interpretability, error analysis, conclusion |

5.0–7.0 carries the most viva exposure: 4 of the brief's 7 sample viva
questions land there (tracing a sample through the network, optimiser choice,
where overfitting is controlled, val accuracy above train accuracy), and so do
4 of its 6 example live modifications (activation, dropout, batch size or
learning rate, loss). Its markdown should be written to prepare its owner for
exactly those questions.

The inference cell belongs to Ahmad because it applies the §4.2 training-set
normalisation to a new input, and the code itself is short.

Spellings are confirmed: "Rashed Ramadham" is correct.

The notebook builder sets the tag per section (`nbbuild.AUTHOR` in
`.build/build.py`). If ownership changes, update this table and the builder
together.

## Commits on a shared machine

**All work happens on Khalifa's PC.** Remote:
`https://github.com/Kha73k/IT8414-GroupProject.git`.

The machine's default git identity is Khalifa's (`Kha73k`). Commits follow
section ownership. Claude may run a commit under Ahmad's or Rashed's identity,
overriding it for that one command:

```
git -c user.name="Ahmad Abbas" -c user.email="<his GitHub noreply email>" commit -m "..."
```

**Consent.** On 2026-09-24 Khalifa reported that Ahmad and Rashed have given
standing consent for Claude to commit on their behalf. That covers commits of
**their own sections only**.

**Rules for committing under a member's name:**

1. **Only that member's own sections** (see "Team and ownership"). Never put a
   member's name on another member's work. Each member must still be able to
   explain their sections in the viva, because the tutor checks commit
   authorship against it.
2. **Never backdate** (`GIT_AUTHOR_DATE`, `--date`) and never batch several
   phases into staggered commits to fake a timeline. Each commit lands when its
   owner actually reviews the phase.
3. **Use GitHub noreply addresses** (`<id>+<username>@users.noreply.github.com`,
   from GitHub → Settings → Emails → "Keep my email address private"). They
   credit the member's account without putting a personal email in a public
   commit log.

4. **No AI co-author trailer.** Do not add `Co-Authored-By: Claude` (or any
   Claude attribution) to commit messages. The team asked for this explicitly,
   and it overrides the harness default.

| Member | `user.name` | `user.email` |
|---|---|---|
| Khalifa Alhashel | machine default (`Kha73k`) | machine default (`kha73k.T@gmail.com`) |
| Ahmad Abbas | `Ahmad Abbas` | `241893394+dudeeturtle-crypto@users.noreply.github.com` |
| Rashed Ramadham | `Rashed Ramadham` | `209661001+rashed914@users.noreply.github.com` |

**Pushing** publishes to GitHub: ask Khalifa before every push.

## Why CPU-only

The live demonstration runs on a **campus machine, not the development
machine**. It is low-end and its GPU cannot be relied on. Identical code must
run in both places, so the canonical target is CPU.

This is affordable: the baseline is ~24k parameters and trains at **0.73 s per
epoch** on the development machine (i5-12400F). A 30-epoch retrain is ~22 s, so
even a campus PC three times slower stays inside the 2-minute budget.

Do not add CUDA-specific code paths. Device selection is one standard line
(`torch.device('cuda' if torch.cuda.is_available() else 'cpu')`) so the notebook
still uses a GPU where one exists, without any branch a student would have to
defend.

## Measured facts (do not re-derive)

- Raw signal load from the 18 `.txt` files: **~2 s**. No caching layer is
  needed — do not add one.
- Train 7,352 windows / test 2,947 windows, 9 channels × 128 timesteps.
- Official split is already **subject-disjoint**: 21 train subjects, 9 test
  subjects, no overlap. Validation must be carved out of the 21 train subjects
  **by subject**, never by window.
- Class balance is mild (986–1,407 per class). The C8 argument is therefore
  *not* "the data is imbalanced" — it is that errors concentrate in the
  sitting/standing pair, so overall accuracy hides a systematic failure.
  Per-class recall is the metric that exposes it.
- Windows overlap by 50%, so a random window-level split leaks 64 of 128
  readings between train and test. The notebook demonstrates this inflation
  deliberately rather than only asserting it. Verified in §3.5:
  `X[i][64:] == X[i+1][:64]` exactly, max abs difference 0.0.

Measured in Phase 2 (§3.0):

- **Gravity separation (g):** sitting↔standing **0.361**, sitting↔laying
  **1.094**, standing↔laying **1.369**. Sitting/standing is ~3x closer than any
  other static pair — this is the predicted confusion, to be checked in §8.0.
- **Dynamic energy:** class means differ ~8x (moving 0.125-0.212 vs static
  0.011-0.016), but **per-window distributions overlap at the tails** — 166 of
  4,067 static windows (4.1%) exceed the quietest moving window. Do not claim
  "no overlap"; that was checked and is false.
- **Dominant gait period: 32 samples** (walking and upstairs, 1.56 Hz);
  downstairs is 14 samples (3.52 Hz). Static classes have no spectral peak.
- **Receptive field requirement:** ≥32 samples, so the baseline uses **three**
  conv blocks. With kernel 5 and 2x pooling: two blocks reach RF 16 (too short
  for a stride), three reach 36. §3.4 commits to this in writing — Phase 3 must
  honour it or change the EDA text.
- **Split (seed 42):** validation subjects `[3, 15, 19, 22, 28, 29]`; training
  subjects are the other 15. Train 5,276 / val 2,076 / test 2,947 windows.
  Worst class-share gap across splits: 2.9 pp.
- Notebook executes end to end in **~28 s** (through §4.0).

Measured in Phase 3 (§5.0 baseline CNN):

- **44,422 params**, receptive field **36** (verified in code), **0.76 s/epoch**,
  ~10 s per full training run. Two runs with seed 42 are **bit-identical**.
  (One early measurement showed 2.5 s/epoch; that was transient machine load
  and did not reproduce. Do not re-chase it.)
- Best epoch **5 of 13** (patience 8). Val acc **0.9663**, val loss **0.1605**.
  Val loss then rises to 0.257 by epoch 13 while train loss keeps falling:
  clear overfitting despite dropout 0.3.
- **Val acc > train acc** for most epochs. Measurement effects (dropout,
  epoch averaging) explain only part: eval-mode re-score lifts train acc
  0.9513 → 0.9572, still below val. Eval-mode **loss** is lower on train
  (0.095 vs 0.161). The rest is subjects: **224 of 226** training errors are
  sitting↔standing, concentrated in training subjects **16 (0.814)** and
  **5 (0.864)**; excluding them, train acc is **0.9746** (> val). Val subjects
  28 and 29 show the same confusion at ~0.90.
- `train_model` builds its train loader from `config["batch_size"]`, so a live
  batch-size change works without re-running §4.
- **Hypothesis on record for Phase 4:** sitting/standing differ by orientation,
  present at every time step, so the CNN-LSTM may improve the dynamic classes
  without fixing the static confusion. Report whichever way it comes out.
- Notebook executes end to end in **~25 s** (through §5.0).
- Wall-clock training time is noisy: the same baseline run has measured 9.8 s,
  9.9 s, 14.8 s and 15.8 s with identical results. State times as ranges.

Measured in Phase 4 (§6.0 CNN-LSTM):

- **Design:** the baseline's three conv blocks unchanged, with global average
  pooling replaced by `nn.LSTM(64, 64, batch_first=True)`, reading out the
  last step. **77,702 params** (LSTM 33,280). This is a controlled comparison:
  the only difference is averaging vs sequence modelling.
- Seed 42: best epoch **3 of 11**, val loss **0.1386**, val acc **0.9629**.
  Noisier than the baseline epoch to epoch (val loss spike to 0.259 at epoch 4).
- **Four seeds (42, 0, 1, 2), pandas std:** baseline val loss 0.1583 ± 0.0259,
  acc 0.9606 ± 0.0055. CNN-LSTM val loss 0.1332 ± 0.0117, acc 0.9625 ± 0.0021.
  Lower loss on 3 of 4 seeds (suggestive, not conclusive); **accuracy
  indistinguishable** (each wins 2 seeds); CNN-LSTM **less than half the
  spread**. Never claim the CNN-LSTM is more accurate.
- **Error overlap (seed 42, validation):** baseline 70 errors, CNN-LSTM 77,
  **69 shared**. Standing errors: the same 31 windows. **All 69 shared errors
  come from subjects 28 (38) and 29 (31).** The static confusion is in those
  people's data, not in either architecture. Hypothesis half confirmed: the
  static confusion is untouched. The other half (LSTM helps dynamic classes) is
  not supported: the baseline is already 100% there, and the LSTM makes 7
  dynamic errors.
- Deployment choice is **deferred to §8 on the test set**.
- Helpers defined in §6.3 for later sections: `build_model(name, config)` and
  `predict(model, X)`.
- Notebook executes end to end in **~2 min** (through §6.0); the seed study is
  most of that.

Measured in Phase 5 (§7.0 experiments, all single runs judged against the
noise threshold **√2 × 0.0259 = 0.0366** val loss):

- **Sweep (seed 42, Δ val loss vs default 0.1605):** lr 3e-4 −0.024 (best
  epoch 7), lr 3e-3 +0.022 (best epoch 1), batch 32 −0.003 (epoch 2), batch 128
  −0.011 (epoch 8), dropout 0.0 +0.002, dropout 0.5 +0.001, kernel 3 −0.017,
  kernel 7 −0.034. **All within noise.** Best epoch moves monotonically with
  lr and batch size; the best result does not.
- **Kernel 3 (RF 22) is not worse.** The §5.1 receptive-field prediction is
  **not supported**, and the notebook says so.
- **Kernel 7 over 4 seeds:** 0.1406 ± 0.0118 vs default 0.1583 ± 0.0259; each
  wins 2 seeds. Not confirmed (winner's curse); **kernel 5 kept.**
- **Ablation (30 epochs, no early stopping):** dropout 0.3 ends at val loss
  0.4281 (2.7× the 0.1605 kept); no dropout ends at 0.3724. Best val loss
  0.1605 vs 0.1622, so **early stopping is the effective regulariser and dropout
  has no measurable effect.** First 13 epochs of the no-ES run are asserted
  identical to §5.2. The no-dropout run spikes at epoch 21 (train loss too),
  an optimisation instability.
- **Augmentation (jitter σ 0.05 + scaling σ 0.1):** Δ −0.004, acc 0.9595,
  sitting 0.870 / standing 0.921. No effect; **off.**
- **Capacity control:** width **85** → 76,846 params (CNN-LSTM 77,702). Four
  seeds: 0.1468 ± 0.0174, acc 0.9623 ± 0.0039. Closes **about half** the
  baseline→LSTM loss gap. **Do not claim sequence modelling helps.**
- **Random window split (80/20 within the 15 training subjects):** own val
  loss 0.0698 / acc 0.9688; the same model on the 6 unseen subjects scores
  **0.3610** / 0.9557. Best epoch **29 of 30** (early stopping never fires).
  **990 of 1,056 (94%)** random-val windows share 64 samples with a training
  window (checked on the raw data).
- **CONFIG unchanged.** §8 evaluates the §5.2 baseline and the §6.2 CNN-LSTM
  as trained. The test set is still untouched.
- Full notebook: **~7 min** (406 s).

## Commitments made in the notebook text (later sections must honour)

- **§7.0 (Khalifa): all delivered in Phase 5.** Capacity control (§7.5),
  random split (§7.6), regulariser ablation (§7.3), augmentation (§7.4), and a
  four-hyperparameter table with observations (§7.1).
- **§8.0 (Rashed):** deployment decision on the test set (§6.3); check the
  §3.3 prediction that sitting↔standing is the largest off-diagonal mass.
- **§8.5 / §9.0 (Rashed):**
  - inspect subjects 28/29's sitting/standing windows (§6.3);
  - check whether misclassified static windows are postural adjustments
    (§3.3 promised "section 8.5 checks").
  (§3.3 originally said §8.5, which is not in the brief's numbering. It now
  points to §9.0.)
