import os
import random
import pandas as pd

image_folder = "DataFiles\parquet\Tumor Data\Images"

# ---- Fake medical vocabulary ----
descriptors = [
    "irregular mass",
    "well circumscribed lesion",
    "heterogeneous density region",
    "hyperintense signal area",
    "hypointense abnormality",
    "lobulated tumor structure",
    "calcified nodular formation",
    "contrast enhancing mass",
    "necrotic core appearance",
    "edematous surrounding tissue"
]

locations = [
    "left hemisphere",
    "right frontal lobe",
    "temporal region",
    "parietal area",
    "occipital lobe",
    "central brain region"
]

diagnosis = [
    "suspicious for malignancy",
    "likely benign growth",
    "possible glioma",
    "consistent with metastatic lesion",
    "requires further evaluation",
    "probable meningioma"
]

modalities = ["MRI", "CT"]

def make_caption():
    return f"{random.choice(descriptors)} located in the {random.choice(locations)}, {random.choice(diagnosis)}."

rows = []

for file in os.listdir(image_folder):
    if file.lower().endswith((".png", ".jpg", ".jpeg")):
        rows.append({
            "id": file.replace(".png","").replace(".jpg",""),
            "image_path": f"images/{file}",
            "caption": make_caption(),
            "label": random.choice(["benign", "malignant"]),
            "modality": random.choice(modalities),
            "split": random.choice(["train","train","train","val","test"])
        })

df = pd.DataFrame(rows)

# save parquet
df.to_parquet("tumor_dataset.parquet", index=False)

print("Parquet created:", len(df), "rows")
