# Tumor Data — Parquet Generator

This folder contains a Python script that generates a Parquet file from tumor images with synthetic medical metadata.

---

## Contents

- **`create_parquet.py`** — Reads images from the `DataFiles/parquet/Tumor Data/Images` folder and produces a Parquet file with columns for image ID, path, caption, modality, and diagnosis.

---

## Generated Schema

| Column | Type | Description |
|--------|------|-------------|
| `id` | string | Image filename (without extension) |
| `image_path` | string | Relative path to the image file |
| `caption` | string | Synthetic medical description of the image |
| `modality` | string | Imaging modality (`MRI` or `CT`) |

---

## How to Run

```bash
cd Scripts/Python/Tumor\ Data
python create_parquet.py
```

The output Parquet file will be saved to `DataFiles/parquet/Tumor Data/`.

---

[← Back to Python README](../README.md)
