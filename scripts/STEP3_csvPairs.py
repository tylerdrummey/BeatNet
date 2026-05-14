'''
Step 3 - Output pairs to all_mix_pairs.csv
'''

import os
import pandas as pd

DATASET_DIR = os.path.join(os.getcwd(), "djmix_dataset")

all_pairs = []

# ----------------------------
# PROCESS EACH MIX CSV
# ----------------------------
for file in os.listdir(DATASET_DIR):

    if not file.endswith("_features.csv"):
        continue

    file_path = os.path.join(DATASET_DIR, file)

    print(f"\nProcessing {file}...")

    df = pd.read_csv(file_path)

    # 🔥 IMPORTANT: ensure correct order
    df = df.sort_values("track_index").reset_index(drop=True)

    # ----------------------------
    # CREATE PAIRS
    # ----------------------------
    for i in range(len(df) - 1):

        song1 = df.iloc[i]
        song2 = df.iloc[i + 1]

        pair_row = {}

        # metadata
        pair_row["mix"] = song1["mix"]
        pair_row["song1_index"] = song1["track_index"]
        pair_row["song2_index"] = song2["track_index"]
        pair_row["song1_title"] = song1["title"]
        pair_row["song2_title"] = song2["title"]

        # features for song 1
        for col in df.columns:
            if col in ["title", "mix", "track_index"]:
                continue
            pair_row[f"{col}_1"] = song1[col]

        # features for song 2
        for col in df.columns:
            if col in ["title", "mix", "track_index"]:
                continue
            pair_row[f"{col}_2"] = song2[col]

        all_pairs.append(pair_row)

# ----------------------------
# SAVE OUTPUT
# ----------------------------
pairs_df = pd.DataFrame(all_pairs)

output_path = os.path.join(DATASET_DIR, "all_mix_pairs.csv")
pairs_df.to_csv(output_path, index=False)

print(f"\nSaved paired dataset: {output_path}")