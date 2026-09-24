# Dataset

## Source

**Human Activity Recognition Using Smartphones Dataset, Version 1.0**
Reyes-Ortiz, J. L., Anguita, D., Ghio, A., Oneto, L., and Parra, X.
Smartlab, Università degli Studi di Genova (Italy) and CETpD, Universitat
Politècnica de Catalunya (Spain).

UCI Machine Learning Repository, dataset 240.
<https://archive.ics.uci.edu/dataset/240/human+activity+recognition+using+smartphones>

The dataset is not committed to this repository (61 MB archive, 270 MB
extracted). Reproduce it with:

```bash
python scripts/get_data.py
```

The archive is verified against SHA-256
`c00b803081a5c797cd5e4b83700a9810b38d53d9d84e01917e090e1fdbc81031`
before extraction.

## Licence and required attribution

Distributed AS-IS. **Commercial use is prohibited.** Use in publications must
acknowledge the source paper:

> Anguita, D., Ghio, A., Oneto, L., Parra, X., and Reyes-Ortiz, J. L. (2013).
> A Public Domain Dataset for Human Activity Recognition Using Smartphones.
> *21st European Symposium on Artificial Neural Networks (ESANN 2013)*,
> Bruges, Belgium, 24–26 April 2013.

This project is coursework and non-commercial, so the licence permits the use.
The citation above must appear in the report's reference list.

## How the data was collected

30 volunteers aged 19–48 wore a Samsung Galaxy S II on the waist and performed
six activities. The phone's accelerometer and gyroscope were sampled at 50 Hz.
Labels were assigned manually from video recordings of each session.

Signals were noise-filtered, then cut into **fixed-width sliding windows of
2.56 s with 50% overlap** — 128 readings per window. Total acceleration was
separated into body and gravity components with a 0.3 Hz Butterworth low-pass
filter.

## What we use

The repository ships two representations. **We use the raw inertial signals,
not the 561-feature vector.**

| | Raw inertial signals (used) | `X_train.txt` 561 features (not used) |
|---|---|---|
| Shape per window | 9 channels × 128 timesteps | 1 × 561 |
| Content | Sensor readings over time | Hand-engineered time/frequency statistics |
| Suits | 1-D CNN, LSTM — model learns its own features | MLP, classical ML |

The 561-feature table already encodes a human's idea of what matters (means,
standard deviations, FFT coefficients, correlations). Feeding it to a network
would mean the network learns almost nothing about the signal — the feature
engineering would be doing the work. Using the raw signals is what makes this a
deep learning problem: the convolutional filters have to discover the periodic
structure of a footstep for themselves.

### The nine channels

| Channel | Sensor | Units |
|---|---|---|
| `total_acc_{x,y,z}` | Accelerometer, raw | g (9.80665 m/s²) |
| `body_acc_{x,y,z}` | Accelerometer, gravity removed | g |
| `body_gyro_{x,y,z}` | Gyroscope | rad/s |

`total_acc = body_acc + gravity`, so the three channel groups are not
independent. Keeping all nine is deliberate: the gravity component in
`total_acc` encodes device orientation, which is the main signal separating
static postures (sitting, standing, laying) that have almost no body
acceleration.

## Size and class balance

| Split | Windows | Subjects |
|---|---|---|
| Train (official) | 7,352 | 21 — IDs 1, 3, 5–8, 11, 14–17, 19, 21–23, 25–30 |
| Test (official) | 2,947 | 9 — IDs 2, 4, 9, 10, 12, 13, 18, 20, 24 |

| Class | Label | Train | Test |
|---|---|---|---|
| 1 | WALKING | 1,226 | 496 |
| 2 | WALKING_UPSTAIRS | 1,073 | 471 |
| 3 | WALKING_DOWNSTAIRS | 986 | 420 |
| 4 | SITTING | 1,286 | 491 |
| 5 | STANDING | 1,374 | 532 |
| 6 | LAYING | 1,407 | 537 |

Imbalance is mild — the largest class is about 1.4× the smallest. Class
weighting is therefore not the main concern. The evaluation problem here is
different and is covered in the report: errors are **concentrated in one
confusable pair** (sitting vs standing), so a high overall accuracy can hide a
specific, systematic failure. Per-class recall is the metric that exposes it.

## Split design and leakage

**The official train/test split is subject-disjoint** — no volunteer appears in
both. This matters more than it looks.

Windows overlap by 50%, so two consecutive windows share 64 of their 128
readings. If the data were shuffled and split randomly, a window in the test set
would share half its samples with a window in the training set. The model would
be scored partly on data it had already seen, and reported accuracy would be
inflated. Worse, even non-overlapping windows from the same person share that
person's individual gait signature, so a random split measures *"can the model
recognise this person's walk it has already memorised"* rather than *"can it
recognise walking in someone new"*.

The second is the question that matters, because the deployed model meets users
it has never seen.

We therefore:

1. Keep the official subject-disjoint test set untouched until final evaluation.
2. Carve the validation set out of the 21 training subjects **by subject**, not
   by window, so the same guarantee holds during model selection.
3. Demonstrate the size of the effect in the notebook by also training under a
   random window-level split and reporting the inflated figure alongside the
   honest one.

## Known limitations

- **Narrow demographic.** All 30 subjects are aged 19–48. Gait changes
  substantially with age and mobility impairment, and the most valuable
  application of this task — fall detection and activity monitoring for elderly
  users — is exactly the population absent from the data.
- **Single device, single position.** One phone model, worn on the waist.
  Wrist-worn or pocket-carried sensors produce different signals.
- **Laboratory conditions.** Scripted activities recorded under supervision.
  Real-world data contains transitions, interruptions and mixed activities that
  do not appear here.
- **No demographic metadata.** Sex, height and weight are not published, so
  bias across those groups cannot be measured — only suspected.
- **Version 1.0 has no transition classes.** A later version of this dataset
  (HAPT) adds postural transitions such as stand-to-sit. Their absence here
  means every window is assumed to contain exactly one steady activity.
