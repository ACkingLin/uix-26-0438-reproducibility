# UIX-26-0438 reproducibility materials

Reproducibility materials for **Independent Risk Calibration Under Scarce Expert Masks for Breast Ultrasound Segmentation: A Locked Cross-Cohort Validation Study**.

## Download

The [v1.0.0 release](https://github.com/ACkingLin/uix-26-0438-reproducibility/releases/tag/v1.0.0) contains the complete software/results archive and all ten original locked checkpoints. The archives are stored in small parts for reliable transfer. The downloader verifies each part and automatically restores the original ZIP files with their recorded SHA-256 checksums.

Download [download_release.py](download_release.py) and run with Python 3.9 or later (no extra packages):

```bash
python3 download_release.py --out uix_materials
```

This retrieves about 0.96 GB and produces:

- `Supplementary_Software_UIX.zip`: source code, dependencies, all 60 run configurations and patient partitions, calibration curves, derived result tables, component records, and integrity manifests.
- `Locked_Checkpoints_UIX.zip`: all ten original locked checkpoints with their run identifiers and checksums.

To obtain only the software and results (about 24 MB):

```bash
python3 download_release.py --software-only --out uix_materials
```

Interrupted downloads can be resumed by repeating the same command. [ARCHIVE_PARTS.json](ARCHIVE_PARTS.json) lists the ordered parts, sizes, and hashes; [SHA256SUMS.txt](SHA256SUMS.txt) records the two final archive hashes.

Extract both archives into the same parent directory. From `UIX_reproducibility/`, run:

```bash
python tools/reproduce.py audit --models
```

The archive README provides the measured environment and detailed instructions for statistical recalculation without imaging data and GPU re-inference with the public data and supplied checkpoints.

## Public datasets

Raw ultrasound images and masks are obtained from their original repositories and are not redistributed here:

- [BrEaST](https://doi.org/10.7937/9WKK-Q141).
- [BUS-UCLM v3](https://doi.org/10.17632/7fvgj4jsp7.3).

The archives preserve the original sealed-test protocol, source identities, and patient split records. Revision sensitivities use the original checkpoints and known cohorts.
