# Methodology

## Objective
Train a supervised classifier to predict **Bus asteroid taxonomic classes** from SMASS-II visible-wavelength reflectance spectra. Taxonomic class denotes spectral similarity rather than measured mineral composition.

## Dataset acquisition
- Spectral archive: `EAR_A_I0028_4_SBN0001_SMASSII_V1_0` (PDS3 spectral tables).
- Taxonomy archive: `EAR_A_5_DDR_TAXONOMY_V6_0`.
- Input spectra: **1,341** tables successfully read.
- Taxonomy catalogue: **2,615** records; **1,443** usable Bus-labelled entries across **26** classes prior to joining.

## Spectral preprocessing
1. Read wavelength, reflectance, and error triplets from PDS spectral tables.
2. Remove **24 all-zero measurement rows** across two affected spectra.
3. Round and align measurements to a **197-feature grid** from **0.435 to 0.925 µm** in **0.0025 µm** steps, with duplicate and off-grid validations.
4. Initially, the aligned matrix contained **11,341 missing cells**. Interpolate **only short interior gaps** of at most two missing wavelength bins when values exist on both sides, recovering **1,966** values. **9,375 cells** remain missing after interpolation.
5. Keep a record of which cells were interpolated to distinguish measured and inferred reflectance.

## Join and taxonomy labels
Normalize asteroid numbers extracted from filenames (for example, `1007_01.tab`), clean invalid taxonomy labels including `***`, and perform a many-to-one join. Resolve six provisional-designation cases. This yields **1,341 unique labelled spectra**, **197 features** and **25 matched Bus classes**.

## Modelling
The **O** class has one example and is not included in the trained classifier. Use stratified random split (80/20, random seed 42) on the remaining **1,340** examples: **1,072 training**, **268 held-out test**, **24 classes**.

Build training-fold pipelines for median imputation, standardization and `SVC(kernel="rbf", class_weight="balanced")`. Compare against a majority-class `DummyClassifier`; use `StratifiedKFold(n_splits=3, shuffle=True, random_state=42)`.

Grid search:
- `C ∈ {0.1, 1, 10, 100}`
- `gamma ∈ {"scale", 0.001, 0.01}`
- Optimize mean cross-validation **macro-F1**, not overall accuracy.

Select `C=10, gamma="scale"` and evaluate once on the held-out test subset.

## Limitations
Spectral class frequencies are imbalanced. Rare classes have very small held-out sample counts; a seemingly perfect class F1 can reflect a single successful prediction. Reflectance curves can be affected by space weathering, observation geometry, measurement uncertainty and wavelength coverage. No mineral-abundance estimation, resource valuation, independent survey validation or production cloud deployment is established by these experiments.

*All numerical outcomes are transcribed from outputs saved in the provided Jupyter notebook; this documentation is not an independently rerun model audit.*
