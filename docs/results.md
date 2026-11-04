# Results

Numbers in this report are transcribed from the provided notebook's saved outputs.

## Preparation audit

| Measure | Result |
|:--|--:|
| Loaded SMASS-II spectra | 1,341 |
| Taxonomy catalogue rows | 2,615 |
| Usable Bus-labelled taxonomy entries | 1,443 |
| Matched spectra | 1,341 |
| Spectral feature count | 197 |
| Matched Bus classes | 25 |
| Initial missing spectral cells | 11,341 |
| Short-gap interpolation fills | 1,966 |
| Remaining missing cells | 9,375 |
| Train / test | 1,072 / 268 |
| Classes in trained classifier | 24 |

## Model selection — training-set cross-validation

| Candidate | Mean CV accuracy | Mean CV balanced accuracy | Mean CV macro-F1 |
|:--|--:|--:|--:|
| Majority-class DummyClassifier | 0.285 | 0.042 | 0.019 |
| Untuned weighted RBF-SVM | 0.696 | 0.654 | 0.605 |
| Best tuned weighted RBF-SVM | **0.788** | **0.658** | **0.658** |

Best `C=10`, `gamma="scale"`; macro-F1 standard deviation **0.025** over CV folds. **0.788 is cross-validation accuracy, not the held-out test accuracy.**

## Held-out test evaluation

**268 objects**, **0.810 accuracy**, **0.730 balanced accuracy**, **0.718 macro-F1**.

| Class | Precision | Recall | F1 | Support |
|:--|--:|--:|--:|--:|
| A | .750 | 1.000 | .857 | 3 |
| B | .833 | .833 | .833 | 12 |
| C | .857 | .857 | .857 | 28 |
| Cb | .500 | .667 | .571 | 6 |
| Cg | .500 | .500 | .500 | 2 |
| Cgh | .667 | .667 | .667 | 3 |
| Ch | .885 | .821 | .852 | 28 |
| D | 1.000 | .500 | .667 | 2 |
| K | .364 | .667 | .471 | 6 |
| L | .625 | .714 | .667 | 7 |
| Ld | .750 | 1.000 | .857 | 3 |
| R | 1.000 | 1.000 | 1.000 | 1 |
| S | .958 | .883 | .919 | 77 |
| Sa | 1.000 | .714 | .833 | 7 |
| Sk | .500 | .333 | .400 | 3 |
| Sl | .600 | .900 | .720 | 10 |
| Sq | .833 | 1.000 | .909 | 10 |
| Sr | .667 | .667 | .667 | 3 |
| T | .500 | .333 | .400 | 3 |
| V | 1.000 | .857 | .923 | 7 |
| X | .773 | .773 | .773 | 22 |
| Xc | .818 | .750 | .783 | 12 |
| Xe | .500 | .200 | .286 | 5 |
| Xk | .778 | .875 | .824 | 8 |

**Interpretation.** Macro-F1 reduces the masking effect of dominant classes. S, C and Ch have comparatively high support, whereas scores of classes with one to three test samples are highly uncertain. The O-class singleton was excluded from the classification experiment.

## Matched class counts

S 383 · C 142 · Ch 138 · X 111 · B 60 · Xc 60 · Sq 52 · Sl 49 · Xk 39 · V 35 · L 34 · Sa 34 · Cb 33 · K 31 · Xe 28 · Sk 16 · A 16 · Cgh 15 · Sr 15 · T 14 · Ld 13 · D 9 · Cg 9 · R 4 · O 1

No compositional analysis or independently verified test dataset is included.
