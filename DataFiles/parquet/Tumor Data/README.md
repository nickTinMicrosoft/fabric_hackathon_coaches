# Tumor Data

This folder contains the tumor image dataset used in the hackathon. It includes source images and any generated Parquet files containing image metadata.

---

## Folders

| Folder | Description |
|--------|-------------|
| [Images](Images/) | Source tumor images (`.jpg`) used to generate the Parquet metadata file |

---

## How It Works

1. The **Images** folder contains raw tumor scan images.
2. The Python script [`create_parquet.py`](../../../Scripts/Python/Tumor%20Data/create_parquet.py) reads these images and generates a Parquet file with synthetic medical metadata (captions, modality, diagnosis, etc.).
3. The resulting Parquet file is placed in this folder and can be ingested into a Fabric Lakehouse.

---

[← Back to parquet README](../README.md)
