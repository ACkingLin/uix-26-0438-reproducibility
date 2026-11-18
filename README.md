# UIX-26-0438 reproducibility materials

Reproducibility materials for **Independent Risk Calibration Under Scarce Expert Masks for Breast Ultrasound Segmentation: A Locked Cross-Cohort Validation Study**.

## Download

The [v1.0.0 release](https://github.com/ACkingLin/uix-26-0438-reproducibility/releases/tag/v1.0.0) provides:

- `Supplementary_Software_UIX.zip`: source code, dependencies, all 60 run configurations and patient partitions, calibration curves, derived result tables, component records, and SHA-256 manifests.
- `Locked_Checkpoints_UIX.zip`: all ten original locked checkpoints, with run identifiers and checksums.
- `SHA256SUMS.txt`: checksums for both archives.

Extract both archives into the same parent directory. From `UIX_reproducibility/`, run `python tools/reproduce.py audit --models`. The archive README provides detailed instructions for statistical recalculation and GPU re-inference.

## Public datasets

Raw images and masks are obtained from their original repositories and are not redistributed here:

- [BrEaST](https://doi.org/10.7937/9WKK-Q141).
- [BUS-UCLM v3](https://doi.org/10.17632/7fvgj4jsp7.3).

The archives preserve the original sealed-test protocol, source identities, and split records. Revision sensitivities use the original checkpoints and known cohorts.
